"""Spike: loop --threshold 0..12 against a real photo folder and record, for
each value, how many duplicate groups came out and how large the biggest one
was. Does not modify the photos; only reads them.

Usage:
    python scripts/threshold_spike.py <folder> [--out spike/threshold-spike-results.csv]
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from find_duplicates.cli import run
from find_duplicates.scanner import ScanTargetError


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Folder of photos to scan (not committed)")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("spike/threshold-spike-results.csv"),
        help="Where to write the per-threshold CSV (default: spike/threshold-spike-results.csv)",
    )
    args = parser.parse_args()

    try:
        photo_count = len(
            [p for p in args.folder.iterdir() if p.suffix.lower() in {".jpg", ".png"}]
        )
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {photo_count} .jpg/.png files in {args.folder}\n")

    rows = []
    for threshold in range(13):
        try:
            exact_count, near_duplicate_group_count, duplicate_groups = run(
                args.folder, threshold
            )
        except ScanTargetError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)

        group_count = len(duplicate_groups)
        largest_group_size = max((len(g.members) for g in duplicate_groups), default=0)

        rows.append(
            {
                "threshold": threshold,
                "group_count": group_count,
                "largest_group_size": largest_group_size,
                "exact_duplicate_groups": exact_count,
                "near_duplicate_groups": near_duplicate_group_count,
            }
        )
        print(
            f"threshold={threshold:2d}  groups={group_count:4d}  "
            f"largest_group={largest_group_size:4d}  "
            f"exact={exact_count:4d}  near={near_duplicate_group_count:4d}"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
