# Manifest format

The stripped data set's manifest is a plain-text file,
`manifest.txt`, one entry per line, UTF-8, LF line endings, sorted
by path. It is written to be diffed and grepped, not parsed by
anything clever.

## Entry format

The file opens with a `#` header block recording the pack's file
count, uncompressed total, pack bytes, and the pack's own SHA-256
— the pack-level hash is what the site pins (see `../CLIENT.md`).
Member files are verified by construction instead: the builder
copies each member byte-for-byte out of the hash-verified release
packs, so a member's provenance is the release pack it came from,
and the pack hash convicts the assembly.

Each entry line is:

```
<size>  <path>
```

- `size` — the file's size in bytes, decimal, right-aligned.
- `path` — the file's path inside the pack, relative, `/`
  separators, no leading `./` (for example
  `maps/evilspace.bsp`, `sound/announcer/robotic/begin.wav`).
- Lines beginning with `#` are
  comments.

## Header

The file opens with a comment block recording what it was built
from and what it builds:

```
# haxiuz stripped data manifest
# source release: nexuiz-252.zip sha256 <hash>
# pack: <pack file name>  size <bytes>  sha256 <hash>
# entries: <count>
```

If the set is ever split into more than one pack, there is one
`# pack:` line per pack, and entries carry the pack name as a
fourth field. Until then, three fields only.

## Provenance marks

An entry that is not a stock 2.5.2 file — a house override, the
evilspace house build — is followed by a comment line naming its
origin:

```
# house: sparta-menu.pk3 entry, built from patches 008+009+010
<sha256>  <size>  menu.dat
```

No entry appears without either a stock source or a house comment.
That is the whole audit trail, and it is enough: every byte in the
set is either in the verified release or accounted for here.
