#!/usr/bin/env node
// Render a time-driven HTML page (SKILL.md, "The render contract") with headless Chromium + ffmpeg.
//
//   node render.mjs page.html --out video.mp4 [--poster 6.5] [--draft] [--alpha] [--audio track.mp3] [--workers 4]
//   node render.mjs page.html --stills 0,2.5,5 --out dir     one PNG per time, plus dir/sheet.png
//   node render.mjs page.html --sheet 12 --out dir           12 evenly spaced frames, plus dir/sheet.png
//
// --draft   half size, 15 fps, fast encode: for checking timing, not for delivery
// --alpha   transparent ProRes 4444 .mov (the page must not paint a background)
// --poster  frame 0 shows the frame at this time, so thumbnails show a settled frame
// --audio   use this file instead of the page's window.motionAudio()
// --blur N  real motion blur: N sub-frames per frame across a 180° shutter (half the frame interval), averaged
//           (idea from the code-animation community's "average 6 subframes"). Costs N× render time; 3–4 is plenty.
// --workers N  capture with N browser pages at once (default 1); frames still reach the encoder in order.
//           Needs a pure seek(t). Roughly N× faster up to the machine's cores.
// A page error, a missing local file, font or image fails the render; page console warnings go to stderr.
// MOTION_CHROMIUM=/path/to/chrome overrides the browser Playwright would launch.
import { spawn, execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { mkdirSync, writeFileSync, rmSync, readdirSync, realpathSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--draft" || a === "--alpha") opts[a.slice(2)] = true;
    else if (a.startsWith("--")) opts[a.slice(2)] = argv[++i];
    else opts.page = a;
  }
  if (!opts.page || !opts.out) {
    console.error("usage: render.mjs <page.html> --out <video.mp4|dir> [--stills t,t,…|--sheet n] [--draft] [--alpha] [--poster t] [--audio file] [--blur n] [--workers n]");
    process.exit(1);
  }
  return opts;
}

// Playwright from this project, else the global install, else this project's playwright-core.
function loadChromium() {
  const req = createRequire(import.meta.url);
  const tries = [
    () => req("playwright"),
    // npm is a .cmd shim on Windows: execFileSync("npm") raises ENOENT there unless run through the shell
    () => req(path.join(execFileSync("npm", ["root", "-g"], { shell: process.platform === "win32" }).toString().trim(), "playwright")),
    () => req("playwright-core"),
  ];
  const errors = [];
  for (const t of tries) {
    try { return t().chromium; } catch (e) { errors.push(e.message.split("\n")[0]); }
  }
  throw new Error("Playwright not found: npm i -D playwright (or npm i -g playwright)\n  tried: " + errors.join("\n  tried: "));
}

function ffmpeg(args) {
  const proc = spawn("ffmpeg", ["-y", "-loglevel", "error", ...args], { stdio: ["pipe", "inherit", "pipe"] });
  let tail = "";
  proc.stderr.on("data", (d) => { tail = (tail + d).slice(-2000); });
  proc.stdin.on("error", () => {}); // EPIPE when ffmpeg dies early (bad --audio path…): `done` reports why
  const done = new Promise((resolve, reject) => {
    proc.on("error", reject); // ffmpeg not on PATH
    proc.on("close", (code) => {
      if (code !== 0) return reject(new Error(`ffmpeg exited ${code}${tail ? ":\n" + tail.trim() : ""}`));
      if (tail) process.stderr.write(tail);
      resolve();
    });
  });
  done.catch(() => {}); // awaited later; this only keeps an early exit from crashing as an unhandled rejection
  return { stdin: proc.stdin, done, kill: () => proc.kill() };
}

// -vf for the video encode. With blur N, sub-frames kN … kN+N-1 (the N ending on frame k's time) are averaged
// into frame k. Converts with the BT.709 matrix at limited range, which is what the stream is tagged as:
// swscale's default is BT.601 and players read untagged HD as BT.709, so brand colours would shift.
// setparams tags the frames too: ffmpeg 7+ takes the stream tags from them over -color_primaries/-color_trc.
export function videoFilter(fps, blur = 1, alpha = false) {
  const mix = blur > 1 ? `tmix=frames=${blur},select='eq(mod(n,${blur}),${blur - 1})',setpts=N/(${fps}*TB),` : "";
  const size = alpha ? "iw:ih" : "trunc(iw/2)*2:trunc(ih/2)*2";
  return `${mix}scale=${size}:out_color_matrix=bt709:out_range=tv,format=${alpha ? "yuva444p10le" : "yuv420p"},` +
    "setparams=color_primaries=bt709:color_trc=bt709";
}

async function probe(browser, url) {
  const page = await browser.newPage();
  await page.goto(url);
  const spec = await page.evaluate(() => window.MOTION);
  await page.close();
  if (!spec?.width || !spec?.height || !spec?.fps || !spec?.duration) {
    throw new Error("page must set window.MOTION = { width, height, fps, duration }");
  }
  return spec;
}

// throw if the page reported an error or a failed asset since the last check
function check(page) {
  if (page.errors.length) throw new Error(page.errors.splice(0).join("\n"));
}

async function openPage(browser, url, spec, scale) {
  const context = await browser.newContext({ viewport: { width: spec.width, height: spec.height }, deviceScaleFactor: scale });
  const page = await context.newPage();
  page.errors = [];
  const origin = new URL(url).origin;
  page.on("pageerror", (err) => page.errors.push(`page error: ${err.message}`));
  page.on("requestfailed", (req) => {
    const u = req.url(), why = req.failure()?.errorText || "failed";
    const own = u.startsWith("file:") || new URL(u).origin === origin;
    // the page's own files must load; ERR_ABORTED is a cancelled request (media range reads), not a missing file
    if (own && why !== "net::ERR_ABORTED") page.errors.push(`failed to load ${u}: ${why}`);
    else console.error(`warning: failed to load ${u}: ${why}`);
  });
  page.on("console", (m) => {
    if (m.type() === "error" || m.type() === "warning") console.error(`page console.${m.type()}: ${m.text()}`);
  });
  await page.goto(url, { waitUntil: "load" });
  const { hasSeek, broken } = await page.evaluate(async () => {
    await document.fonts.ready;
    const broken = [...document.fonts].filter((f) => f.status === "error").map((f) => `font ${f.family}`);
    for (const img of document.images) await img.decode().catch(() => broken.push(`image ${img.currentSrc || img.src}`));
    return { hasSeek: typeof window.seek === "function", broken };
  });
  page.errors.push(...broken.map((b) => `failed to load ${b}`));
  check(page);
  if (!hasSeek) throw new Error("page must define window.seek = async (t) => { … }");
  return page;
}

async function shoot(page, t, alpha) {
  const badFonts = await page.evaluate(async (t) => {
    await window.seek(t);
    await document.fonts.ready;
    return [...document.fonts].filter((f) => f.status === "error").map((f) => f.family);
  }, t);
  page.errors.push(...badFonts.map((f) => `failed to load font ${f}`));
  // animations: "disabled" finishes stray CSS animations/transitions so nothing runs on the wall clock
  const png = await page.screenshot({ type: "png", omitBackground: alpha, animations: "disabled" });
  check(page);
  return png;
}

async function stills(page, times, dir) {
  mkdirSync(dir, { recursive: true });
  // clear stills from earlier runs: the sheet reads a numbered sequence and would pick up stale frames
  for (const f of readdirSync(dir)) if (/^still-\d+\.png$/.test(f) || f === "sheet.png") rmSync(path.join(dir, f));
  for (const [i, t] of times.entries()) {
    const name = `still-${String(i).padStart(2, "0")}.png`;
    writeFileSync(path.join(dir, name), await shoot(page, t, false));
    console.log(`${name}  t=${t}s`);
  }
  const cols = Math.min(times.length, 6);
  const rows = Math.ceil(times.length / cols);
  const sheet = ffmpeg(["-framerate", "1", "-i", path.join(dir, "still-%02d.png"), "-frames:v", "1",
    "-vf", `scale=-2:480,tile=${cols}x${rows}:padding=12:color=0x808080`, "-frames:v", "1", path.join(dir, "sheet.png")]);
  sheet.stdin.end();
  await sheet.done;
  console.log(`sheet.png  ${cols}x${rows} → ${dir}`);
}

async function video(pages, spec, opts) {
  const fps = opts.draft ? Math.min(15, spec.fps) : spec.fps;
  const frames = Math.round(spec.duration * fps);
  const out = opts.alpha ? opts.out.replace(/\.\w+$/, ".mov") : opts.out;
  mkdirSync(path.dirname(path.resolve(out)), { recursive: true });

  let audio = opts.audio;
  let tempAudio;
  if (!audio && !opts.draft && (await pages[0].evaluate(() => typeof window.motionAudio === "function"))) {
    tempAudio = audio = `${out}.audio.wav`;
    writeFileSync(audio, Buffer.from(await pages[0].evaluate(() => window.motionAudio()), "base64"));
  }

  const blur = opts.draft ? 1 : Math.max(1, parseInt(opts.blur || "1", 10));
  const args = ["-f", "image2pipe", "-framerate", String(fps * blur), "-i", "-"];
  if (audio) args.push("-i", audio, "-af", "loudnorm=I=-14:LRA=11:TP=-1", "-t", String(spec.duration));
  args.push("-vf", videoFilter(fps, blur, !!opts.alpha), "-r", String(fps),
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv");
  if (opts.alpha) {
    args.push("-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le");
    if (audio) args.push("-c:a", "pcm_s16le");
  } else {
    args.push("-c:v", "libx264", "-pix_fmt", "yuv420p",
      "-crf", opts.draft ? "26" : "16", "-preset", opts.draft ? "veryfast" : "slow", "-movflags", "+faststart");
    if (audio) args.push("-c:a", "aac", "-b:a", "192k");
  }
  args.push(out);

  const times = [];
  for (let i = 0; i < frames; i++) {
    const t = i === 0 && opts.poster !== undefined ? Number(opts.poster) : i / fps;
    for (let k = 0; k < blur; k++) {           // sub-frames end on t, so the last one is the sharp "real" frame
      times.push(Math.max(0, t - ((blur - 1 - k) / blur) * (0.5 / fps)));
    }
  }
  // page w shoots shots w, w+W, w+2W… one at a time; at most 2W shots run ahead of the encoder, which takes them in order
  const enc = ffmpeg(args);
  const started = Date.now(), W = pages.length, lanes = pages.map(() => Promise.resolve()), shots = [];
  const queue = (j) => {
    const w = j % W;
    shots[j] = lanes[w] = lanes[w].then(() => shoot(pages[w], times[j], !!opts.alpha));
    shots[j].catch(() => {}); // surfaced in order below
  };
  try {
    for (let j = 0, queued = 0; j < times.length; j++) {
      for (; queued < Math.min(times.length, j + 2 * W); queued++) queue(queued);
      const png = await shots[j];
      shots[j] = null;
      if (!enc.stdin.write(png)) await Promise.race([new Promise((resolve) => enc.stdin.once("drain", resolve)), enc.done]);
      if ((j + 1) % (blur * fps) === 0) process.stdout.write(`\r${(j + 1) / blur}/${frames} frames`);
    }
    enc.stdin.end();
    await enc.done;
  } catch (e) {
    enc.kill();
    throw e;
  }
  if (tempAudio) rmSync(tempAudio);
  console.log(`\r${frames} frames in ${((Date.now() - started) / 1000).toFixed(1)}s${W > 1 ? ` (${W} workers)` : ""} → ${out}`);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const workers = parseInt(opts.workers || "1", 10);
  if (!(workers >= 1)) throw new Error("--workers must be a whole number ≥ 1");
  const executablePath = process.env.MOTION_CHROMIUM;
  const browser = await loadChromium().launch(executablePath ? { executablePath } : {});
  try {
    const url = pathToFileURL(path.resolve(opts.page)).href, scale = opts.draft ? 0.5 : 1;
    const spec = await probe(browser, url);
    const n = opts.stills || opts.sheet ? 1 : workers;
    const pages = await Promise.all(Array.from({ length: n }, () => openPage(browser, url, spec, scale)));
    if (opts.stills) await stills(pages[0], opts.stills.split(",").map(Number), opts.out);
    else if (opts.sheet) {
      const n = Number(opts.sheet);
      await stills(pages[0], Array.from({ length: n }, (_, i) => +((spec.duration * (i + 0.5)) / n).toFixed(2)), opts.out);
    } else await video(pages, spec, opts);
  } finally {
    await browser.close();
  }
}

// run only as a script, so tests can import videoFilter (realpath matches how Node names the main module)
if (process.argv[1] && pathToFileURL(realpathSync(process.argv[1])).href === import.meta.url) {
  main().catch((e) => { console.error(`\nrender failed: ${e.message}`); process.exit(1); });
}
