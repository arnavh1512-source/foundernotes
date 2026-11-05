#!/usr/bin/env node
// Render a time-driven HTML page (SKILL.md, "The render contract") with headless Chromium + ffmpeg.
//
//   node render.mjs page.html --out video.mp4 [--poster 6.5] [--draft] [--alpha] [--audio track.mp3]
//   node render.mjs page.html --stills 0,2.5,5 --out dir     one PNG per time, plus dir/sheet.png
//   node render.mjs page.html --sheet 12 --out dir           12 evenly spaced frames, plus dir/sheet.png
//
// --draft   half size, 15 fps, fast encode: for checking timing, not for delivery
// --alpha   transparent ProRes 4444 .mov (the page must not paint a background)
// --poster  frame 0 shows the frame at this time, so thumbnails show a settled frame
// --audio   use this file instead of the page's window.motionAudio()
// MOTION_CHROMIUM=/path/to/chrome overrides the browser Playwright would launch.
import { spawn, execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { mkdirSync, writeFileSync, rmSync, readdirSync } from "node:fs";
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
    console.error("usage: render.mjs <page.html> --out <video.mp4|dir> [--stills t,t,…|--sheet n] [--draft] [--alpha] [--poster t] [--audio file]");
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
  const proc = spawn("ffmpeg", ["-y", "-loglevel", "error", ...args], { stdio: ["pipe", "inherit", "inherit"] });
  const done = new Promise((resolve, reject) =>
    proc.on("close", (code) => (code === 0 ? resolve() : reject(new Error(`ffmpeg exited ${code}`)))));
  return { stdin: proc.stdin, done };
}

async function openPage(browser, url, scale) {
  const probe = await browser.newPage();
  await probe.goto(url);
  const spec = await probe.evaluate(() => window.MOTION);
  await probe.close();
  if (!spec?.width || !spec?.height || !spec?.fps || !spec?.duration) {
    throw new Error("page must set window.MOTION = { width, height, fps, duration }");
  }
  const context = await browser.newContext({ viewport: { width: spec.width, height: spec.height }, deviceScaleFactor: scale });
  const page = await context.newPage();
  page.on("pageerror", (err) => console.error("page error:", err.message));
  await page.goto(url, { waitUntil: "load" });
  const hasSeek = await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((img) => img.decode().catch(() => {})));
    return typeof window.seek === "function";
  });
  if (!hasSeek) throw new Error("page must define window.seek = async (t) => { … }");
  return { page, spec };
}

async function shoot(page, t, alpha) {
  await page.evaluate(async (t) => { await window.seek(t); await document.fonts.ready; }, t);
  return page.screenshot({ type: "png", omitBackground: alpha });
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

async function video(page, spec, opts) {
  const fps = opts.draft ? Math.min(15, spec.fps) : spec.fps;
  const frames = Math.round(spec.duration * fps);
  const out = opts.alpha ? opts.out.replace(/\.\w+$/, ".mov") : opts.out;
  mkdirSync(path.dirname(path.resolve(out)), { recursive: true });

  let audio = opts.audio;
  let tempAudio;
  if (!audio && !opts.draft && (await page.evaluate(() => typeof window.motionAudio === "function"))) {
    tempAudio = audio = `${out}.audio.wav`;
    writeFileSync(audio, Buffer.from(await page.evaluate(() => window.motionAudio()), "base64"));
  }

  const args = ["-f", "image2pipe", "-framerate", String(fps), "-i", "-"];
  if (audio) args.push("-i", audio, "-af", "loudnorm=I=-14:LRA=11:TP=-1", "-t", String(spec.duration));
  if (opts.alpha) {
    args.push("-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le");
    if (audio) args.push("-c:a", "pcm_s16le");
  } else {
    args.push("-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
      "-crf", opts.draft ? "26" : "16", "-preset", opts.draft ? "veryfast" : "slow", "-movflags", "+faststart");
    if (audio) args.push("-c:a", "aac", "-b:a", "192k");
  }
  args.push(out);

  const enc = ffmpeg(args);
  const started = Date.now();
  for (let i = 0; i < frames; i++) {
    const t = i === 0 && opts.poster !== undefined ? Number(opts.poster) : i / fps;
    if (!enc.stdin.write(await shoot(page, t, !!opts.alpha))) {
      await new Promise((resolve) => enc.stdin.once("drain", resolve));
    }
    if (i % fps === 0) process.stdout.write(`\r${i}/${frames} frames`);
  }
  enc.stdin.end();
  await enc.done;
  if (tempAudio) rmSync(tempAudio);
  console.log(`\r${frames} frames in ${((Date.now() - started) / 1000).toFixed(1)}s → ${out}`);
}

const opts = parseArgs(process.argv.slice(2));
const executablePath = process.env.MOTION_CHROMIUM;
const browser = await loadChromium().launch(executablePath ? { executablePath } : {});
try {
  const { page, spec } = await openPage(browser, pathToFileURL(path.resolve(opts.page)).href, opts.draft ? 0.5 : 1);
  if (opts.stills) await stills(page, opts.stills.split(",").map(Number), opts.out);
  else if (opts.sheet) {
    const n = Number(opts.sheet);
    await stills(page, Array.from({ length: n }, (_, i) => +((spec.duration * (i + 0.5)) / n).toFixed(2)), opts.out);
  } else await video(page, spec, opts);
} finally {
  await browser.close();
}
