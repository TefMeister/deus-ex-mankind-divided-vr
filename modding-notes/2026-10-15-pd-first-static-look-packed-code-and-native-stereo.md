# 2026-10-15 (`/pd`, dev PC, no launch): first static look: packed code, and the game's own side-by-side 3D

The game was not launched, and nothing here has been run. Read from `retail\DXMD.exe` and the game's registry key
only. Evidence and scripts: `dev-archive/recon/2026-10-15-pd-first-static-look-dev-pc/`.

## What was found `[inferred-static 2026-10-15]`

1. **64-bit, Direct3D 11 by default** (Direct3D 12 by the `EnableDX12` registry switch). Both are loaded at run time.
2. **The code is packed at rest.** The section that will hold the code (`.trace`, 25 MB) has no bytes on disk; an
   80 MB encrypted block (`.sdata`) and a small unpacker (`.xtext`) fill it at start-up. No code on disk refers to
   the settings strings. That fits Denuvo still being on the Steam build `[hypothesis]` (`/gr` found it there in
   2020). So: **every question about the code waits for a memory image taken from the running game.**
3. **The game has its own stereo 3D, including a side-by-side mode** for 3D TVs, besides NVIDIA 3D Vision and AMD
   HD3D. Registry: `Stereoscopic3DMode` (0), `StereoSeparation` (75), `StereoPopOut` (250),
   `StereoNearSeparationMultiplier` (350), `Stereoscopic3DAMDSwapEyes` (0). It switches side-by-side off in a window
   and with several monitors, and needs exclusive fullscreen in DX11 and v-sync.
4. **A hidden `-vrdemo` switch** loads a scene `98_vr/98_vr_master.entity`; together with `BreachVR` input flags it
   is most likely the 2016 PlayStation VR demo's leftovers. No headset runtime is named in the exe.
5. `-nolauncher` skips the small launcher window (good for unattended driving).
6. **Every blur and screen effect has a registry switch** except the vignette / damage tint: `MotionBlur` (already 0),
   `DOFQuality`, `ChromaticAberration`, `LensFlares`, `Bloom`, `Sharpen`, `TAA`.
7. **The dev PC is not windowed yet** (`Fullscreen` 1, exclusive, 1920x1080).

## Why the stereo mode matters

A game that draws its own two eyes has already done the step every other project builds by hand. If side-by-side
renders each eye with its own camera (as 3D Vision titles do), the VR work becomes: allow it in a window, take each
half to its headset eye, and drive the camera with the head.

## What is NOT established

- Which `Stereoscopic3DMode` value is side-by-side (string order suggests 1) `[hypothesis]`.
- Whether side-by-side is a real per-eye render or a cheap depth-based fake. A screenshot answers it: a real one
  shows near objects shifted between the halves, with things visible in one eye only at edges.
- Whether the unit of the separation numbers is hundredths.
- Whether the Steam build really still has Denuvo (the layout fits, but that is not proof).

## Next (each needs the game running)

1. **Window the dev PC** (registry, backup first), as on the home PC: `Fullscreen` 0, 1280x720.
2. **One fullscreen side-by-side test** (one-off, exclusive fullscreen at 1280x720, key backed up first):
   `Stereoscopic3DMode` 1, start with `-nolauncher`, screenshot in gameplay. Two squeezed pictures = side-by-side
   (then compare near and far objects); one picture = wrong value, try 2; game refuses or reverts = read its log.
3. **Take a memory image of the unpacked exe** from the running game (read-only, as Manhunt's), so the stereo code
   and the windowed check can be read statically.
