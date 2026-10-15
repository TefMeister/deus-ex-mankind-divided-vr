# 2026-10-15 (`/pd`, dev PC, no launch): first static look at DXMD.exe on the dev PC

The game was not launched. Everything here was read from `retail\DXMD.exe` (Steam build id 3355064, file version
1.19, sha256 `73af0e3f28fc`) and the game's registry key, read only. Write-up:
`modding-notes/2026-10-15-pd-first-static-look-packed-code-and-native-stereo.md`; dossier §1-4.

| file | what |
| --- | --- |
| `pe-sections-imports-strings.txt` | header, sections with entropy, imports, version, telling strings (`dxmd_pe.py`) |
| `stereo-console-effects-strings.txt` | every stereo, VR-demo, console, switch and post-effect string (`dxmd_strings.py`) |
| `no-code-refs-on-disk.txt` | no RIP-relative reference to the stereo strings in the on-disk bytes (`dxmd_riprefs.py`) |
| `registry-graphics-dev-pc.txt` | `HKCU\Software\Eidos Montreal\Deus Ex: MD\Graphics` on the dev PC |

Re-run: `python -I dxmd_pe.py <DXMD.exe>`; `python -I dxmd_strings.py <DXMD.exe> "<regex>"`;
`python -I dxmd_riprefs.py <DXMD.exe> "<string>" ...`. Needs `pefile`.
