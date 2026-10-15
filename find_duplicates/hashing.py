import hashlib
from pathlib import Path

import imagehash
from PIL import Image, ImageOps


def exact_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


PERCEPTUAL_HASH_SIZE = 7


def perceptual_hash(path: Path) -> imagehash.ImageHash:
    with Image.open(path) as img:
        return imagehash.phash(ImageOps.exif_transpose(img), hash_size=PERCEPTUAL_HASH_SIZE)


def hamming_distance(hash_a: imagehash.ImageHash, hash_b: imagehash.ImageHash) -> int:
    return int(hash_a - hash_b)


DEFAULT_NEAR_DUPLICATE_THRESHOLD = 8
