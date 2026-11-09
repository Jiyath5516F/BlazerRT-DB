"""Rebuilds index.json, the file 0x's Manager reads to know what's in here.

Every BlazerRT build, mod and tool is a folder with an info.json in it. You write the
info.json by hand; this script adds the file list, sizes and SHA-256 hashes, so nobody has
to type a hash ever again. Run it after adding or changing anything, then commit both.

    python update_index.py          rebuild index.json
    python update_index.py --check  only say whether index.json is out of date

Layout:
    blazerrt/channels.json                  the channels, in the order the app shows them
    blazerrt/thumbnail.jpg                  the picture on the app's BlazerRT page
    blazerrt/<channel>/<build>/info.json    one BlazerRT build, plus its files
    mods/<mod>/info.json                    one mod, plus its files
    tools/<tool>/info.json                  one tool, plus its files
"""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

REPO = "Jiyath5516F/BlazerRT-DB"
BRANCH = "main"
HERE = Path(__file__).resolve().parent
INDEX = HERE / "index.json"
EDITIONS = ("release", "preview")  # release = Minecraft from the Store, preview = Minecraft Preview
IMAGE = "blazerrt/thumbnail.jpg"   # the BlazerRT picture 0x's Manager shows
GAME = re.compile(r"^\d+\.\d+\.\d+\.\d+$")
GITHUB_LIMIT = 100 * 1024 * 1024  # GitHub refuses single files over 100 MB

problems = []


def problem(where, what):
    problems.append(f"{where}: {what}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_info(folder):
    path = folder / "info.json"
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        problem(path.relative_to(HERE).as_posix(), f"can't read it ({e})")
        return None


def files_in(folder):
    out = []
    for path in sorted(folder.rglob("*"), key=lambda p: p.relative_to(folder).as_posix().lower()):
        if not path.is_file() or path.name == "info.json":
            continue
        rel = path.relative_to(folder).as_posix()
        size = path.stat().st_size
        if size > GITHUB_LIMIT:
            problem(f"{folder.relative_to(HERE).as_posix()}/{rel}", "over 100 MB, GitHub won't take it")
        out.append({"path": rel, "size": size, "sha256": sha256(path)})
    return out


MATERIAL_MAGIC = 168942106
MATERIAL_ID = b"RenderDragon.CompiledMaterialDefinition"


def material_format(path):
    """The .material.bin format version (22, 23, 25, 26...), or None if it isn't one."""
    with open(path, "rb") as f:
        head = f.read(64)
    if len(head) < 12:
        return None
    magic, n = struct.unpack_from("<QI", head)
    if magic != MATERIAL_MAGIC or head[12:12 + n] != MATERIAL_ID or len(head) < 20 + n:
        return None
    return struct.unpack_from("<Q", head, 12 + n)[0]


def refresh_hashes(folder):
    """Keeps a build's own hashes.json (the list for people installing by hand) in step with
    its files, so a changelog edited on GitHub can't leave it behind."""
    path = folder / "hashes.json"
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    listed = []
    for f in sorted(folder.rglob("*"), key=lambda p: p.relative_to(folder).as_posix().lower()):
        rel = f.relative_to(folder).as_posix()
        if f.is_file() and rel not in ("hashes.json", "info.json"):
            listed.append({"path": rel, "bytes": f.stat().st_size, "sha256": sha256(f)})
    if data.get("files") != listed:
        data["files"] = listed
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


def need(info, where, *keys):
    ok = True
    for key in keys:
        if not str(info.get(key, "")).strip():
            problem(where, f'"{key}" is missing')
            ok = False
    return ok


def build_entry(channel, folder):
    where = folder.relative_to(HERE).as_posix()
    info = read_info(folder)
    if info is None or not need(info, where, "version", "edition", "game"):
        return None
    if info["edition"] not in EDITIONS:
        problem(where, f'"edition" has to be one of {", ".join(EDITIONS)}')
    if not GAME.match(info["game"]):
        problem(where, '"game" should look like 1.26.6301.0')
    refresh_hashes(folder)
    files = files_in(folder)
    names = {f["path"] for f in files}
    for pack in info.get("packs", []):
        if pack.get("file") not in names:
            problem(where, f'pack "{pack.get("file")}" isn\'t in the folder')
    if not any(n.startswith("data/") for n in names):
        problem(where, "there's no data folder, so there's nothing to install")
    # The shader file format the build was compiled for. The manager compares it with the
    # game's own, and converts with Lazurite when they differ.
    formats = {material_format(folder / n) for n in names if n.endswith(".material.bin")}
    formats.discard(None)
    if len(formats) > 1:
        problem(where, f"its .material.bin files mix format versions {sorted(formats)}")
    entry = {
        "id": f"{channel}/{folder.name}",
        "version": info["version"],
        "edition": info["edition"],
        "game": info["game"],
        "format": formats.pop() if len(formats) == 1 else None,
        "date": info.get("date", ""),
        "notes": info.get("notes", ""),
        "path": where,
        "packs": info.get("packs", []),
        "replaces": info.get("replaces", []),
        "files": files,
    }
    if "CHANGELOG.md" in names:
        entry["changelog"] = "CHANGELOG.md"
    return entry


def simple_entries(root, kind, required):
    out = []
    if not root.is_dir():
        return out
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        where = folder.relative_to(HERE).as_posix()
        info = read_info(folder)
        if info is None or not need(info, where, *required):
            continue
        entry = {"id": folder.name, **info, "path": where, "files": files_in(folder)}
        if kind == "mod":
            for ed in entry.get("editions", []):
                if ed not in EDITIONS:
                    problem(where, f'"{ed}" in "editions" has to be one of {", ".join(EDITIONS)}')
            if entry.get("install", "loose") not in ("loose", "folder"):
                problem(where, '"install" has to be "loose" or "folder"')
            if not any(f["path"].lower().endswith(".dll") for f in entry["files"]):
                problem(where, "there's no DLL in it")
        out.append(entry)
    return out


def build_index():
    try:
        channels = json.loads((HERE / "blazerrt" / "channels.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        problem("blazerrt/channels.json", f"can't read it ({e})")
        channels = []
    out_channels = []
    for ch in channels:
        cid = ch.get("id", "")
        folder = HERE / "blazerrt" / cid
        builds = []
        if folder.is_dir():
            for sub in sorted(p for p in folder.iterdir() if p.is_dir()):
                entry = build_entry(cid, sub)
                if entry:
                    builds.append(entry)
        # Newest first. Dates are YYYY-MM-DD, so they sort as text.
        builds.sort(key=lambda b: (b["date"], b["game"]), reverse=True)
        out_channels.append({"id": cid, "name": ch.get("name", cid), "note": ch.get("note", ""), "builds": builds})

    index = {
        "schema": 1,
        "raw": f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/",
        "browse": f"https://github.com/{REPO}/tree/{BRANCH}/",
    }
    # The picture on the BlazerRT page. Swap the file to change it; the hash tells the app.
    picture = HERE / IMAGE
    if picture.is_file():
        index["image"] = {"path": IMAGE, "size": picture.stat().st_size, "sha256": sha256(picture)}
    else:
        problem(IMAGE, "missing, so the BlazerRT page has no picture")
    return {
        **index,
        "channels": out_channels,
        "mods": simple_entries(HERE / "mods", "mod", ("name", "version")),
        "tools": simple_entries(HERE / "tools", "tool", ("name",)),
    }


def main():
    index = build_index()
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    for p in problems:
        print("problem:", p)
    if problems:
        print("index.json not written. Fix the above first.")
        return 1
    old = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    if "--check" in sys.argv:
        print("index.json is up to date." if old == text else "index.json is out of date. Run update_index.py.")
        return 0 if old == text else 1
    if old == text:
        print("index.json was already up to date.")
    else:
        INDEX.write_text(text, encoding="utf-8", newline="\n")
        builds = sum(len(c["builds"]) for c in index["channels"])
        print(f"index.json written: {builds} BlazerRT builds, {len(index['mods'])} mods, {len(index['tools'])} tools.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
