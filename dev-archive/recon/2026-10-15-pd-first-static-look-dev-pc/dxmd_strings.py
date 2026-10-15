"""Print every printable string (ASCII and UTF-16) in a file that matches a regex. Read-only."""
import sys, re
path, pat = sys.argv[1], re.compile(sys.argv[2].encode(), re.I)
data = open(path, "rb").read()
seen = set()
for m in re.finditer(rb"[\x20-\x7e]{5,}", data):
    s = m.group()
    if pat.search(s) and s not in seen:
        seen.add(s); print(f"a {m.start():#010x} {s.decode()[:160]}")
for m in re.finditer(rb"(?:[\x20-\x7e]\x00){5,}", data):
    s = m.group().decode("utf-16le").encode()
    if pat.search(s) and s not in seen:
        seen.add(s); print(f"w {m.start():#010x} {s.decode()[:160]}")
