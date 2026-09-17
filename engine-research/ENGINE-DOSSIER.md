# Engine Dossier — Deus Ex: Mankind Divided (Dawn Engine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, repo created (2026-09-15); the game is still downloading, so nothing has been read from it yet. · **VR-readiness verdict:** TBD.

## 1. Identity
- Game / build / version: Deus Ex: Mankind Divided, Steam build (app 337000). **Still downloading** on the home PC (about 1% on 2026-09-15); no files on disk yet.
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: Eidos-Montréal's **Dawn Engine**, derived from IO Interactive's Glacier 2 `[reported]`. Unchecked against the binary.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.):
- Distinctive file formats / build tags / symbol naming: —

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): not yet looked at — nothing installed.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: Direct3D 11, with a Direct3D 12 mode added after release `[reported]`. Unchecked.
- Developer console / cvar system present? how opened?: not yet investigated.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: Shipped with Denuvo in 2016 `[reported]`; whether the current Steam build still carries it is unchecked.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

**🎮 2026-09-17 (home PC `RTX`, `/lm`) — FIRST LIVE LOOK.**
- **Runs:** Steam launch opens a small in-exe launcher (Play / Options / Website / … / Quit); **Play** reaches the main menu (STORY / BREACH / JENSEN'S STORIES / EXTRAS / OPTIONS / SHOP / SQUARE ENIX / QUIT), build `v1.19 build 801.0` `[verified-live 2026-09-17, n=2]`.
- **With our file added:** A 64-bit `dxgi.dll` proxy in `retail\` loads and the game reaches the main menu `[verified-live 2026-09-17, n=1]`. Calls seen: `SetAppCompatStringPointer` (see below), `CreateDXGIFactory2`, `CompatValue`, `CreateDXGIFactory`. **Windows' app-compat shim (`AcGenral.dll`) calls dxgi's `SetAppCompatStringPointer` before our `DllMain` runs**, and loading the real dxgi at that moment fails (error 1168); the generator now answers that one early call with 0 and loads the real dll a moment later `[verified-live 2026-09-17, n=1]`. Found on Prey, the same thing happens here. The proxy comes from the shared generator `staging/_shared/proxy-gen/` (every export of the real system dll re-exported with the same ordinals; first call of each export logged). 
- **Windowed (for measuring; 1280×720 keeps aspect-keyed numbers the same on both PCs):** Registry `HKCU\Software\Eidos Montreal\Deus Ex: MD\Graphics`: `Fullscreen=0`, `WindowWidth`/`UserWindowWidth=1280`, `WindowHeight`/`UserWindowHeight=720` → 1280×720 client window `[verified-live 2026-09-17, n=2]`. Backup of the key exported on RTX (`dxmd_graphics_backup_2026-09-17.reg`, session scratchpad).
- **Driving it:** Launcher: click **Play** (≈ 345, 40 launcher-image px ×1.79 from the launcher's top-left on RTX). In game, `WM_CLOSE` opens `Quit game? Yes/No`; click Yes. ⚠️ `WM_CLOSE` alone does not close it — check the process is gone before relaunching.
- **Dead ends:** `WM_CLOSE` does not exit the game by itself (it only opens the quit prompt) `[verified-live 2026-09-17, n=2]`.

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
- none yet.

## 12. Open risks toward the North Star
- ⚠️ Not installed yet — no static work is possible until the download finishes.
- ⚠️ If Denuvo is still present, attaching a debugger and injecting code both get much harder `[hypothesis]`.
