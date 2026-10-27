# Building the patch stack

The patch stack in `patches/` is reproducible from this repo plus
one input: a verified Nexuiz 2.5.2 release (`nexuiz-252.zip`,
SHA-256
`a5e27ebcc9775c4a490d0d3536c32e4a8f8f96b038c0b6a78d1823c37a962000`).
Its source archive, `gamesource20091001.zip` inside the release,
carries both the QuakeC sources (`qcsrc/`) and the compiler. No
other toolchain is involved, and no stock file is edited in place:
patches apply to an extracted copy of the sources, and the compiled
progs ship as override packs that ride the engine's own pack
precedence beside the unmodified release packs.

## The compiler

fteqcc, as shipped by Alientrap inside the release itself —
`sources/fteqcc-binaries-and-source-rev1253299209-bb8ceb9870af06104b67ae4cc2ec29552dce705b.zip`
in the verified zip; the prebuilt `fteqcc/fteqcc-linux-x86_64`
binary, SHA-256
`b2905a9a91911ec621c420edc5e9122b77458cdd03beda5145874040cff0612f`
(base revision commit `bb8ceb9870af`, the fteqcc "nexuiz" branch
snapshot of the release month). Using the era's own compiler is not
nostalgia: it is what makes the parity measurements below mean
anything.

## Server and client progs

```
# from the extracted gamesource tree (the directory holding qcsrc/)
patch -p1 < house-qc-patch-001.diff   # server: infinite ammo, no drops
patch -p1 < house-qc-patch-006.diff   # server: equip fallback
patch -p1 < house-qc-patch-007.diff   # client: countdown voice

cd qcsrc/server && fteqcc -Os         # writes progs.dat
cd qcsrc/client && fteqcc -Os         # writes csprogs.dat
zip -9 sparta-progs.pk3   progs.dat   # single entry, at the root
zip -9 sparta-csprogs.pk3 csprogs.dat # single entry, at the root
```

Both builds: 0 warnings. The two override packs go in the server's
data directory. Patch paths inside the server/client diffs are
relative to the `qcsrc/` tree (`server/…`, `client/…`); the menu
diffs below are relative to the tree's parent (`qcsrc/menu/…`) —
apply each from the directory its paths expect.

## Menu progs

```
# from the extracted gamesource tree's parent (holding qcsrc/)
patch -p1 < house-qc-patch-008.diff   # settings lock + build tag
patch -p1 < house-qc-patch-009.diff   # the door
patch -p1 < house-qc-patch-010.diff   # identity: tag + door label "haxiuz"
patch -p1 < house-qc-patch-011.diff   # the native cursor
patch -p1 < house-qc-patch-012.diff   # the menu banner
patch -p1 < house-qc-patch-013.diff   # mouse sensitivity, restored

cd qcsrc/menu
fteqcc -O1 -Oreturn_only -Ostrip_functions   # writes ../../menu.dat
zip -9 sparta-menu.pk3 menu.dat gfx/nightware-banner.tga
```

The patches apply clean in order and reproduce the compiled
tree exactly. The pack's second entry is the banner patch 012
draws: the NIGHTWARE LABZ gunmetal banner converted losslessly
from its PNG master (1,672 x 941; the engine build decodes no
PNG), at `gfx/nightware-banner.tga`. Current shipped hashes
(008 through 013): menu.dat SHA-256
`de06b531c8cabedf64c00d005d4e1365ca54b92c2992797a474073aa0e186f0c`,
sparta-menu.pk3 SHA-256
`8e4f26be73410725a0f7d4807809eb29875cbf0b4988107bf2ee39d759c0e0c2`.

## Parity discipline

A rebuild is not trusted because it compiles. It is measured
against the shipped progs it replaces, and the claim made for it is
exactly what the measurement supports:

- **Header CRC.** The progs header CRC is the engine-visible
  contract. Server progs: **5927** for stock and for every patched
  build. Menu progs: **10020**, stock and patched alike. A build
  that moves the CRC is a different program, not a patch.
- **Definitions are byte-identical.** Strings, field definitions,
  global definitions, and initial global data match the shipped
  file's sections, except where a patch's own record says otherwise
  (patch 009 adds two anonymous string globals — the door's label
  and command; patch 010's duplicate-string fold removes one).
  Function tables keep their shape: same count (menu: 1,010), same
  names, order, and parameter metadata.
- **Statement deltas are counted, not waved at.** Each patch's
  measured delta is on its record: patch 009 changes exactly one
  function's statement stream (+16 statements, the net program
  delta). Patch 010 changes no statement at all — 43,525 in both
  builds, opcode stream identical; only string operands renumber
  past the folded global.
- **Code-section byte-identity is not claimed.** The release's
  fteqcc was two weeks younger than the bundled revision and does
  not survive; even an unpatched rebuild differs from the shipped
  progs in function-exit encodings (menu: 168 of 1,010 functions,
  the differing opcode census confined to DONE, RETURN, IF, IFNOT,
  GOTO). What is claimed is what is measured: same defs, same
  strings, same globals, same CRC — and the same behavior, driven
  against the real client and server.

## The server config

`config/haxiuz.cfg` needs no build. It is stock cvars only, run by
the native DarkPlaces dedicated server with the override packs
above in its data directory. Its comments name the source of every
line. The one identity line is the hostname, `haxiuz`.

## What is not built here

The engine (DarkPlaces to WebAssembly) and the data packs are not
built from this repo. The engine build is recorded in the site
repo's `tools/nexuiz/BUILD.md`; the minimal data set is assembled
by the builder in `data/` from the verified release. This repo
builds the game's logic, config, and manifest — the parts that are
haxiuz's own.
