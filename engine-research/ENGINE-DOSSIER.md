# Engine Dossier — Deus Ex: Mankind Divided (Dawn Engine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M1, first static look done on the dev PC (2026-10-15): the code is packed at rest, and the game has its own side-by-side stereo 3D mode. · **VR-readiness verdict:** promising (a native two-eye mode exists), unproven.

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
- ⚠️ **The code is packed at rest** `[inferred-static 2026-10-15]`: `.trace` is 25 MB of address space with NO bytes on disk, `.sdata` is 80 MB at entropy 7.96 (encrypted or compressed), `.text` is 61 % zeros on disk, the entry point sits in a tiny section named `.reloc`, and `.xtext` (1.3 MB) is the unpacker. Not one RIP-relative reference to the settings strings exists in the on-disk bytes, so the real code is written into `.trace` at start-up. Matches Denuvo still being on the Steam build `[hypothesis]` (see §4). **Static code reading needs a memory image of the running process** (the Manhunt method: `static-disasm.py --raw`).
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: **Direct3D 11 by default, Direct3D 12 by switch.** `d3d11.dll` and `d3d12.dll` are loaded at run time (`Loaded d3d11.dll`, `D3D12CreateDevice`), only `dxgi.dll!CreateDXGIFactory` is imported; registry `EnableDX12` (0 on the dev PC) `[inferred-static 2026-10-15]`. `D3DX11CompileFromMemory` is imported, so some shaders are compiled at run time.
- Developer console / cvar system present? how opened?: a `ConsoleCmd <name> <value>` mechanism exists (`Render_ShowDebug`, `EnableFpsString`, `MaxFPS`, `Breach_DisableChipsets`, `Render_ShowEntityDebug`), fed from `[assembly:/common/preinit.ini]` `[inferred-static 2026-10-15]`; whether a player-reachable console exists is unknown. Start-up switches: `-nolauncher` (skips the small launcher window: use it for driving), `-benchmark` (`benchmark.ini`), `-vrdemo` (loads `assembly:/scenes/game/98_vr/98_vr_master.entity`; with `LoadBenchmarkOrVRDemo` and `eGameInputFlags_BreachVR_*` input flags, likely the 2016 PlayStation VR demo's leftovers), `-nixxes`, `-nochroma`, `-forcepack` `[inferred-static 2026-10-15]`. No headset runtime (OpenVR, Oculus, PSVR) is named in the exe.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: Shipped with Denuvo in 2016 `[reported]`; still on the Steam build in 2020, and the GOG build never had it `[reported 2020-04-29]` (DSOGaming, KitGuru; `/gr` 2026-10-04). The packed layout in §3 fits it still being there `[hypothesis]`. A GOG copy would give a clean binary; buying it is Tefa's call.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

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

⚠️ **The dev PC is NOT windowed yet:** its registry says `Fullscreen` 1, `ExclusiveFullscreen` 1, 1920x1080 (only the home PC was set to 1280x720 on 2026-09-17). Set it the same way (backup first) before the first dev-PC launch.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**:
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from:
- The per-eye override maths (`K_eye = …`):

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

## 11. Dead ends & false leads (save future time)
- Reading the exe's code straight off disk: the code section is empty or encrypted on disk (§3) `[inferred-static 2026-10-15]`.

## 12. Open risks toward the North Star
- ✅ Installed on both PCs (dev PC since at least 2026-10-15).
- ⚠️ The code is packed at rest (§3): every code question waits for a memory image from a running game.
- ⚠️ If Denuvo is still present, attaching a debugger and injecting code both get much harder `[hypothesis]`.

## Inbox folds, 2026-09-29

**Recon logs were silently ignored (`/gs` 2026-09-23): fixed 2026-09-29.** `.gitignore` now keeps `dev-archive/recon/**/*.log`.


## Inbox folds, 2026-10-15

- `2026-10-04-gr-steam-kept-denuvo-in-2020-gog-is-drm-free.md` (`/gr`): Denuvo still on the Steam build in 2020, GOG
  never had it `[reported 2020-04-29]`. Folded into §4; the packed layout found the same day (§3) fits it.
