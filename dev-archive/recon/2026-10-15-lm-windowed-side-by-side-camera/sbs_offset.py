import sys, numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert('L'), dtype=np.float32)
h, w = im.shape; L = im[:, :w//2]; R = im[:, w//2:]
def shift(y0, y1, x0, x1, rng=90):
    a = L[y0:y1, x0:x1]; best = None
    for d in range(-rng, rng+1):
        if x0+d < 0 or x1+d > R.shape[1]: continue
        b = R[y0:y1, x0+d:x1+d]
        aa = a - a.mean(); bb = b - b.mean()
        c = (aa*bb).sum() / (np.sqrt((aa*aa).sum()*(bb*bb).sum()) + 1e-6)
        if best is None or c > best[1]: best = (d, c)
    return best
for name, box in [("gun (near)", (560, 900, 440, 640)), ("crate left (mid)", (480, 620, 80, 260)),
                  ("plate (mid)", (560, 640, 700, 820)), ("far buildings", (200, 330, 400, 700)),
                  ("HUD ammo", (820, 960, 820, 940)), ("HUD portrait", (40, 200, 10, 90))]:
    print(name, shift(*box))
