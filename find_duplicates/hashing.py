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


def find_near_duplicate_pairs(
    files: list[Path],
    threshold: int = DEFAULT_NEAR_DUPLICATE_THRESHOLD,
) -> list[tuple[Path, Path]]:
    exact_hashes = {file: exact_hash(file) for file in files}
    perceptual_hashes = {file: perceptual_hash(file) for file in files}

    pairs = []
    for i, file_a in enumerate(files):
        for file_b in files[i + 1 :]:
            if exact_hashes[file_a] == exact_hashes[file_b]:
                continue
            if is_near_duplicate(perceptual_hashes[file_a], perceptual_hashes[file_b], threshold):
                pairs.append((file_a, file_b))
    return pairs
