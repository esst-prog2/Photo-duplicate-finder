"""Build the hw5 benchmark folder from the hand-picked photos in benchmark/sources/.

Each source photo becomes one group of 4 files: a downscaled original, a
byte-identical copy, a copy resized to 70%, and a copy re-saved at JPEG quality
70. The expected result (one group of 4 per source photo) follows from this
construction, so this script must never import or run find_duplicates.
"""

import argparse
import csv
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "sources"
DATA = HERE / "data"
MANIFEST = HERE / "manifest.csv"

LONG_SIDE = 800
RESIZE_FACTOR = 0.7
ORIGINAL_QUALITY = 90
RECOMPRESSED_QUALITY = 70
RESAMPLE = Image.Resampling.LANCZOS


def load_upright_rgb(path: Path) -> Image.Image:
    with Image.open(path) as img:
        return ImageOps.exif_transpose(img).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="regenerate even though benchmark/data already exists",
    )
    args = parser.parse_args()

    sources = sorted(p for p in SOURCES.iterdir() if p.suffix.lower() in {".jpg", ".jpeg"})
    if not sources:
        sys.exit(f"No .jpg sources found in {SOURCES}")
    if DATA.exists() and any(DATA.iterdir()) and not args.force:
        sys.exit(f"{DATA} already exists and the benchmark data is frozen; use --force to regenerate.")
    DATA.mkdir(exist_ok=True)

    rows = []
    for number, source in enumerate(sources, start=1):
        group = f"p{number:02d}"
        paths = {
            "orig": DATA / f"{group}_orig.jpg",
            "identical": DATA / f"{group}_identical.jpg",
            "resized": DATA / f"{group}_resized.jpg",
            "recompressed": DATA / f"{group}_recompressed.jpg",
        }

        original = load_upright_rgb(source)
        original.thumbnail((LONG_SIDE, LONG_SIDE), RESAMPLE)
        original.save(paths["orig"], "JPEG", quality=ORIGINAL_QUALITY)

        shutil.copyfile(paths["orig"], paths["identical"])

        with Image.open(paths["orig"]) as saved:
            base = saved.convert("RGB")
        width, height = base.size
        resized_size = (max(1, round(width * RESIZE_FACTOR)), max(1, round(height * RESIZE_FACTOR)))
        base.resize(resized_size, RESAMPLE).save(paths["resized"], "JPEG", quality=ORIGINAL_QUALITY)
        base.save(paths["recompressed"], "JPEG", quality=RECOMPRESSED_QUALITY)

        rows.extend({"file": path.name, "group": group} for path in paths.values())
        print(f"{group} <- {source.name}")

    with open(MANIFEST, "w", newline="", encoding="utf-8") as manifest_file:
        writer = csv.DictWriter(manifest_file, fieldnames=["file", "group"])
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"\n{len(sources)} sources -> {len(rows)} files in {DATA}; "
        f"expected result: {len(sources)} groups, each of size 4, 0 contaminated."
    )


if __name__ == "__main__":
    main()
