"""Compute the real numbers shown in the "How it decides" video.

Run from the repository root with the project's virtual environment:

    .venv/Scripts/python video/fingerprint/make_data.py

It uses the program's own functions (perceptual_hash, hamming_distance) on the
benchmark photos and writes video/fingerprint/data.json and data.js plus small copies of the
photos under video/fingerprint/assets/. The mirrored picture is a test edit made
here, not a benchmark file.
"""

import json
from pathlib import Path

import imagehash
from PIL import Image, ImageOps

from find_duplicates.hashing import (
    PERCEPTUAL_HASH_HIGHFREQ_FACTOR,
    PERCEPTUAL_HASH_SIZE,
    hamming_distance,
    perceptual_hash,
)

ROOT = Path(__file__).resolve().parents[2]
BENCH = ROOT / "benchmark" / "data"
OUT = Path(__file__).resolve().parent
ASSETS = OUT / "assets"
ASSETS.mkdir(exist_ok=True)

THUMB_SIDE = PERCEPTUAL_HASH_SIZE * PERCEPTUAL_HASH_HIGHFREQ_FACTOR  # 28


def thumb_pixels(path: Path) -> list[list[int]]:
    """The tiny grey picture imagehash compares: grey, resized to 28 by 28."""
    with Image.open(path) as img:
        grey = ImageOps.exif_transpose(img).convert("L")
        small = grey.resize((THUMB_SIDE, THUMB_SIDE), Image.Resampling.LANCZOS)
    pixels = list(small.tobytes())
    return [pixels[row * THUMB_SIDE : (row + 1) * THUMB_SIDE] for row in range(THUMB_SIDE)]


def bits(h: imagehash.ImageHash) -> list[list[int]]:
    return [[int(v) for v in row] for row in h.hash]


def copy_small(src: Path, name: str, height: int = 480) -> str:
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        width = round(img.width * height / img.height)
        img.resize((width, height), Image.Resampling.LANCZOS).save(ASSETS / name, "JPEG", quality=88)
    return name


# the test edit: a mirrored copy of the original (saved at full size so it is hashed like a file)
mirrored_path = ASSETS / "p05_mirrored_full.jpg"
with Image.open(BENCH / "p05_orig.jpg") as img:
    ImageOps.mirror(ImageOps.exif_transpose(img).convert("RGB")).save(mirrored_path, "JPEG", quality=90)

files = {
    "orig": BENCH / "p05_orig.jpg",
    "resized": BENCH / "p05_resized.jpg",
    "recompressed": BENCH / "p05_recompressed.jpg",
    "other": BENCH / "p07_orig.jpg",
    "mirrored": mirrored_path,
}
hashes = {key: perceptual_hash(path) for key, path in files.items()}

data = {
    "hash_bits": PERCEPTUAL_HASH_SIZE**2,
    "thumb_side": THUMB_SIDE,
    "files": {
        key: {
            "name": ("p05_mirrored (test edit)" if key == "mirrored" else path.name),
            "image": copy_small(path, f"{key}.jpg"),
            "thumb": thumb_pixels(path),
            "bits": bits(hashes[key]),
        }
        for key, path in files.items()
    },
    "distance_to_orig": {
        key: hamming_distance(hashes["orig"], hashes[key]) for key in files if key != "orig"
    },
}
(OUT / "data.json").write_text(json.dumps(data), encoding="utf-8")
(OUT / "data.js").write_text("window.FP = " + json.dumps(data) + ";" + chr(10), encoding="utf-8")
mirrored_path.unlink()
print(json.dumps(data["distance_to_orig"]), "hash bits:", data["hash_bits"])
