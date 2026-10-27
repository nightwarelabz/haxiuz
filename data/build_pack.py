import json, zipfile, hashlib
W="/home/hatch/workspace/haxiuz-data/work/"
keep=json.load(open(W+"keep.json"))
z=zipfile.ZipFile("/home/hatch/workspace/thisissparta2/server/data/data20091001.pk3")
names={i.filename:i for i in z.infolist() if not i.filename.endswith("/")}
missing=[f for f in keep if f not in names]
print("keep entries not in stock pk3 (dropped):", missing)
final=[f for f in keep if f in names]
spogz=zipfile.ZipFile("/home/hatch/workspace/thisissparta2/server/data/common-spog.pk3")
spog=[i.filename for i in spogz.infolist() if not i.filename.endswith("/")]
out="/home/hatch/workspace/haxiuz-data/haxiuz.pk3"
zo=zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9)
manifest=[]
for f in sorted(final):
    data=z.read(f)
    zo.writestr(f, data, zipfile.ZIP_DEFLATED, 9)
    manifest.append((f, len(data)))
for f in sorted(spog):
    data=spogz.read(f)
    zo.writestr(f, data, zipfile.ZIP_DEFLATED, 9)
    manifest.append((f, len(data)))
zo.close()
import os
raw=open(out,"rb").read()
print("pack files:", len(manifest), "uncompressed:", sum(s for _,s in manifest))
print("pack bytes:", len(raw), "sha256:", hashlib.sha256(raw).hexdigest())
with open("/home/hatch/workspace/haxiuz-data/manifest.txt","w") as fh:
    fh.write("# haxiuz.pk3 — stripped Nexuiz 2.5.2 client data for the haxiuz session\n")
    fh.write("# files: %d  uncompressed: %d  pk3 bytes: %d\n"%(len(manifest), sum(s for _,s in manifest), len(raw)))
    fh.write("# sha256: %s\n"%hashlib.sha256(raw).hexdigest())
    for f,s in manifest: fh.write("%10d  %s\n"%(s,f))
json.dump({"files":len(manifest),"uncompressed":sum(s for _,s in manifest),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"filelist":[f for f,_ in manifest]}, open("/home/hatch/workspace/haxiuz-data/manifest.json","w"), indent=1)
