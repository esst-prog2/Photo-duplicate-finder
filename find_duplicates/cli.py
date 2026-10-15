import sys
from collections import Counter
from collections.abc import Callable
from datetime import datetime
from itertools import combinations
from pathlib import Path

import click

from find_duplicates.grouping import group_by_threshold
from find_duplicates.hashing import (
    DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    exact_hash,
    hamming_distance,
    perceptual_hash,
)
from find_duplicates.report import DuplicateGroup, suggest_keep, write_report
from find_duplicates.scanner import (
    SUPPORTED_EXTENSIONS,
    ScanTargetError,
    scan_folder,
    skipped_image_files,
)


def _categorize_distance(distance: int, threshold: int) -> str:
    if distance > threshold:
        raise ValueError(f"distance {distance} is above the threshold {threshold}, so it cannot be in a group")
    return "Very Similar" if distance <= threshold // 2 else "Similar"


def _group_similarity_category(
    members: list[Path],
    exact_hashes: dict[Path, str],
    distance: Callable[[Path, Path], int],
    threshold: int,
) -> str:
    if len({exact_hashes[member] for member in members}) == 1:
        return "Exact"

    max_distance = max(distance(file_a, file_b) for file_a, file_b in combinations(members, 2))
    return _categorize_distance(max_distance, threshold)


def _report_filename(now: datetime) -> str:
    return now.strftime("duplicates_%Y%m%d_%H%M.xlsx")


def run(folder: Path, threshold: int) -> tuple[int, int, list[DuplicateGroup]]:
    files = scan_folder(folder)

    exact_hashes = {file: exact_hash(file) for file in files}
    perceptual_hashes = {file: perceptual_hash(file) for file in files}

    def distance(file_a: Path, file_b: Path) -> int:
        return hamming_distance(perceptual_hashes[file_a], perceptual_hashes[file_b])

    groups = group_by_threshold(files, distance, threshold)
    exact_group_count = sum(1 for count in Counter(exact_hashes.values()).values() if count > 1)

    duplicate_groups = []
    near_duplicate_group_count = 0
    for members in groups:
        category = _group_similarity_category(members, exact_hashes, distance, threshold)
        if category != "Exact":
            near_duplicate_group_count += 1
        duplicate_groups.append(
            DuplicateGroup(
                members=members,
                similarity_category=category,
                keep=suggest_keep(members),
            )
        )

    return exact_group_count, near_duplicate_group_count, duplicate_groups


@click.command()
@click.argument("folder", type=click.Path(path_type=Path))
@click.option(
    "--threshold",
    type=click.IntRange(min=0),
    default=DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    show_default=True,
    help="Maximum Hamming distance for two images to count as near-duplicates.",
)
def main(folder: Path, threshold: int) -> None:
    try:
        exact_count, near_duplicate_group_count, duplicate_groups = run(folder, threshold)
    except ScanTargetError as error:
        click.echo(f"Error: {error}", err=True)
        sys.exit(1)

    skipped = skipped_image_files(folder)
    if skipped:
        counts = Counter(path.suffix.lower() for path in skipped)
        details = ", ".join(f"{extension}: {count}" for extension, count in sorted(counts.items()))
        noun = "image file" if len(skipped) == 1 else "image files"
        scanned = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        click.echo(
            f"Warning: skipped {len(skipped)} {noun} in formats this tool does not read "
            f"({details}). Only {scanned} are scanned.",
            err=True,
        )

    output_path = folder.resolve().parent / _report_filename(datetime.now())
    if output_path.exists():
        click.confirm(
            f"{output_path} already exists. Overwrite it?",
            default=False,
            abort=True,
        )
    write_report(duplicate_groups, output_path)
    click.echo(
        f"{exact_count} exact duplicates found, "
        f"{near_duplicate_group_count} near-duplicate groups found."
    )

