import sys
from datetime import datetime
from itertools import combinations
from pathlib import Path

import click
import imagehash

from find_duplicates.grouping import cluster_by_threshold
from find_duplicates.hashing import (
    DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    exact_hash,
    group_by_exact_hash,
    hamming_distance,
    perceptual_hash,
)
from find_duplicates.report import DuplicateGroup, choose_keep, write_report
from find_duplicates.scanner import ScanTargetError, scan_folder


def _categorize_distance(distance: int, threshold: int) -> str:
    return "Very Similar" if distance <= threshold // 2 else "Similar"


def _group_similarity_score(
    members: list[Path],
    exact_hashes: dict[Path, str],
    perceptual_hashes: dict[Path, imagehash.ImageHash],
    threshold: int,
) -> str:
    if len({exact_hashes[member] for member in members}) == 1:
        return "Exact"

    max_distance = max(
        (
            hamming_distance(perceptual_hashes[members[i]], perceptual_hashes[members[j]])
            for i, j in combinations(range(len(members)), 2)
        ),
        default=0,
    )
    return _categorize_distance(max_distance, threshold)


def _report_filename(now: datetime) -> str:
    return now.strftime("duplicates_%Y%m%d_%H%M.xlsx")


def run(folder: Path, threshold: int) -> tuple[int, int, list[DuplicateGroup]]:
    files = scan_folder(folder)

    exact_hashes = {file: exact_hash(file) for file in files}
    perceptual_hashes = {file: perceptual_hash(file) for file in files}

    def distance(file_a: Path, file_b: Path) -> int:
        return hamming_distance(perceptual_hashes[file_a], perceptual_hashes[file_b])

    groups = cluster_by_threshold(files, distance, threshold)
    exact_group_count = len(group_by_exact_hash(files))

    duplicate_groups = []
    near_duplicate_group_count = 0
    for members in groups:
        score = _group_similarity_score(members, exact_hashes, perceptual_hashes, threshold)
        if score != "Exact":
            near_duplicate_group_count += 1
        duplicate_groups.append(
            DuplicateGroup(
                members=members,
                similarity_score=score,
                keep=choose_keep(members),
            )
        )

    return exact_group_count, near_duplicate_group_count, duplicate_groups


@click.command()
@click.argument("folder", type=click.Path(path_type=Path))
@click.option(
    "--threshold",
    type=int,
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

    output_path = folder.parent / _report_filename(datetime.now())
    if output_path.exists():
        click.confirm(
            f"{output_path} already exists. Overwrite it?",
            abort=True,
        )
    write_report(duplicate_groups, output_path)
    click.echo(
        f"{exact_count} exact duplicates found, "
        f"{near_duplicate_group_count} near-duplicate groups found."
    )


if __name__ == "__main__":
    main()
