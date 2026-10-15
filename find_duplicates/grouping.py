from collections.abc import Callable
from pathlib import Path


def group_by_threshold(
    files: list[Path],
    distance: Callable[[Path, Path], int],
    threshold: int,
) -> list[list[Path]]:
    assigned: set[Path] = set()
    groups: list[list[Path]] = []

    for file in files:
        if file in assigned:
            continue
        members = [file]
        assigned.add(file)
        for other in files:
            if other in assigned:
                continue
            if all(distance(other, member) <= threshold for member in members):
                members.append(other)
                assigned.add(other)
        if len(members) > 1:
            groups.append(members)

    return groups
