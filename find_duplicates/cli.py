import sys
from datetime import datetime
from itertools import combinations
from pathlib import Path

import click

from find_duplicates.grouping import merge_duplicate_groups
from find_duplicates.hashing import (
    DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    exact_hash,
    find_near_duplicate_pairs,
    group_by_exact_hash,
    hamming_distance,
    perceptual_hash,
)
from find_duplicates.report import DuplicateGroup, choose_keep, write_report
from find_duplicates.scanner import ScanTargetError, scan_folder


def _categorize_distance(distance: int, threshold: int) -> str:
    return "Very Similar" if distance <= threshold // 2 else "Similar"


def _group_similarity_score(members: list[Path], threshold: int) -> str:
    exact_hashes = [exact_hash(member) for member in members]
    if len(set(exact_hashes)) == 1:
        return "Exact"

    hashes = [perceptual_hash(member) for member in members]
    max_distance = max(
        (hamming_distance(hashes[i], hashes[j]) for i, j in combinations(range(len(hashes)), 2)),
        default=0,
    )
    return _categorize_distance(max_distance, threshold)


def _report_filename(now: datetime) -> str:
    return now.strftime("duplicates_%Y%m%d_%H%M.xlsx")


def run(folder: Path, threshold: int) -> tuple[int, int, list[DuplicateGroup]]:
    files = scan_folder(folder)

    exact_groups = group_by_exact_hash(files)
    near_duplicate_pairs = find_near_duplicate_pairs(files, threshold=threshold)
    merged_groups = merge_duplicate_groups(files, exact_groups, near_duplicate_pairs)

    near_duplicate_member_pairs = {frozenset(pair) for pair in near_duplicate_pairs}

    duplicate_groups = []
    near_duplicate_group_count = 0
    for members in merged_groups:
        has_near_duplicate_pair = any(
            frozenset(pair) in near_duplicate_member_pairs for pair in combinations(members, 2)
        )
        if has_near_duplicate_pair:
            near_duplicate_group_count += 1
        duplicate_groups.append(
            DuplicateGroup(
                members=members,
                similarity_score=_group_similarity_score(members, threshold),
                keep=choose_keep(members),
            )
        )

    return len(exact_groups), near_duplicate_group_count, duplicate_groups


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
