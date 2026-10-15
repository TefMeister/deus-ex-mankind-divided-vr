# 2026-10-15 `/lm` (dev PC): windowed, side-by-side 3D, the camera finder

Note: `modding-notes/2026-10-15-lm-windowed-side-by-side-and-the-camera.md`.

| File | What it is |
| --- | --- |
| `side-by-side-menu.jpg`, `side-by-side-gameplay.jpg` | the game's own side-by-side 3D (`Stereoscopic3DMode` 1), scaled to 1280x720 |
| `sbs_offset.py` | measures the left/right offset between the two halves (run on the full 1920x1080 screenshot) |
| `windowed-gameplay-1280x720.jpg` | the windowed game in gameplay, with the camera finder loaded |
| `dxmd_camlog.txt` | the camera finder's log: stand 19:53:30-44, turn 19:53:44-51, walk 19:53:51-53 |
| `dxmd_vr_proxy_log.txt` | the proxy's own start-up log |
| `d3d11.dll` (local only: dlls are not committed here) | the camera finder build, sha256 `9a90a0264f01`, taken out of the game folder after the run; the same build and its source are in `staging/deus-ex-mankind-divided-vr/proxy-d3d11-camlog/` |
