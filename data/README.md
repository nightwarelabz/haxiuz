# The stripped data set

Status: **built.** This directory holds the builder and the
manifest of the stripped pack the site serves as `haxiuz.pk3`
(1,528 files, 99,228,456 bytes, SHA-256
`10018c6a19fee310c70504952691fb21748ff5d1412c4f1271ff7de658d7f5b3`).
The manifest was produced by measuring what a haxiuz session loads
(a native client under an open-file census: menu boot + a full CTF
MinstaHook bot match on evilspace, closed out with the gamecode's
precache lists), never by guessing.

## What is here

- `build_keep.py` — derives the keep set (`keep.json`) from the
  session censuses and the closure rules (model companions,
  texture variants, QC precaches).
- `build_pack.py` — assembles the pack from the verified release
  packs: every member copied byte-for-byte from
  `data20091001.pk3` / `common-spog.pk3`, nothing re-encoded, and
  writes `manifest.txt`.
- `keep.json` — the derived keep set the builder consumes.
- `manifest.txt` — the manifest itself, in the format specified
  in `MANIFEST.md`: a header block (file count, uncompressed
  total, pack bytes, pack SHA-256), then one line per file —
  size, then path.

## The rule the set is built by

A file is in the set only if a haxiuz session loads it: the
evilspace CTF match, MinstaHook, the MinstaNex, the Mulder player
model, the countdown and game announcer audio, the menu and HUD,
and the engine's own startup surface. Everything else in the 2.5.2
universe — the other maps, weapons, models, campaigns — is out,
however stock it is. The house override packs (menu, progs,
csprogs) and the evilspace house build are additions on top of the
set, recorded in the manifest as their own entries with their own
provenance, never silently folded into the stock list.

## Verification

- The input release is verified before anything is extracted:
  `nexuiz-252.zip`, 931,253,731 bytes, SHA-256
  `a5e27ebcc9775c4a490d0d3536c32e4a8f8f96b038c0b6a78d1823c37a962000`.
- Every member is copied byte-for-byte from the verified release
  packs (never re-encoded); the manifest records each member's
  size and path, and the pack's own SHA-256 in its header.
- The built pack is recorded with its size and SHA-256, which is
  what the site pins in its build record (see `../CLIENT.md`).

## What is never here

The game data itself. This repo holds the manifest and the
builder — the recipe — not the packs they produce, the same rule
as the engine binaries and the stock packs everywhere else in the
house repos.
