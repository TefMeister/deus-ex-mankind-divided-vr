"""Find RIP-relative LEA references (48/4C 8D modrm=rip) to given strings, in every section's ON-DISK bytes. Read-only.
Also reports how much of each code section is all-zero on disk (code unpacked only at run time)."""
import sys, re, pefile
path = sys.argv[1]
targets = [t.encode() for t in sys.argv[2:]]
data = open(path, "rb").read()
pe = pefile.PE(data=data, fast_load=True)
want = {}
for t in targets:
    for m in re.finditer(re.escape(t) + b"\x00", data):
        rva = pe.get_rva_from_offset(m.start())
        if rva is not None: want[rva] = t.decode()
print("string RVAs:", {hex(k): v for k, v in want.items()})
for s in pe.sections:
    name = s.Name.rstrip(b"\0").decode(errors="replace")
    raw = s.get_data()
    if not raw: continue
    zero = raw.count(0) / len(raw)
    hits = 0
    for i in range(len(raw) - 7):
        if raw[i] in (0x48, 0x4C) and raw[i + 1] == 0x8D and (raw[i + 2] & 0xC7) == 0x05:
            disp = int.from_bytes(raw[i + 3:i + 7], "little", signed=True)
            tgt = s.VirtualAddress + i + 7 + disp
            if tgt in want:
                hits += 1
                print(f"  {name} rva {s.VirtualAddress + i:#x} -> {want[tgt]}")
    print(f"{name:8s} raw {len(raw):#x}  zero bytes {zero:.0%}  string refs {hits}")
