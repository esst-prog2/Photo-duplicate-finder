from pathlib import Path

import imagehash
import numpy as np

from find_duplicates.hashing import (
    exact_hash,
    find_near_duplicate_pairs,
    group_by_exact_hash,
    hamming_distance,
    is_near_duplicate,
    perceptual_hash,
)

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


def test_perceptual_hash_of_image_against_itself_has_zero_distance():
    base_hash = perceptual_hash(FIXTURES / "base.png")

    assert hamming_distance(base_hash, base_hash) == 0


def test_custom_threshold_changes_match_decision_for_borderline_case():
    hash_a = imagehash.ImageHash(np.zeros((8, 8), dtype=bool))
    bits = np.zeros((8, 8), dtype=bool)
    bits[0, 0] = True
    bits[0, 1] = True
    bits[0, 2] = True
    hash_b = imagehash.ImageHash(bits)
    assert hamming_distance(hash_a, hash_b) == 3

    assert is_near_duplicate(hash_a, hash_b, threshold=5) is True
    assert is_near_duplicate(hash_a, hash_b, threshold=2) is False


def test_default_threshold_is_used_when_none_given():
    hash_a = imagehash.ImageHash(np.zeros((8, 8), dtype=bool))
    hash_b = imagehash.ImageHash(np.zeros((8, 8), dtype=bool))

    assert is_near_duplicate(hash_a, hash_b) is True


def test_resized_copy_is_a_near_duplicate_of_base_at_default_threshold():
    base_hash = perceptual_hash(FIXTURES / "base.png")
    resized_hash = perceptual_hash(FIXTURES / "base_resized.png")

    assert is_near_duplicate(base_hash, resized_hash) is True


def test_unrelated_image_is_not_a_near_duplicate_of_base_at_default_threshold():
    base_hash = perceptual_hash(FIXTURES / "base.png")
    unrelated_hash = perceptual_hash(FIXTURES / "unrelated.png")

    assert is_near_duplicate(base_hash, unrelated_hash) is False


def test_exact_duplicate_pairs_are_excluded_from_near_duplicate_pairs():
    base = FIXTURES / "base.png"
    identical_copy = FIXTURES / "base_identical_copy.png"
    resized = FIXTURES / "base_resized.png"
    unrelated = FIXTURES / "unrelated.png"

    # base and identical_copy are perceptually identical too (distance 0), so
    # without the exclusion they would also show up as a near-duplicate pair.
    pairs = find_near_duplicate_pairs([base, identical_copy, resized, unrelated])

    assert (base, identical_copy) not in pairs
    assert (base, resized) in pairs
    assert (identical_copy, resized) in pairs
    assert not any(unrelated in pair for pair in pairs)
