# How the site serves haxiuz

haxiuz is played in the browser, inside BLACKSITE OS on
nosuchmachine.net. This file records the split between that site and
this repo: the site serves the client and the transport; this repo is
the game's own source of truth — its QuakeC patch stack
(`patches/`), its server configuration (`config/`), and its data
manifest (`data/`). The full serving record lives in the site repo
at `public/nexuiz/NOTICE.txt` and `tools/nexuiz/BUILD.md`; what
follows is the shape of it.

## What the site serves

From the site repo's `public/nexuiz/`:

- **The engine** — DarkPlaces compiled from its real source tree to
  WebAssembly (`darkplaces-wasm.js` + `darkplaces-wasm.wasm`),
  served immutable under an engine stamp in the play frame; a
  rebuild bumps the stamp in the same change. Build record:
  `tools/nexuiz/BUILD.md` in the site repo.
- **The play frame** (`play.html` / `play.js`) — the loader. It
  fetches the data packs, SHA-256-verifies each against its pinned
  hash before the engine starts (wrong bytes are refused), writes
  them into the engine's filesystem, and deals the session's
  transport. Kept packs are verified from local bytes on later
  visits; the wire is crossed once.
- **The menu override pack** (`sparta-menu.pk3`) — compiled from
  this repo's menu patch stack (008 + 009 + 010; see `BUILD.md`).
  It rides beside the data packs, and the engine's own directory
  order makes its `menu.dat` the one that loads. The release packs
  are not modified.
- **The house configuration** (`autoexec.cfg`) — cvars only: the
  MinstaHook table for local games and the two platform cvars the
  web build needs. Online, the server's own settings rule.
- `NOTICE.txt` — the provenance and hash record for everything
  above, written for players.

## The data pipe

The stock packs are too large to ship as site files, so the site's
data proxy (`/api/nexuiz-data`) streams fixed 16 MiB chunks of each
pack's span inside its pinned container zip; the loader inflates,
reassembles, and verifies. The stripped data set defined by this
repo's `data/` manifest replaces those full packs as the thing
served — same loader discipline (pinned size, SHA-256 verified
before the engine starts, kept locally after one crossing), a
fraction of the bytes. The stripped pack is itself too large for
a site file (99 MB against the platform's 25 MiB static-asset
ceiling), so it rides the same pipe: its container is
`haxiuz-release.zip` — a release asset on this repo (tag
`data-1`), a zip whose single deflated entry is the pack — and
the pipe streams the pack's span out of it (offset 40, length
98,509,217) as its `haxiuz` part. The full packs' parts stand
beside it, unchanged, as the documented restore.

## The door and the connect token

Opening the game deals the room itself: the client boots with
the connect dealt (the auto-join — the mechanism the client
carried before the menu-first build, restored), and the player
lands in the match. The door the menu patch stack puts at the
head of the Multiplayer dialog (patch 009; labeled **haxiuz**
by patch 010) stands as the manual road back in — after a
local match, a disconnect, or a join that failed; a failed
join leaves the player at the menu, with the door. The door
issues one stock command:

```
connect thisissparta2
```

The word `thisissparta2` in that command is an internal routing
token, not the game's name. It is load-bearing across the menu, the
bridge, the gateway, and the OS window, and the haxiuz identity does
not change it — patch 010 is explicit that the command stands
byte-for-byte. Do not "fix" it to match the label.

The engine's socket layer dials the dealt bridge address for any
connect, so the boot's connect and the door's connect alike reach
the room through the dealt transport: on a room deal the frame
deals the transport and the connect argument together; on the
other deals the transport rides undialed, for the door.

## The road to the server

DarkPlaces speaks UDP; a browser has no UDP. Two house roads carry
the datagrams, tried in this order:

1. **WebRTC** — the nightwire gateway (`sparta-rtc`, in the
   nightwire repo). The play frame's socket shim opens a signaling
   WebSocket at the bridge door's `/rtc` path, creates an
   RTCDataChannel labeled `sparta` (`{ordered: false,
   maxRetransmits: 0}`), and from channel-open each DataChannel
   message is one UDP datagram to the native server, and back,
   byte-identical.
2. **WebSocket** — the house bridge (`sparta-bridge`). The engine's
   socket layer dials the dealt `wss` address verbatim with the
   `sparta` subprotocol; the bridge carries each binary frame as one
   datagram to the real server. One WebSocket session is one player.

The public door to both is an outbound tunnel endpoint on the game
host (the host's router is never reconfigured; there is no inbound
mapping). The OS window (`src/scripts/os-nexuiz.ts` in the site
repo) deals the bridge address, the player's name, and a per-deal
session tag with the game frame. The server at the end of the road
is the native DarkPlaces dedicated server, running this repo's
`config/haxiuz.cfg` with the server/client patch stack's override
packs in its data directory.

## The consumption rule

When a haxiuz change is a game change — a patch, a cvar, the data
set — it is made here, in this repo, and the site and the server
pick it up from here. When it is a serving change — the loader, the
transport, the OS window — it is made in the site or nightwire repo,
and this file is updated to match.
