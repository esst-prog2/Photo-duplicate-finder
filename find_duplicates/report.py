import csv
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

CSV_FIELDNAMES = ["files", "similarity_score", "keep"]


def _keep_metric(path: Path) -> tuple[int, int]:
    file_size = path.stat().st_size
    with Image.open(path) as img:
        resolution = img.width * img.height
    return (file_size, resolution)


def choose_keep(group: list[Path]) -> Path:
    return max(group, key=_keep_metric)


@dataclass
class DuplicateGroup:
    members: list[Path]
    similarity_score: str
    keep: Path


def write_report(groups: list[DuplicateGroup], output_path: Path) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for group in groups:
            writer.writerow(
                {
                    "files": ";".join(member.name for member in group.members),
                    "similarity_score": group.similarity_score,
                    "keep": group.keep.name,
                }
            )
