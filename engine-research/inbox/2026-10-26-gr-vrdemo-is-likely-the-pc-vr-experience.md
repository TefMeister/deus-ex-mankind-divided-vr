# `-vrdemo` most likely belongs to the free PC "VR Experience" (Steam 526180), not a PlayStation VR demo

From: `/gr`, 2026-10-26 (estate sweep, CHECK-IN). Topic: `external-research/topics/2026-10-26-official-pc-vr-experience-on-the-same-engine.md`.

**What it answers:** the board's `[FLAT]` `-vrdemo` row and `modding-notes/2026-10-15-pd-first-static-look-...md`
item 4: "A hidden `-vrdemo` switch loads a scene `98_vr/98_vr_master.entity` ... most likely the 2016 PlayStation
VR demo's leftovers."

Eidos released **Deus Ex: Mankind Divided - VR Experience** free on Steam (app 526180, 24 Jan 2017, Windows, "SteamVR
or Oculus PC", four environments from the game) `[reported 2026-10-26, Steam store API]`. Same studio and engine,
so it is the likelier owner of `-vrdemo` `[hypothesis]`.

**It also touches §11/§12 (packed code closes the memory-image route):** the VR Experience is a working Dawn Engine
VR renderer that may not be packed `[hypothesis, unchecked]`; inspecting it from outside could answer how Dawn draws
per eye for a headset.

**Suggested dossier change:** in §4/§12 replace the PlayStation VR guess with this, tagged `[hypothesis]`, and
consider a `[USER]` row "install Steam app 526180 (free)" followed by a `[PD]` row "imports, sections, scene names".
