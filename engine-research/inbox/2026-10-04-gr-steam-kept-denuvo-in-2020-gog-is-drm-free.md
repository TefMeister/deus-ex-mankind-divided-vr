# Denuvo: the Steam build still had it in 2020; the GOG build has never had it

From: `/gr`, 2026-10-04. For dossier §1 ("whether the current Steam build still carries it is unchecked") and the
`[PD]` first-static-look row (the `.xtext/.sdata/.link/.trace` sections).

- DSOGaming, 2020-04-29: the GOG release is DRM-free and has no Denuvo; Square Enix had **not** removed Denuvo from
  the Steam version and had said nothing about doing so `[reported 2020-04-29]`. KitGuru reported the same, and that
  GOG ships the unprotected binary with a Steam-to-GOG bridge layer added `[reported]`.
- Nothing newer found that says the Steam build was patched since. So "Denuvo still present on Steam" is the
  working assumption `[hypothesis]`; the unusual sections our static look found fit that.
- **Why it matters:** if Denuvo is there, debugger attach and code injection on the Steam build are much harder (§
  risks). A GOG copy would be the clean binary for the same game. Buying it is Tefa's call, not a research one;
  this only records that the option exists.
- Sources: <https://www.dsogaming.com/?p=138223>, <https://www.kitguru.net/?p=464857>.
