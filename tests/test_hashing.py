from pathlib import Path

from PIL import Image

from find_duplicates.hashing import (
    DEFAULT_NEAR_DUPLICATE_THRESHOLD,
    exact_hash,
    hamming_distance,
    perceptual_hash,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_identical_copy_hashes_equal_to_base():
    base_hash = exact_hash(FIXTURES / "base.jpg")
    copy_hash = exact_hash(FIXTURES / "base_identical_copy.jpg")

    assert base_hash == copy_hash


def test_unrelated_image_hashes_different_from_base():
    base_hash = exact_hash(FIXTURES / "base.jpg")
    unrelated_hash = exact_hash(FIXTURES / "unrelated.jpg")

    assert base_hash != unrelated_hash


def test_perceptual_hash_of_image_against_itself_has_zero_distance():
    base_hash = perceptual_hash(FIXTURES / "base.jpg")

    assert hamming_distance(base_hash, base_hash) == 0


def test_resized_copy_is_within_the_default_threshold_of_base():
    base_hash = perceptual_hash(FIXTURES / "base.jpg")
    resized_hash = perceptual_hash(FIXTURES / "base_resized.jpg")

    assert hamming_distance(base_hash, resized_hash) <= DEFAULT_NEAR_DUPLICATE_THRESHOLD


def test_unrelated_image_is_outside_the_default_threshold_of_base():
    base_hash = perceptual_hash(FIXTURES / "base.jpg")
    unrelated_hash = perceptual_hash(FIXTURES / "unrelated.jpg")

    assert hamming_distance(base_hash, unrelated_hash) > DEFAULT_NEAR_DUPLICATE_THRESHOLD


def test_hamming_distance_is_a_plain_int():
    base_hash = perceptual_hash(FIXTURES / "base.jpg")
    unrelated_hash = perceptual_hash(FIXTURES / "unrelated.jpg")

    assert type(hamming_distance(base_hash, unrelated_hash)) is int


def test_photo_stored_with_an_orientation_tag_hashes_like_the_upright_photo(tmp_path):
    # The same visible photo, stored the way a phone does it: the pixels are turned
    # 90 degrees and an EXIF tag (Orientation = 6) tells viewers to turn them back.
    with Image.open(FIXTURES / "base.jpg") as source:
        upright = source.convert("RGB")
    upright.save(tmp_path / "upright.jpg", quality=90)
    exif = Image.Exif()
    exif[0x0112] = 6
    upright.rotate(90, expand=True).save(tmp_path / "tagged.jpg", quality=90, exif=exif)

    distance = hamming_distance(
        perceptual_hash(tmp_path / "upright.jpg"), perceptual_hash(tmp_path / "tagged.jpg")
    )

    assert distance <= DEFAULT_NEAR_DUPLICATE_THRESHOLD
