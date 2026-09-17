# 2026-09-17 — first live look: Deus Ex: Mankind Divided

Home PC `RTX`, `/lm` session. The user asked for a first look at six games: does each run, and does it still run with our own file added.

## Does it run?

Steam launch opens a small in-exe launcher (Play / Options / Website / … / Quit); **Play** reaches the main menu (STORY / BREACH / JENSEN'S STORIES / EXTRAS / OPTIONS / SHOP / SQUARE ENIX / QUIT), build `v1.19 build 801.0` `[verified-live 2026-09-17, n=2]`.

## With our file added

A 64-bit `dxgi.dll` proxy in `retail\` loads and the game reaches the main menu `[verified-live 2026-09-17, n=1]`. Calls seen: `SetAppCompatStringPointer` (see below), `CreateDXGIFactory2`, `CompatValue`, `CreateDXGIFactory`. **Windows' app-compat shim (`AcGenral.dll`) calls dxgi's `SetAppCompatStringPointer` before our `DllMain` runs**, and loading the real dxgi at that moment fails (error 1168); the generator now answers that one early call with 0 and loads the real dll a moment later `[verified-live 2026-09-17, n=1]`. Found on Prey, the same thing happens here. The proxy comes from the shared generator `staging/_shared/proxy-gen/` (every export of the real system dll re-exported with the same ordinals; first call of each export logged). 

## Windowed mode

Registry `HKCU\Software\Eidos Montreal\Deus Ex: MD\Graphics`: `Fullscreen=0`, `WindowWidth`/`UserWindowWidth=1280`, `WindowHeight`/`UserWindowHeight=720` → 1280×720 client window `[verified-live 2026-09-17, n=2]`. Backup of the key exported on RTX (`dxmd_graphics_backup_2026-09-17.reg`, session scratchpad).

## How it was driven

Launcher: click **Play** (≈ 345, 40 launcher-image px ×1.79 from the launcher's top-left on RTX). In game, `WM_CLOSE` opens `Quit game? Yes/No`; click Yes. ⚠️ `WM_CLOSE` alone does not close it — check the process is gone before relaunching.

## Dead ends

`WM_CLOSE` does not exit the game by itself (it only opens the quit prompt) `[verified-live 2026-09-17, n=2]`.

## Not established

- Nothing past the menus: no gameplay was loaded, no camera data read.
- Every result is from one machine (`RTX`, 21:9 desktop) on one day.

## Next

- [PD] first static look: bitness (64-bit confirmed), protection — the exe has `.xtext/.sdata/.link/.trace` sections, which looks like a protector, but no `denuvo` string was found `[inferred-static 2026-09-17]`; fill in dossier §1–4
- [PD] add a swap-chain `Present` + constant-buffer logger to the shared proxy generator (the same job as Burnout's, 64-bit path)
- [FLAT] run that logger windowed and read which cbuffer carries the camera
