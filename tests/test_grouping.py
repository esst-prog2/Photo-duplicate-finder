from pathlib import Path

from find_duplicates.grouping import cluster_by_threshold


def _distance_from_table(table: dict[frozenset, int]):
    def distance(a: Path, b: Path) -> int:
        if a == b:
            return 0
        return table[frozenset({a, b})]

    return distance


def test_two_files_within_threshold_form_one_group():
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    distance = _distance_from_table({frozenset({file_a, file_b}): 2})

    groups = cluster_by_threshold([file_a, file_b], distance, threshold=5)

    assert len(groups) == 1
    assert set(groups[0]) == {file_a, file_b}


def test_unrelated_files_produce_no_groups():
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    distance = _distance_from_table({frozenset({file_a, file_b}): 20})

    groups = cluster_by_threshold([file_a, file_b], distance, threshold=5)

    assert groups == []


def test_disjoint_matches_produce_separate_groups():
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    file_c = Path("c.jpg")
    file_d = Path("d.jpg")
    distance = _distance_from_table(
        {
            frozenset({file_a, file_b}): 1,
            frozenset({file_c, file_d}): 1,
            frozenset({file_a, file_c}): 20,
            frozenset({file_a, file_d}): 20,
            frozenset({file_b, file_c}): 20,
            frozenset({file_b, file_d}): 20,
        }
    )

    groups = cluster_by_threshold([file_a, file_b, file_c, file_d], distance, threshold=5)

    assert len(groups) == 2
    group_sets = {frozenset(group) for group in groups}
    assert group_sets == {frozenset({file_a, file_b}), frozenset({file_c, file_d})}


def test_exact_duplicate_merges_into_a_near_duplicate_clique():
    # A and B are exact duplicates (distance 0); B and C are near-duplicates
    # (distance 3, within threshold). By the triangle inequality, A-C can be at
    # most 0 + 3 = 3, also within threshold, so all three correctly form one group.
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    file_c = Path("c.jpg")
    distance = _distance_from_table(
        {
            frozenset({file_a, file_b}): 0,
            frozenset({file_b, file_c}): 3,
            frozenset({file_a, file_c}): 3,
        }
    )

    groups = cluster_by_threshold([file_a, file_b, file_c], distance, threshold=5)

    assert len(groups) == 1
    assert set(groups[0]) == {file_a, file_b, file_c}


def test_chain_whose_ends_are_not_similar_is_not_merged_into_one_group():
    # A-B, B-C, C-D are each within threshold (3 <= 5), but A-D is far outside it
    # (9 > 5). Single-linkage/transitive-closure grouping would incorrectly merge
    # all four into one group; clique-bounded grouping must not.
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    file_c = Path("c.jpg")
    file_d = Path("d.jpg")
    distance = _distance_from_table(
        {
            frozenset({file_a, file_b}): 3,
            frozenset({file_b, file_c}): 3,
            frozenset({file_c, file_d}): 3,
            frozenset({file_a, file_c}): 6,
            frozenset({file_b, file_d}): 6,
            frozenset({file_a, file_d}): 9,
        }
    )

    groups = cluster_by_threshold([file_a, file_b, file_c, file_d], distance, threshold=5)

    for group in groups:
        assert not ({file_a, file_d} <= set(group))
