# The house QC patch stack

Every house change to the game's QuakeC lives here as a numbered
diff against the stock Nexuiz 2.5.2 sources (the release's own
`gamesource20091001` tree, `qcsrc/`). Nothing else in the game logic
is changed. Patches apply in number order within each progs, with
`patch -p1`; see `../BUILD.md` for the compile recipe and the parity
discipline.

## Server and client progs

Applied to `qcsrc/server` and `qcsrc/client`. Numbers 002–005 were
an earlier, abandoned menu line — a live-match overlay menu that
fronted the room — superseded by the stock-menu-plus-door approach
of 008–010; they are not part of this stack. The numbering is kept
as-is so the numbers match the house record.

| Patch | Progs | What it does |
|---|---|---|
| `house-qc-patch-001.diff` | server | Infinite ammo and no dropped weapons. Grants every spawning player `IT_UNLIMITED_WEAPON_AMMO` in the minstagib branch of `StartItems` (`server/miscfunctions.qc`) — the game's own "never deduct" bit, so MinstaNex shots cost nothing and `DEATH_NOAMMO` cannot occur. Also makes `SpawnThrownWeapon` (`server/cl_player.qc`) return unconditionally under `g_minstagib`, so a death never drops a weapon pickup. |
| `house-qc-patch-006.diff` | server | Equip fallback. In `W_SetWeapon` (`server/cl_weapons.qc`): when a joining player reaches spawn with `switchweapon` 0 — the priority list has not arrived, or never does — recover by choosing the best owned weapon, falling back to the first weapon the player actually owns (in this room, always the MinstaNex). Only a player who owns nothing gets the stock clear-out. |
| `house-qc-patch-007.diff` | client | Countdown voice. In `client/miscfunctions.qc`, the restart announcer speaks the robotic countdown numbers at `<= 10` instead of the stock `<= 3`, so the 10-second start delay (`g_start_delay 10` in the server config) is spoken 10..1 and the stock BEGIN plays at zero. One comparison constant; the announcer samples are stock files. |

The server progs ships as the override pack `sparta-progs.pk3`
(single entry `progs.dat`) and the client progs as
`sparta-csprogs.pk3` (single entry `csprogs.dat`) in the server's
data directory, where pack precedence makes them the files the
engine reads. The release packs are never modified.

## Menu progs

Applied to `qcsrc/menu`, stacked in order 008, then 009, then 010,
then 011, then 012, then 013, then 014.

| Patch | Files | What it does |
|---|---|---|
| `house-qc-patch-008.diff` | `dialog_settings.c`, `dialog_multiplayer_playersetup.c`, `menu.qc` | Settings lock and the build tag. The Settings dialog's six tabs (Input, Video, Effects, Audio, Network, Misc) are replaced by the single Player tab, and the player tab keeps only the name label, the name field, and the stock "Apply immediately" row. Everything else the tab offered — model, colors, crosshair, view, weapons, radar/HUD, gore — is removed, so every player runs the same specs and the only editable setting is the name worn in the room. The same patch puts the build's tag in the main menu (`menu.qc`, drawn with the menu background at the lower right of the title area); patch 010 later sets that tag's text. |
| `house-qc-patch-009.diff` | `dialog_multiplayer.c` | The door. The Multiplayer dialog gains a full-width stock command button at its head, above the server browser, issuing `connect thisissparta2` — the same connect the boot once dealt sight unseen, now pressed by the player's own hand. The dialog grows one row (24 to 25) and its tab controller drops the same row. The door carries no name dependency: the web build deals the player's name to the engine itself. |
| `house-qc-patch-010.diff` | `menu.qc`, `dialog_multiplayer.c` | Identity: the main menu's masthead tag and the door button's label both read "haxiuz". The door's command, `connect thisissparta2`, is unchanged — that token is load-bearing across the bridge, the gateway, and the OS window, and is not part of the identity. |
| `house-qc-patch-012.diff` | `menu.qc`, `menu/nexuiz/util.qc` | The menu banner. The stock backgrounds carry the Nexuiz logo and the nexuiz.com strap baked into one plate layer (title layer 3, in-game layer 2); that layer is never drawn, and in its top-right footprint the menu draws the house banner — the machined gunmetal NIGHTWARE LABZ plate built for this menu in the 2026-10-25 house art pass (`redo_plate` in the site-era `build_menu_art.py`: raised machined-silver letters, the red rule along its foot, the red etched rezzmodV1 tag), carried as `gfx/nightware-banner.tga` in the menu pack — fitted by its own aspect at each background's own alpha. The separate update nag carrying a nexuiz.com address is gated off, so no nexuiz.com element can appear on the menu. Parity: CRC 10020, two functions' opcode streams change (see the site repo's BUILD.md). |
| `house-qc-patch-013.diff` | `menu/nexuiz/dialog_multiplayer_playersetup.c` | Mouse sensitivity, restored. The Player tab (the Settings surface patch 008 left standing) gains the stock "Sensitivity:" label and slider (`makeNexuizSlider(1, 32, 0.2, "sensitivity")`, verbatim from the stock Input settings, unwired since 008). The house config never deals the cvar, so the player's value stands and the engine's config save persists it. Parity: CRC 10020, one function's opcode stream changes. |
| `house-qc-patch-014.diff` | `menu.qc` | The tag's seat. Since patch 012 the plate owns the title's top right and the build's tag (008/010) overprinted the plate's right edge, stacked over its etched rezzmodV1. The tag moves to the clear band immediately left of the plate at the same height, its right edge one tag margin (0.014) left of the plate's left edge, which `m_draw` recomputes with drawBackground's own cover-fit math so the seat tracks the plate at any aspect. Nothing else moves. Parity: CRC 10020, one function's opcode stream changes (`m_draw`, 287 → 323 statements). |
| `house-qc-patch-011.diff` | `menu/draw.qc` | The native cursor. The menu's drawn mouse pointer paints at zero alpha — same picture, position and size, nothing shown — while mouse tracking and hit-testing are untouched; with `menu_mouse_absolute 1` dealt by the client, the engine's pointer IS the browser's pointer, so menus are worked with the real cursor. Parity against 010 is total except one statement's operand (see the proof record in the site repo's BUILD.md). |

The menu progs ships as the override pack `sparta-menu.pk3`
(two entries: `menu.dat` and `gfx/nightware-banner.tga`, the
banner patch 012 draws) beside the release packs in the served
game directory. Current build (through 014): menu.dat
`d8afaccf5dd8f7b1f32383353a4e52ff9a011790859b370b1361630b24e80ef5`,
pk3 `9b20e773ef86a45017835138ac3bda582631c583dddffe68f9c1c1eb6b67cd17`.
