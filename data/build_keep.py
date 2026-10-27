import json, zipfile, collections, re
W="/home/hatch/workspace/haxiuz-data/work/"
opened=set()
for f in ["opened.json","opened-sdl.json","opened-menu-sdl.json"]:
    opened |= set(json.load(open(W+f)))
opened={o for o in opened if not o.endswith("/")}
print("union opened files:", len(opened))
z=zipfile.ZipFile("/home/hatch/workspace/thisissparta2/server/data/data20091001.pk3")
sizes={i.filename:i.file_size for i in z.infolist() if not i.filename.endswith("/")}
names=set(sizes)
def sz(s): return sum(sizes.get(f,0) for f in s)
print("union opened size: %.1f MB"%(sz(opened)/1048576))
keep=set(opened)
rules=collections.Counter()
def add(f, why):
    if f in names and f not in keep: keep.add(f); rules[why]+=1
# 1. root configs/text
for f in names:
    if "/" not in f and (f.endswith((".cfg",".txt",".rc",".db"))): add(f,"root cfg/txt")
# 2. all scripts + particles
for f in names:
    if f.startswith("scripts/") or f.startswith("particles/"): add(f,"scripts/particles all")
# 3. model companions: same dir, stem prefix
for f in list(opened):
    if f.startswith("models/"):
        stem=f.rsplit(".",1)[0]
        for g in names:
            if g.startswith(stem) and g!=f: add(g,"model companion")
# also whole models/player dir (session opened every player model)
for f in names:
    if f.startswith("models/player/"): add(f,"models/player all")
# 4. texture variants: same stem, any suffix file in same dir
for f in list(opened):
    if f.startswith("textures/"):
        stem=f.rsplit(".",1)[0]
        for g in names:
            if g.rsplit(".",1)[0]==stem or g.startswith(stem+"_"): add(g,"texture variant")
# 5. sound randomized variants: same dir + stem-with-trailing-digits-stripped prefix
for f in list(opened):
    if f.startswith("sound/") and "." in f:
        d=f.rsplit("/",1)[0]; stem=f.rsplit("/",1)[1].rsplit(".",1)[0]
        base=re.sub(r"\d+$","",stem)
        if base:
            for g in names:
                if g.startswith(d+"/"):
                    gst=g.rsplit("/",1)[1].rsplit(".",1)[0]
                    if re.sub(r"\d+$","",gst)==base: add(g,"sound variant")
# 6. gfx: siblings in any gfx dir that has an opened file (fonts/hud completeness)
gfxdirs={f.rsplit("/",1)[0] for f in opened if f.startswith("gfx/")}
for f in names:
    if f.startswith("gfx/") and f.rsplit("/",1)[0] in gfxdirs: add(f,"gfx sibling")
# 7. evilspace map files all
for f in names:
    if f.startswith("maps/evilspace") : add(f,"evilspace")
# 8. spog merge (from common-spog.pk3)
z2=zipfile.ZipFile("/home/hatch/workspace/thisissparta2/server/data/common-spog.pk3")
spog=[i.filename for i in z2.infolist() if not i.filename.endswith("/")]
print("keep total: %d files, %.1f MB uncompressed"%(len(keep), sz(keep)/1048576))
print(rules)
bytop=collections.Counter(); bytopn=collections.Counter()
for f in keep: bytop[f.split("/")[0]]+=sizes.get(f,0); bytopn[f.split("/")[0]]+=1
for k,v in bytop.most_common(15): print(f"  {v/1048576:8.1f} MB {bytopn[k]:5d}  {k}")
json.dump(sorted(keep), open(W+"keep.json","w"), indent=0)
json.dump(spog, open(W+"spog.json","w"), indent=0)
# what player models cost
pm=[f for f in keep if f.startswith("models/player/")]
print("models/player kept: %d files %.1f MB"%(len(pm), sz(pm)/1048576))
oth=[f for f in keep if f.startswith("models/") and not f.startswith("models/player/")]
print("other models kept: %d files %.1f MB"%(len(oth), sz(oth)/1048576))
