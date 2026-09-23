from pathlib import Path

from find_duplicates.hashing import exact_hash, group_by_exact_hash

FIXTURES = Path(__file__).parent / "fixtures"


def test_identical_copy_hashes_equal_to_base():
    base_hash = exact_hash(FIXTURES / "base.png")
    copy_hash = exact_hash(FIXTURES / "base_identical_copy.png")

    assert base_hash == copy_hash


def test_unrelated_image_hashes_different_from_base():
    base_hash = exact_hash(FIXTURES / "base.png")
    unrelated_hash = exact_hash(FIXTURES / "unrelated.png")

    assert base_hash != unrelated_hash


def test_group_by_exact_hash_groups_only_identical_files():
    base = FIXTURES / "base.png"
    identical_copy = FIXTURES / "base_identical_copy.png"
    resized = FIXTURES / "base_resized.png"
    unrelated = FIXTURES / "unrelated.png"

    groups = group_by_exact_hash([base, identical_copy, resized, unrelated])

    assert len(groups) == 1
    assert set(groups[0]) == {base, identical_copy}
