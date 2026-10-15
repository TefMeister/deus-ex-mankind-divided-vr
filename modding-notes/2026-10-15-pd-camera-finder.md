# 2026-10-15 (dev PC, /pd, no launch): a camera finder that needs no names

**What it is.** A small `d3d11.dll` that sits beside the game and watches what the game sends to the graphics card.
Every two seconds, for a quarter of a second, it looks through the numbers each vertex shader is given and picks out
the ones that have the exact shape of a camera (a view and lens combined). When it finds one it writes down where
it was (which buffer slot, which byte), where the camera stands, which way it faces and how wide the picture is.
If the game's shaders still carry their own variable names, it writes the name too.

**Why shape and not name.** For Burnout we knew the name of the camera variable before writing the logger. Here we
know nothing about the shaders yet, and the code is packed, so a finder that recognises a camera by its maths is
the cheapest way in.

**How sure.** Built and tested without the game `[compile-verified 2026-10-15]`:
- 20,000 made-up cameras (random place, heading, lens, both storage layouts, normal and reversed depth, small
  jitter) all come back with the right place and heading `[verified-numerically 2026-10-15, n=20000]`; a planted
  sign mistake makes 20,000 checks fail, so the test can fail.
- Cube-map faces, shadow passes, plain object matrices, zeros and NaN are all refused.
- The shader-name reader is checked against a shader compiled here with known names; a stripped one gives nothing.
- End to end: a small program loads the built dll, draws with the software renderer, and the log names the camera at
  `12.000 1.700 -30.000` and `Frame.gViewProj+0` `[verified-numerically 2026-10-15, n=1]`.

**Not deployed on purpose**: the game folder stays plain for the side-by-side 3D test, which comes first.

**What it does NOT do:** it does not hook the picture swap (Present), and it changes nothing the game draws.

Source, build and outcome table: `staging/deus-ex-mankind-divided-vr/proxy-d3d11-camlog/` (private).
