#!/usr/bin/env python3
"""Unpack the raw study data into data/raw/ and record a manifest.

The raw data ships as three ZIP archives exported from the course Teams folder
"SPO-14560 Project Seminar I - General":

    Anaropia.zip    VR tracking   -> data/raw/vr/
    PsychoPy.zip    PsychoPy logs -> data/raw/psychopy/
    LimeSurvey.zip  questionnaire -> data/raw/limesurvey/

Each file's SHA-256 is computed from the stream while it is written, so the
~0.9 GB of raw data is read once and never re-hashed. The manifest is written
next to data/raw/, never inside it: once extracted, data/raw/ holds exactly the
contents of the archives and nothing else. Files already present
with the expected size keep their hash from the existing manifest, which makes
the script both idempotent and resumable: interrupt it and run it again.

Usage
-----
    python src/00_unpack_raw.py --source ~/Downloads
    python src/00_unpack_raw.py --source ~/Downloads --max-seconds 150
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys
import time
import zipfile
from pathlib import Path

ARCHIVES = {
    "Anaropia.zip": "vr",
    "PsychoPy.zip": "psychopy",
    "LimeSurvey.zip": "limesurvey",
}

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
MANIFEST = REPO / "data" / "raw_manifest.csv"
CHUNK = 1 << 20


def load_manifest() -> dict[str, dict]:
    if not MANIFEST.exists():
        return {}
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        return {r["path"]: r for r in csv.DictReader(fh)}


def save_manifest(rows: dict[str, dict]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists() and not os.access(MANIFEST, os.W_OK):
        raise PermissionError(MANIFEST)
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["archive", "path", "bytes", "sha256"])
        w.writeheader()
        for key in sorted(rows):
            w.writerow(rows[key])


def extract_one(zf: zipfile.ZipFile, member: zipfile.ZipInfo, out: Path) -> str:
    """Write one member to disk, returning its SHA-256 without a second read."""
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".part")
    h = hashlib.sha256()
    with zf.open(member) as src, tmp.open("wb") as dst:
        while chunk := src.read(CHUNK):
            h.update(chunk)
            dst.write(chunk)
    tmp.replace(out)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--source", type=Path, default=Path.home() / "Downloads",
                    help="folder holding the three ZIP archives")
    ap.add_argument("--max-seconds", type=float, default=0,
                    help="stop cleanly after N seconds; re-run to continue")
    args = ap.parse_args()

    missing = [n for n in ARCHIVES if not (args.source / n).exists()]
    if missing:
        print(f"Archives not found in {args.source}: {', '.join(missing)}",
              file=sys.stderr)
        return 1

    RAW.mkdir(parents=True, exist_ok=True)
    rows = load_manifest()
    started = time.monotonic()
    new = kept = 0
    stopped_early = False

    for name, sub in ARCHIVES.items():
        with zipfile.ZipFile(args.source / name) as zf:
            for m in zf.infolist():
                if m.is_dir():
                    continue
                out = RAW / sub / m.filename
                key = str(out.relative_to(RAW)).replace("\\", "/")
                if (out.exists() and out.stat().st_size == m.file_size
                        and key in rows):
                    kept += 1
                    continue
                if args.max_seconds and time.monotonic() - started > args.max_seconds:
                    stopped_early = True
                    break
                digest = extract_one(zf, m, out)
                rows[key] = {"archive": name, "path": key,
                             "bytes": m.file_size, "sha256": digest}
                new += 1
        if stopped_early:
            break

    if new or not MANIFEST.exists():
        try:
            save_manifest(rows)
        except PermissionError:
            print("data/raw is write-protected by DVC. Run 'dvc unprotect data/raw' "
                  "first if you really need to re-extract.", file=sys.stderr)
            return 3
    total = sum(int(r["bytes"]) for r in rows.values())
    print(f"extracted now: {new} | already present: {kept} | "
          f"in manifest: {len(rows)} files, {total / 1e9:.2f} GB")
    if stopped_early:
        print("time budget reached — run the script again to continue")
        return 2
    if new:
        print(f"manifest -> {MANIFEST.relative_to(REPO)}")
    else:
        print("nothing to do — data/raw already matches the archives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
