# 2026-10-15 (/lm reader, dev PC, game not touched): a read-only outside memory-image tool for DXMD

For: dossier §3 ("Static code reading needs a memory image of the running process").

- **The Manhunt way was an inside job:** Manhunt's 32-bit d3d8 proxy wrote `manhunt_module_unpacked.bin` from
  inside the game (`dump_full_module_image` in `staging/manhunt-2003-vr/proxy-d3d8/src/proxy.c`), a flat image where
  file offset = address minus base, read by `flat-to-vr-RE-toolkit/tools/static-disasm.py --raw` `[inferred-static]`.
  There was no outside 64-bit dumper anywhere in the estate.
- **New: `staging/deus-ex-mankind-divided-vr/memdump/memdump.py`**, run from OUTSIDE the game with query + read
  access only. Same flat layout as Manhunt's, and the header is also fixed up into a loadable PE at the runtime base
  (raw offsets = RVAs, relocations cleared), plus a `.map.txt` with live page protections, the non-zero share of each
  section (the "did `.trace` really fill" check) and every range it did not read. Refuses to write inside a git tree
  or the game folder `[compile-verified 2026-10-15]`.
- **Tested without the game** `[measured 2026-10-15, n=3]`: notepad (code bytes identical to disk, imports parse,
  `static-disasm.py` reads it in both `--raw` and PE mode), explorer (5.8 MB, no unread ranges), and a Python child
  with one no-access and one guarded page of its own image (both skipped, listed, not touched).
- **Command for the live session:** `python -I memdump.py --name DXMD.exe --out "<folder outside every repo and the
  game folder>" --tag gameplay`, taken in gameplay. Whether Denuvo blocks an outside read handle is untested
  `[hypothesis]`; if it does, the map or the error says so and the Manhunt inside route (from the camera-finder
  d3d11 proxy) is the fallback.
