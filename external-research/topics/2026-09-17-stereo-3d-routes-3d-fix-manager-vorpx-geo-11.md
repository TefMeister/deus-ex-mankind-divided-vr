# Deus Ex: Mankind Divided has public stereo-3D routes: a DX12 3D launcher, vorpX and geo-11

**Status:** 🆕 new · **Priority:** medium.

## What is public

- **Helix Mod's 3D Fix Manager** added a special `start3d.exe` for Mankind Divided, described as a
  one-click way to play it "in DirectX 12 3D" `[reported]`. That implies the game has a stereo-3D path
  on its DirectX 12 renderer that an outside launcher can switch on `[hypothesis]`.
- **vorpX:** a March 2017 forum thread on "SBS stereo in virtual screen mode" reports Z-Normal 3D looking
  "almost as good as Geometry", and trouble selecting SBS content `[reported]`.
- **geo-11:** an MTBS3D thread titled "geo-11 Deus Ex Mankind Divided" exists; it returned HTTP 403 to
  automated fetch, so its contents are unread `[reported, title only]`.

## Why it matters here

1. If the game has its own side-by-side or 3D output (as the vorpX "SBS" thread and `start3d.exe`
   suggest), the renderer already produces two views, and finding that code path beats inventing one
   `[hypothesis]`.
2. The board's static rows (protection, cbuffer logger) are unaffected, but the logger should watch for a
   second view when 3D is on.

## Next step

Open the MTBS3D geo-11 thread and the 3D Fix Manager page in a browser to learn what `start3d.exe`
switches (a launch argument, a registry value, or a config file).

## Sources

- Helix Mod, 3D Fix Manager — <https://helixmod.blogspot.com/2017/05/3d-fix-manager.html>
- vorpX forum, "Deus Ex Mankind Divided SBS stereo in virtual screen mode" — <https://www.vorpx.com/forums/topic/deus-ex-mankind-divided-sbs-stereo-in-virtual-screen-mode/>
- MTBS3D, "geo-11 Deus Ex Mankind Divided" — <https://www.mtbs3d.com/phpbb/viewtopic.php?t=26274>
