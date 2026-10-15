"""First static look at DXMD.exe: header, sections (with entropy), imports, version, telling strings. Read-only."""
import sys, math, re, collections, hashlib, pefile

path = sys.argv[1]
data = open(path, "rb").read()
pe = pefile.PE(data=data, fast_load=False)
print("sha256", hashlib.sha256(data).hexdigest()[:12], "size", len(data))
print("machine", hex(pe.FILE_HEADER.Machine), "timestamp", pe.FILE_HEADER.TimeDateStamp,
      "imagebase", hex(pe.OPTIONAL_HEADER.ImageBase), "entry", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
      "dllchar", hex(pe.OPTIONAL_HEADER.DllCharacteristics))
import datetime
print("link date", datetime.datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp, datetime.timezone.utc))
ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
for s in pe.sections:
    name = s.Name.rstrip(b"\0").decode(errors="replace")
    raw = s.get_data()
    c = collections.Counter(raw)
    ent = -sum(v / len(raw) * math.log2(v / len(raw)) for v in c.values()) if raw else 0
    has_ep = s.VirtualAddress <= ep < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData)
    print(f"  {name:8s} va {s.VirtualAddress:#010x} vsize {s.Misc_VirtualSize:#010x} raw {s.SizeOfRawData:#010x} "
          f"ent {ent:.2f} chr {s.Characteristics:#010x}{'  <- entry point' if has_ep else ''}")
if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
    for imp in pe.DIRECTORY_ENTRY_IMPORT:
        names = [i.name.decode() if i.name else f"#{i.ordinal}" for i in imp.imports]
        print("import", imp.dll.decode(), len(names), ", ".join(names[:12]) + (" ..." if len(names) > 12 else ""))
if hasattr(pe, "VS_FIXEDFILEINFO"):
    for fi in getattr(pe, "FileInfo", []):
        for e in fi:
            for st in getattr(e, "StringTable", []):
                for k, v in st.entries.items():
                    print("ver", k.decode(), "=", v.decode(errors="replace"))
pats = [rb"denuvo", rb"Denuvo", rb"d3d11\.dll", rb"d3d12\.dll", rb"D3D12CreateDevice", rb"D3D11CreateDevice",
        rb"dxgi\.dll", rb"openvr", rb"OpenVR", rb"oculus", rb"Oculus", rb"stereo", rb"Stereo", rb"nvapi", rb"NvAPI",
        rb"AGS", rb"-dx12", rb"dx12", rb"DX12", rb"Glacier", rb"Dawn", rb"console", rb"Console", rb"cheat",
        rb"fov", rb"FOV", rb"FieldOfView", rb"MotionBlur", rb"DepthOfField", rb"ChromaticAberration",
        rb"FilmGrain", rb"Vignette", rb"Bloom", rb"LensFlare", rb"Sharpen", rb"TemporalAA", rb"ShadowQuality",
        rb"CommandLine", rb"Fullscreen", rb"WindowWidth", rb"Eidos Montreal"]
for p in pats:
    hits = [m.start() for m in re.finditer(p, data)]
    if hits:
        samples = []
        for h in hits[:4]:
            a = h
            while a > 0 and 32 <= data[a - 1] < 127 and h - a < 60: a -= 1
            b = h
            while b < len(data) and 32 <= data[b] < 127 and b - h < 80: b += 1
            samples.append(data[a:b].decode(errors="replace"))
        print(f"str {p.decode():22s} {len(hits):5d}  e.g. {samples}")
