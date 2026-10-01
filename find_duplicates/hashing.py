import hashlib
from pathlib import Path

import imagehash
from PIL import Image


def exact_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def group_by_exact_hash(files: list[Path]) -> list[list[Path]]:
    groups: dict[str, list[Path]] = {}
    for file in files:
        groups.setdefault(exact_hash(file), []).append(file)
    return [group for group in groups.values() if len(group) > 1]


def perceptual_hash(path: Path) -> imagehash.ImageHash:
    with Image.open(path) as img:
        return imagehash.average_hash(img)


def hamming_distance(hash_a: imagehash.ImageHash, hash_b: imagehash.ImageHash) -> int:
    return hash_a - hash_b


DEFAULT_NEAR_DUPLICATE_THRESHOLD = 5


def is_near_duplicate(
    hash_a: imagehash.ImageHash,
    hash_b: imagehash.ImageHash,
    threshold: int = DEFAULT_NEAR_DUPLICATE_THRESHOLD,
) -> bool:
    return bool(hamming_distance(hash_a, hash_b) <= threshold)
