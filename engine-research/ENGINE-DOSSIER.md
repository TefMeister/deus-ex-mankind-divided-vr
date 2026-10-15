# Engine Dossier — Deus Ex: Mankind Divided (Dawn Engine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M2 (2026-10-15 `/lm`): windowed on both PCs; the game's own side-by-side 3D draws a real picture per eye; the camera is found (camera-relative, `b0`/`b1` in vertex-shader buffers). · **VR-readiness verdict:** promising: the engine already renders per eye; next is getting that into a headset.

## 1. Identity
- Game / build / version: Deus Ex: Mankind Divided, Steam build (app 337000), Steam build id 3355064 on the dev PC; `retail\DXMD.exe` file version 1.19, link date 2017-05-11, 100,332,544 bytes, sha256 `73af0e3f28fc` `[inferred-static 2026-10-15]`. In-game `v1.19 build 801.0` (home PC, 2026-09-17). Installed on both PCs; dev PC at `D:\Program Files (x86)\Steam\steamapps\common\Deus Ex Mankind Divided` (44 GB).
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: Eidos-Montréal's **Dawn Engine**, derived from IO Interactive's Glacier 2 `[reported]`. Unchecked against the binary.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.): PhysX 3 + APEX (clothing, destruction), FMOD, Bink 2, AMD AGS, NVTX, Tobii EyeX (eye tracking) `[inferred-static 2026-10-15]` (dlls beside the exe, import table).
- Distinctive file formats / build tags / symbol naming: `runtime\` holds 36 GB of hash-named packages (`<32 hex>.pc_headerlib`, `.pc_fsbm`, `.pc_binkvid`); resource paths `assembly:/scenes/...entity`; class names `Z...` (Glacier style, e.g. `ZPostfilterMotionBlurAspect`, `ZCameraModifier_FieldOfView_Base`); build path `i:\dxng_rc3\code\src\apps\engine\_windows\main.cpp` (DXNG = the internal name). PC port by Nixxes (`-nixxes`, `NixxesBenchmarkEndEvent`) `[inferred-static 2026-10-15]`.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **64-bit**, image base `0x140000000`, ASLR on (DllCharacteristics `0x8120`) `[inferred-static 2026-10-15]`.
- ⚠️ **The code is packed at rest** `[inferred-static 2026-10-15]`: `.trace` is 25 MB of address space with NO bytes on disk, `.sdata` is 80 MB at entropy 7.96 (encrypted or compressed), `.text` is 61 % zeros on disk, the entry point sits in a tiny section named `.reloc`, and `.xtext` (1.3 MB) is the unpacker. Not one RIP-relative reference to the settings strings exists in the on-disk bytes, so the real code is written into `.trace` at start-up. Matches Denuvo still being on the Steam build `[hypothesis]` (see §4). ~~Static code reading needs a memory image~~ A read-only outside image was taken 2026-10-15 (130.8 MB, 0 ranges unread; non-zero `.trace` 3.8 %, `.text` 15 %, `.sdata` 96.2 %, `.xtext` 97.5 %) `[measured 2026-10-15, n=1]`, so the unpacked code does not simply sit in `.trace`. **Reading into it was stopped by a safety check (the copy protection lives there); that route is closed for us.** Work goes through the graphics side instead (§6). The image stays local, never committed.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: **Direct3D 11 by default, Direct3D 12 by switch.** `d3d11.dll` and `d3d12.dll` are loaded at run time (`Loaded d3d11.dll`, `D3D12CreateDevice`), only `dxgi.dll!CreateDXGIFactory` is imported; registry `EnableDX12` (0 on the dev PC) `[inferred-static 2026-10-15]`. `D3DX11CompileFromMemory` is imported, so some shaders are compiled at run time.
- Developer console / cvar system present? how opened?: a `ConsoleCmd <name> <value>` mechanism exists (`Render_ShowDebug`, `EnableFpsString`, `MaxFPS`, `Breach_DisableChipsets`, `Render_ShowEntityDebug`), fed from `[assembly:/common/preinit.ini]` `[inferred-static 2026-10-15]`; whether a player-reachable console exists is unknown. Start-up switches: `-nolauncher` (skips the small launcher window: use it for driving), `-benchmark` (`benchmark.ini`), `-vrdemo` (loads `assembly:/scenes/game/98_vr/98_vr_master.entity`; with `LoadBenchmarkOrVRDemo` and `eGameInputFlags_BreachVR_*` input flags, likely the 2016 PlayStation VR demo's leftovers), `-nixxes`, `-nochroma`, `-forcepack` `[inferred-static 2026-10-15]`. No headset runtime (OpenVR, Oculus, PSVR) is named in the exe.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: Shipped with Denuvo in 2016 `[reported]`; still on the Steam build in 2020, and the GOG build never had it `[reported 2020-04-29]` (DSOGaming, KitGuru; `/gr` 2026-10-04). The packed layout in §3 fits it still being there `[hypothesis]`. A GOG copy would give a clean binary; buying it is Tefa's call.
- Attach workflow that works: not tried, and not planned (the copy protection, §3).
- Injection vector that works: **a `d3d11.dll` proxy beside `DXMD.exe` loads and hooks the device** (`D3D11CreateDevice`, 51 of 51 exports forwarded) `[verified-live 2026-10-15, n=1]`; a `dxgi.dll` proxy loads too (2026-09-17).

**🎮 2026-09-17 (home PC `RTX`, `/lm`) — FIRST LIVE LOOK.**
- **Runs:** Steam launch opens a small in-exe launcher (Play / Options / Website / … / Quit); **Play** reaches the main menu (STORY / BREACH / JENSEN'S STORIES / EXTRAS / OPTIONS / SHOP / SQUARE ENIX / QUIT), build `v1.19 build 801.0` `[verified-live 2026-09-17, n=2]`.
- **With our file added:** A 64-bit `dxgi.dll` proxy in `retail\` loads and the game reaches the main menu `[verified-live 2026-09-17, n=1]`. Calls seen: `SetAppCompatStringPointer` (see below), `CreateDXGIFactory2`, `CompatValue`, `CreateDXGIFactory`. **Windows' app-compat shim (`AcGenral.dll`) calls dxgi's `SetAppCompatStringPointer` before our `DllMain` runs**, and loading the real dxgi at that moment fails (error 1168); the generator now answers that one early call with 0 and loads the real dll a moment later `[verified-live 2026-09-17, n=1]`. Found on Prey, the same thing happens here. The proxy comes from the shared generator `staging/_shared/proxy-gen/` (every export of the real system dll re-exported with the same ordinals; first call of each export logged). 
- **Windowed (for measuring; 1280×720 keeps aspect-keyed numbers the same on both PCs):** Registry `HKCU\Software\Eidos Montreal\Deus Ex: MD\Graphics`: `Fullscreen=0`, `WindowWidth`/`UserWindowWidth=1280`, `WindowHeight`/`UserWindowHeight=720` → 1280×720 client window `[verified-live 2026-09-17, n=2]`. Backup of the key exported on RTX (`dxmd_graphics_backup_2026-09-17.reg`, session scratchpad).
- **Driving it:** Launcher: click **Play** (≈ 345, 40 launcher-image px ×1.79 from the launcher's top-left on RTX). In game, `WM_CLOSE` opens `Quit game? Yes/No`; click Yes. ⚠️ `WM_CLOSE` alone does not close it — check the process is gone before relaunching.
- **Dead ends:** `WM_CLOSE` does not exit the game by itself (it only opens the quit prompt) `[verified-live 2026-09-17, n=2]`.

**⭐ 2026-10-15 (dev PC, `/pd`, no launch) — THE GAME HAS ITS OWN STEREO 3D, INCLUDING SIDE-BY-SIDE** `[inferred-static 2026-10-15]`, all from strings and the registry, no code read (it is packed):
- Three vendor paths: NVIDIA 3D Vision (`NvAPI_Stereo_*`, `NVIDIA Stereo message recieved: activated=%u separation=%f`), AMD HD3D quad-buffer stereo, and a **side-by-side mode** (the 3D-TV kind, no special hardware): `Disabling side-by-side stereoscopic 3d mode, we're running in windowed mode.` / `..., multi-monitor is active.`
- Menu entries `ui_text_menu_stereoscopic_3d`, `_stereo_separation`, `_stereo_popout`; choices listed as off / sidebyside / on.
- Registry `HKCU\Software\Eidos Montreal\Deus Ex: MD\Graphics` (dev PC, read only): `Stereoscopic3DMode` 0, `StereoSeparation` 75, `StereoPopOut` 250, `StereoNearSeparationMultiplier` 350, `Stereoscopic3DAMDSwapEyes` 0. Which number means side-by-side is NOT known; the string order suggests 0 off, 1 side-by-side, 2 vendor `[hypothesis]`. The other three are probably hundredths (0.75, 2.5, 3.5) `[hypothesis]`.
- Conditions it logs: v-sync must be on (it turns it on), exclusive fullscreen must be on in DX11, not supported for DX12 on NVIDIA, side-by-side refuses windowed mode and multi-monitor.
- Why it matters: if side-by-side draws each eye with its own camera (a real per-eye projection, as 3D Vision games do), the engine already does the hardest VR step. The windowed refusal is the first wall (our window rule); a patch needs the code, so the memory image first.
- Also in the exe: `FOVCorrection` (registry, 1000 on the dev PC, probably x1000), `CameraFOV`, `ZCameraModifier_FieldOfView_Base`.

**Screen effects (VR rule): the switches** `[inferred-static 2026-10-15]` (dev PC registry, same key; values today): `MotionBlur` 0 (off already), `DOFQuality` 1, `ChromaticAberration` 1, `Bloom` 1, `LensFlares` 1, `Sharpen` 1, `TAA` 1, `VolumetricLighting` 2. For VR: `MotionBlur`, `DOFQuality`, `ChromaticAberration`, `LensFlares` to 0. The vignette (`ZPostfilterVignetteAspect`, and a `damageVignette_mc` UI element = the damage tint) and the eye-augmentation screen overlays have no registry switch seen; they need the code or the post-filter entities.

**✅ 2026-10-15 (dev PC, `/lm`): windowed and muted.** Same registry values as the home PC give a 1280x720 client while the desktop stays 1920x1080 `[verified-live 2026-10-15, n=2]` (key exported first). Music 0 % via OPTIONS -> AUDIO, stored in the game's `game_options.bin` `[verified-live 2026-10-15, n=1]`. `-nolauncher` goes straight to the menu `[verified-live 2026-10-15, n=3]`.

**⭐⭐ 2026-10-15 (dev PC, `/lm`): `Stereoscopic3DMode` 1 = side-by-side, and it draws a real picture per eye** `[verified-live 2026-10-15, n=1]`. With `Fullscreen` 1 and `ExclusiveFullscreen` 1 (separation 75, pop-out 250, near multiplier 350 as shipped) the menu and gameplay show as two squeezed pictures. Offset between the halves in one gameplay frame `[measured 2026-10-15, n=1 frame]`: far scene 71 px, nearer ground 70 down to 66 px, gun and hand 30 px, display 0 px (960-px halves). Offset changing with distance = two cameras, not a copy. It ran at 1920x1080 despite `FullscreenWidth`/`Height` 1280x720, started minimised, mouse clicks missed in its menus (keyboard fine). Unknown: own lens per eye or only a shifted camera; separation in metres. Evidence: `dev-archive/recon/2026-10-15-lm-windowed-side-by-side-camera/`.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?: **deferred contexts, heavily**: in gameplay about 200,000 deferred draws and 2,000 `ExecuteCommandList` per 5 s against 75,000 immediate, 8-9 contexts `[measured 2026-10-15, n=1 run]`.
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**: **camera-relative view-projection in vertex-shader
  constant buffers** `[verified-live 2026-10-15, n=1 run, 130+ scans]`, found by shape (no names: the camera shaders
  are among the 565 stripped; 147 kept names):
  - `b0 @0`, 544-byte buffer, columns: view-projection with the camera at the origin; the most used (600-1,500 per scan).
  - `b1 @0`, 144-byte buffer, columns: the same camera in **world space**; `b1 @64` the camera-relative one again.
  - `b11 @32`, 336-byte buffer: world space, seen less.
  - `b1 @0` followed the player: still while standing; a mouse turn swung forward from (-0.22, 0.94) to (0.97, 0.03) and (0.84, -0.49); 2 s of walking moved it about 3 units along the heading `[verified-live 2026-10-15, n=1]`. Forward Z stayed -0.249 through the turn: **Z up** `[inferred-static 2026-10-15]`. Units probably metres `[hypothesis]`.
  - Picture shape 1.777, lens 1.092 x 1.940 (about 85 x 55 degrees) at 1280x720.
  - So a per-eye shift goes into the camera-relative matrix (`b0`, and `b1 @64`), not into a world position.
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from:
- The per-eye override maths (`K_eye = …`):
- **2026-10-15 /pd: a camera finder is built, not yet run** `[compile-verified 2026-10-15]`. The shader variable
  names are unknown, so `staging/deus-ex-mankind-divided-vr/proxy-d3d11-camlog/` (a `d3d11.dll` proxy, 64-bit,
  d3d11.dll `9a90a0264f01`) recognises a camera by SHAPE: any 4x4 block in a vertex-shader constant buffer that is
  a perspective view*projection (forward row unit length, right/up/forward at right angles, aspect from the row
  lengths), both memory layouts, and solves the camera position from it. Where the shader keeps its reflection it
  also names the variable (`Frame.gViewProj+0`). Tested without the game: 120,009 synthetic cameras
  `[verified-numerically 2026-10-15, n=20000]`, planted sign mistake caught; and an end-to-end WARP run through the
  built DLL `[verified-numerically 2026-10-15, n=1]`. Present is not hooked (d3d11 only). Log: `dxmd_camlog.txt`
  next to the exe. Whether DXMD's shaders keep their names is unknown `[hypothesis]`.

## 7. Constant-buffer fill mechanism
- Map/DISCARD ring / UpdateSubresource / D3D11.1 offset / **persistent map +
  memcpy** (trap):
- Can source contents be read cheaply (captured CPU pointer) or need staging
  read-back?:
- The chosen override patch point and why:

## 8. Pass inventory (by render target)
- Main scene (res/formats):
- Shadow passes (depth-only sizes):
- Post / AA chain (SMAA/TAA/motion vectors; downscale sizes):
- UI / HUD (how it's kept separate):

## 9. cvar / console cheat sheet
| command / cvar | effect | use |
|---|---|---|
| | | |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene (commands used):
- In-process input / camera drive method that worked:
- Frame-capture method; where images land:
- **Camera-finder run (done 2026-10-15, see §6):** copy `build/d3d11.dll` from the folder above into `retail\`
  (no d3d11.dll there today), start windowed with `-nolauncher`, stand still in gameplay for 10 s, then turn the
  mouse; close; read `retail\dxmd_camlog.txt`. Take the dll out again after. Outcome table: that folder's README.

## 11. Dead ends & false leads (save future time)
- Reading the exe's code straight off disk: the code section is empty or encrypted on disk (§3) `[inferred-static 2026-10-15]`.
- Reading the unpacked code from a memory image: closed (copy protection; §3). Use the graphics side.

## 12. Open risks toward the North Star
- ✅ Installed on both PCs (dev PC since at least 2026-10-15).
- ⚠️ The code is packed at rest and the memory-image route is closed (§3): code questions (the windowed refusal of side-by-side, the stereo values) must be answered from the outside, through the graphics calls.
- ⚠️ If Denuvo is still present, attaching a debugger and injecting code both get much harder `[hypothesis]`.

## Inbox folds, 2026-09-29

**Recon logs were silently ignored (`/gs` 2026-09-23): fixed 2026-09-29.** `.gitignore` now keeps `dev-archive/recon/**/*.log`.


## Inbox folds, 2026-10-15

- `2026-10-04-gr-steam-kept-denuvo-in-2020-gog-is-drm-free.md` (`/gr`): Denuvo still on the Steam build in 2020, GOG
  never had it `[reported 2020-04-29]`. Folded into §4; the packed layout found the same day (§3) fits it.

## Inbox folds, 2026-10-15 (`/lm`)

- `2026-10-15-lm-reader-outside-memory-image-tool.md` (the `/lm` reader): the outside read-only `memdump.py`, tested
  on notepad, explorer and a guarded test process. Used live the same evening (§3): the image was taken, reading into
  it was then stopped and that route closed.
