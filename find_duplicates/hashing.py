import hashlib
from pathlib import Path


def exact_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def group_by_exact_hash(files: list[Path]) -> list[list[Path]]:
    groups: dict[str, list[Path]] = {}
    for file in files:
        groups.setdefault(exact_hash(file), []).append(file)
    return [group for group in groups.values() if len(group) > 1]
