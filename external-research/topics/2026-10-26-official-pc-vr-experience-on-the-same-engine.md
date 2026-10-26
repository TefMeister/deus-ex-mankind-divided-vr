# The official, free "Mankind Divided - VR Experience" (2017) is a PC VR build on the same engine

**Status:** 🆕 new · **Priority:** medium-high. It is most likely what the main game's hidden `-vrdemo` switch and
its `98_vr/98_vr_master.entity` scene belong to, and it is a working Dawn Engine VR renderer from Eidos itself.

## What is public

- **Steam app 526180, "Deus Ex: Mankind Divided™ - VR Experience"**, released **24 January 2017**, **free**, Windows
  64-bit, store categories "VR Supported", "Tracked Controller Support", "Full controller support"; listed VR
  support: **"SteamVR or Oculus PC"**; 9 GB `[reported 2026-10-26, Steam store API]`. Store text: "Discover four
  iconic environments from Deus Ex: Mankind Divided, for the first time in virtual reality."
- Road to VR (Paul James, 28 Jan 2017): a walk through several of the full game's locations, full locomotion (no
  teleport), snap turning, motion controllers or an Xbox pad, ran "very well on the Oculus Rift"; it does not need
  any Deus Ex game to be owned `[reported 2017-01-28]`.
- The fan wiki describes it as a technology demo for HTC Vive, Oculus Rift and OSVR `[reported]` (page not
  fetchable by the automated reader; seen in a search snippet only).
- A side-by-side VR community guide (360900/tinkergame wiki) says the main game's built-in Stereo3D mode "kind of
  worked" in a headset "but was distorted" `[reported]`.
- No fan VR mod for Mankind Divided was found; DeusExHRVR remains Human Revolution only `[reported 2026-10-26, n=1 search]`.

## Why it matters here

1. **The `-vrdemo` row.** Our 2026-10-15 static look guessed the switch was "the 2016 PlayStation VR demo's
   leftovers". The PC VR Experience is a more likely owner: same studio, same season, same "four environments"
   shape `[hypothesis]`. If so, the main exe carries some of the demo's code path but not its headset runtime (the
   dossier found no headset runtime named in the exe).
2. **A working Dawn Engine VR renderer to look at, legally free.** Installing it is installing an official free
   game, not studying someone's mod. Its program would show, from the outside, how Dawn draws per eye for a real
   headset: which runtime DLLs it loads (SteamVR / Oculus), the per-eye constant buffers, and whether its stereo is
   the same mechanism as the side-by-side mode the main game already has `[hypothesis]`.
3. **The packed-code dead end.** The main game's code is packed at rest (dossier §3, §11). Whether the VR
   Experience is packed too is unknown; if it is not, its code could answer stereo questions the main exe cannot
   `[hypothesis, unchecked]`.

## Next step it unlocks

Install Steam app 526180 on one PC (free, 9 GB), then, with no game running: list its DLL imports and sections
(packed or not), and compare its scene names with `98_vr/98_vr_master.entity` in the main game.

## Sources

- Steam store, app 526180: <https://store.steampowered.com/app/526180/>
- Road to VR, "Deus Ex: Mankind Divided's Free VR Experience is a Beautiful Glimpse at the Future": <https://roadtovr.com/deus-ex-mankind-divideds-free-vr-experience-is-a-beautiful-glimpse-at-the-future/>
- Deus Ex fan wiki (Fandom), "Deus Ex: Mankind Divided - VR Experience": <https://deusex.fandom.com/wiki/Deus_Ex:_Mankind_Divided_-_VR_Experience>
- 360900, tinkergame wiki "Side by Side VR": <https://github.com/360900/tinkergame/wiki/Side-by-Side-VR>
