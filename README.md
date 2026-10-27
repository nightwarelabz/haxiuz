# haxiuz

haxiuz is the house capture-the-flag game: a strip-down rebuild on the
DarkPlaces engine and the Nexuiz 2.5.2 base, cut down to exactly one
match format and the data that format loads. It is not a mod of a
larger game install — this repository is the game's own source of
truth for its QuakeC patches, its server configuration, and its data
manifest.

A NIGHTWARE LABZ project.

## The match

Every match runs the same table:

- Capture the flag on **evilspace** (the house CTF build: stock
  geometry, flag and team-spawn entities injected into the BSP entity
  lump, mapinfo `type ctf 300 20 10`).
- **MinstaHook**: MinstaGib plus the offhand grappling hook.
- The **MinstaNex** is the only weapon. Mouse 1 fires the beam,
  mouse 2 fires its bounce laser. One shot at a time, infinite
  ammunition (patch 001), no weapon pickups — the flag is the only
  pickup in the room.
- **20 minutes / 10 captures** (the map's mapinfo limits: 300 points,
  20 minutes, 10 captures).
- Every match opens with a spoken **10-second countdown** ending in
  BEGIN (patch 007 widens the stock announcer, which only spoke the
  last three seconds).
- Every player wears the same character — **Mulder**, red team red,
  blue team blue — set by stock server cvars, not by logic.
- **Bots fill the room to 6** and yield to human players one for one
  (`minplayers 6`, `bot_join_empty 1` in the server config).
- Settings are locked to the player name (patch 008): every player
  runs the same build specs and configuration.

## How it is played

haxiuz runs inside BLACKSITE OS on nosuchmachine.net. Open the
haxiuz window in the OS; the game boots to its own main menu. In the
menu's Multiplayer dialog, the first button is the door, labeled
**haxiuz** (patch 009 lays the door, patch 010 sets its label).
Pressing it connects to the house server. No connection is made for
the player at boot.

The browser has no UDP, so the connection rides the house transport:
a WebRTC DataChannel first (the nightwire gateway), falling back to
the house WebSocket bridge — one session is one player, and each
frame crosses as one datagram to the native DarkPlaces server. See
CLIENT.md for what the site serves and how it consumes this repo.

## Why a strip-down

The full Nexuiz 2.5.2 data universe is close to a gigabyte of packs
for a game that, here, plays one map, one gametype, one weapon. The
strip-down keeps only what a haxiuz session actually loads —
one map, the models, sounds and textures that map and the match
reference — as a minimal data set in place of the full release
packs. The set is defined by the manifest in `data/` and assembled
by its builder; the game data itself is not stored in this repo
(same rule as the other house repos: sources, patches, config and
manifest live here, binaries and packs do not).

## Layout

- `patches/` — the house QuakeC patch stack, numbered, applied in
  order. `patches/README.md` is the index: what each patch does,
  which progs it touches, and the stack order per progs.
- `config/haxiuz.cfg` — the server configuration. Stock cvars only;
  every line names its source in the stock 2.5.2 server config or
  QuakeC sources. It changes no game logic — MinstaHook is built
  from the mutators the game shipped.
- `data/` — the stripped-pack manifest format and the builder that
  assembles the minimal data set from a verified 2.5.2 release.
- `BUILD.md` — how the patch stack is applied and compiled with the
  release's own fteqcc, and the parity discipline a rebuild is
  measured against.
- `CLIENT.md` — what nosuchmachine.net serves for haxiuz and how
  the site consumes this repo.
- `LICENSE` — GPL v2 text, as shipped with the base release.

## Provenance

- Engine: DarkPlaces (the Xonotic team's maintained tree),
  GPL-2.0-or-later. The web client is that engine compiled to
  WebAssembly; its build is recorded in the site repo's
  `tools/nexuiz/BUILD.md` and served under `public/nexuiz/` there.
- Game base: Nexuiz 2.5.2 (Alientrap, 2009), file
  `nexuiz-252.zip`, 931,253,731 bytes, SHA-256
  `a5e27ebcc9775c4a490d0d3536c32e4a8f8f96b038c0b6a78d1823c37a962000`.
  The QuakeC sources patched here are the release's own
  `gamesource20091001` tree.
- Everything house-made in this repo is a numbered diff against
  that base, a cvar configuration, or a manifest. No stock file is
  modified in place anywhere; overrides ride the engine's own pack
  precedence.

## License

GNU General Public License v2 — see `LICENSE`. The base game and
engine are GPL; haxiuz is GPL for the same reason, stated plainly.
