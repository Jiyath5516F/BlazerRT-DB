# BlazerRT-DB

Downloads for BlazerRT, its mods and tools. 0x's Manager reads `index.json` from here and installs straight from this repo.

## What's where

```
index.json                      what the manager reads. Built by update_index.py, don't edit by hand
update_index.py                 rebuilds index.json
blazerrt/channels.json          the channels: Release, Preview, Dev Channel
blazerrt/thumbnail.jpg          the picture on the manager's BlazerRT page
blazerrt/<channel>/<build>/     one BlazerRT build per folder
mods/<mod>/                     mods the manager can install
tools/<tool>/                   tools, linked from the manager's Tools tab
```

Every build, mod and tool folder has an `info.json` with the stuff a person has to decide: the version, which Minecraft it's for, a line about it. Everything else (the file list, sizes, SHA-256 hashes) comes from the files themselves.

## Adding a BlazerRT build

1. Make a folder like `blazerrt/release/alpha-0.0.3_1.26.6401.0/` and put the package in it, same layout as the others: `data/`, `mods/`, `resource_packs/`, `INSTALL.txt` and so on.
2. Copy an `info.json` from another build and change it. `edition` is `release` for Minecraft or `preview` for Minecraft Preview, and `game` is the exact version it was built for. On any other version the manager asks first, and if the game's shader format differs from the build's, it converts the shaders with Lazurite before installing. `update_index.py` reads the format out of the build's `.material.bin` files and puts it in `index.json`, so there's nothing to fill in for that.
3. Run `python update_index.py`, then commit and push.

The Dev Channel is empty for now. A build goes in `blazerrt/dev/<build>/` the same way.

Edited something on GitHub's website, like a changelog? Pull, run `python update_index.py`, push. Every file's hash is in `index.json`, and the manager won't install a file whose hash doesn't match, so an edit without that step leaves the file stuck. The script also keeps each build's `hashes.json` up to date.

## What the manager does with a build

- `data/` goes into the game's `Content` folder, after the files it replaces are backed up.
- `mods/` goes into `Content\mods`. The live settings controller is a folder mod, `mods/BlazerRT Live Settings Controller/`, with its `icon.png` and `manifest.json`, so the manager's Mods page shows its logo and details. That's also the folder the controller keeps `settings.json` and its exported profiles in, so nothing of yours moves. An older loose `BlazerRT Live Settings Controller.dll` gets switched off, so the two can't both load. Mods listed under `replaces` in `info.json` get switched off too, so RTXControl and the controller don't both run.
- The `.mcpack` files get imported into the game, and the one picked during install is switched on at the top of Global Resources.
- `WINHTTP.dll` is the mod loader. The manager puts in its own copy, which is the same file.
- Everything else (`INSTALL.txt`, `CHANGELOG.md`, `licenses/`, `hashes.json`) stays here for people installing by hand.

`manifest.json` and the zips in the root and in `files/` belong to the older BlazerRT app. The manager doesn't use them.
