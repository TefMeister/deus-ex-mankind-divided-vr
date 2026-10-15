# 2026-10-15 (evening, dev PC, `/lm`, unattended, one reader): windowed, the game's own side-by-side 3D, and the camera

Three launches through Steam with `-nolauncher`. Evidence: `dev-archive/recon/2026-10-15-lm-windowed-side-by-side-camera/`.

## 1. The dev PC is windowed, and the music is off

- Registry key `HKCU\Software\Eidos Montreal\Deus Ex: MD` exported first (session scratchpad). Set `Fullscreen` 0,
  `ExclusiveFullscreen` 0, `WindowWidth`/`UserWindowWidth` 1280, `WindowHeight`/`UserWindowHeight` 720.
- Measured: client 1280x720 while the desktop stayed 1920x1080 `[verified-live 2026-10-15, n=2 runs]`. Window title
  `Deus Ex: Mankind Divided v1.19 build 801.0`, about 45-50 s after the launch.
- Music: OPTIONS -> AUDIO -> Music Volume to 0 %, saved in the game's own `game_options.bin` `[verified-live 2026-10-15, n=1]`.
- Graphics page lists Motion Blur, Depth of Field (on), Bloom, Lens Flares, Sharpen, Volumetric Lighting; Chromatic
  Aberration is registry-only so far. Not switched off yet (that is for the headset build).
- Menu to gameplay by keyboard: STORY -> CONTINUE, about 2.5 min loading, Space on the story card. Two Enter presses
  sent right after the window appeared were lost; check the screen first.

## 2. ⭐ The game's side-by-side 3D draws a real picture per eye

- `Fullscreen` 1, `ExclusiveFullscreen` 1, `Stereoscopic3DMode` 1 (separation 75, pop-out 250, near multiplier 350 as
  shipped). The game started minimised; brought to the front it ran at 1920x1080 although `FullscreenWidth`/`Height`
  said 1280x720.
- **`Stereoscopic3DMode` 1 = side-by-side** `[verified-live 2026-10-15, n=1]`: the menu and gameplay as two squeezed
  pictures, left and right.
- **The two halves are different eye positions, not one copied picture** `[measured 2026-10-15, n=1 frame]`. Horizontal
  offset between the halves (best match, 960-pixel halves, `sbs_offset.py`):

  | Where | Offset |
  | --- | --- |
  | far buildings, far ground | 71 px |
  | ground, nearer and nearer | 70, 69, 68, 67, 66 px |
  | the gun and hand | 30 px |
  | the on-screen display | 0 px |

  The offset changes with distance, so the scene is drawn twice from two cameras; the display is drawn flat on top.
  So the engine already does the step every VR mod needs most: render the world once per eye.
- Not established: whether each eye also gets its own lens (off-centre projection) or only a shifted camera; how
  the separation numbers map to metres.
- Mouse clicks in menus missed in this mode; the keyboard worked, and Enter answers `Quit game?` with Yes.
- Key put back to windowed, 3D off, `FullscreenWidth`/`Height` 1920x1080 as before.

## 3. The camera is found (camera finder `d3d11.dll` `9a90a0264f01`)

- Windowed run, the finder beside the exe, gameplay on the Dubai rooftop: stand 10 s, turn with the mouse, walk 2 s.
- Every 2 s scan found the same four camera-shaped places in vertex-shader constant buffers, columns layout
  `[verified-live 2026-10-15, n=1 run, 130+ scans]`:

  | Place | Buffer | What it holds |
  | --- | --- | --- |
  | `b0 @0` | 544 bytes, the most used (600-1,500 per scan) | view-projection **relative to the camera** (position 0) |
  | `b1 @0` | 144 bytes | view-projection **in world space**: position 75.69, -129.86, 378.80 |
  | `b1 @64` | same buffer | the camera-relative one again |
  | `b11 @32` | 336 bytes, seen less | world space, same camera |

- **`b1 @0` follows the player** `[verified-live 2026-10-15, n=1]`: standing, the position held still; the mouse
  turn changed the forward direction from (-0.22, 0.94) to (0.97, 0.03) and then (0.84, -0.49), the position
  barely moving; walking 2 s moved it about 3 units along that heading (units are most likely metres
  `[hypothesis]`). The forward Z stayed -0.249 through the turn, so **Z is up** `[inferred-static 2026-10-15]`.
- Picture shape 1.777 (the window), lens 1.092 x 1.940: about 85 degrees wide, 55 tall.
- So the world is drawn **camera-relative** (the usual large-world trick): most draws use `b0`, which has no
  position in it. A per-eye shift therefore goes into the camera-relative matrix, not into a world position.
- 147 vertex shaders kept their variable names, 565 were stripped; the camera places all sit in stripped ones, so
  only slot and byte are known.
- The game draws mostly through **deferred contexts**: in gameplay about 200,000 deferred draws and 2,000 command
  lists per 5 s against 75,000 on the immediate context, 8-9 contexts. The finder only scans the immediate context;
  the camera was found anyway.
- Taken back out of the game folder with its log and the proxy log; nothing of ours is installed now.

## 4. The memory image: taken, and its analysis stopped

- The reader's outside, read-only tool (`staging/deus-ex-mankind-divided-vr/memdump/memdump.py`) took a 130.8 MB
  image of `DXMD.exe` in gameplay, 0 ranges unread `[measured 2026-10-15, n=1]`. Non-zero shares: `.trace` 3.8 %,
  `.text` 15 %, `.sdata` 96.2 %, `.xtext` 97.5 %. So the unpacked code does not simply sit in `.trace`.
- Reading into it was stopped by a safety check, since that part of the exe is the copy protection. We leave that
  route alone and work on the graphics side, which today's camera result shows is enough to go on. The image stays
  on this PC and is never committed.

## Recorded

- `first-dev-pc-run_2026-10-15_19-25-55.mp4`, `camera-finder_2026-10-15_19-46-33.mp4` (the game window only), MEGA
  `Videos\deus-ex-mankind-divided-vr`. The side-by-side run was not recorded: OBS refused to start ("Video settings
  cannot be changed while an output is active"); nothing was found active afterwards and the next run recorded.

## Not established

- Whether the side-by-side eyes get their own lens; whether the camera matrices are written on deferred contexts.
- Comfort, scale, anything in a headset.

## Automation

Self-launch ✅ (Steam, `-nolauncher`), menu to gameplay ✅ (keyboard), commands ✅ (options, registry), character and
camera ✅ (mouse turn, walk), self-close ✅ (window close + Enter).
