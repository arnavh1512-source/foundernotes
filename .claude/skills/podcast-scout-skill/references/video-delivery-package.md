# Delivery package for every video

Owner rule, 2026-11-13: "every time you make a video I need a thumbnail, description, a short, with the title."

A video is not finished when the long film passes QC. Deliver all five items below, without being asked, in `studio-output/<slug>/full/`.

| Item | File | Requirements |
|---|---|---|
| Long video | `final/video.mp4` | Passes `qc_video.py`; all channel rules apply |
| Short | `short/summary-short.mp4` | Vertical 1080x1920, under 60 s, a summary of the whole video (not a clip of its opening) |
| Thumbnail | `package/thumbnail.png` | 1280x720, same visual style as the video, one large face or object, at most four words, channel logo |
| Title | in `package/title-and-description.md` | One recommended title plus three alternatives; also a suggested Short title |
| Description | in `package/title-and-description.md` | Two or three sentences, chapter timestamps taken from the final narration timings, every source with a DOI or link, the educational disclaimer and the AI-voice line |

## The Short

- Write a new narration of about 130-150 words that covers the whole video: hook, the main findings in order, the practical moves, a one-line close pointing to the full video.
- Record it with the channel narrator and run the speech check.
- Reuse scenes from the long film, re-timed to the new narration. Do not introduce claims that are not in the long video.
- Layout: fixed title at the top, the 16:9 picture across the middle (uncropped), large captions below, the bottom fifth left empty for YouTube's interface, a 2-3 second end card with the logo and "Full video on the channel".
- Loudness about -14 LUFS, as for the long video.

## The thumbnail

- Draw it with the same engine and palette as the video so the two match.
- The words on the image should complement the title, not repeat it.
- Check it at small size: the face and the words must still read.

## Title and description

- Titles name the viewer's problem in plain words. No invented numbers, no promises the video does not keep.
- Chapters come from `narration/timings.json` of the final cut, so they are correct to the second.
- List only sources that were actually read for the video.
- Never name the source podcast, host or guest.

## What stays the owner's job

Uploading, choosing between title options, and YouTube's altered-content setting. The studio never uploads or publishes.
