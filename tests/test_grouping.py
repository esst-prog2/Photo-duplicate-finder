from pathlib import Path

from find_duplicates.grouping import merge_duplicate_groups


def test_transitive_match_merges_into_one_group():
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    file_c = Path("c.jpg")
    file_d = Path("d.jpg")

    # A and B are exact duplicates; B and C are near-duplicates; D is unrelated.
    groups = merge_duplicate_groups(
        files=[file_a, file_b, file_c, file_d],
        exact_groups=[[file_a, file_b]],
        near_duplicate_pairs=[(file_b, file_c)],
    )

    assert len(groups) == 1
    assert set(groups[0]) == {file_a, file_b, file_c}


def test_unrelated_files_produce_no_groups():
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")

    groups = merge_duplicate_groups(
        files=[file_a, file_b],
        exact_groups=[],
        near_duplicate_pairs=[],
    )

    assert groups == []


def test_disjoint_matches_produce_separate_groups():
    file_a = Path("a.jpg")
    file_b = Path("b.jpg")
    file_c = Path("c.jpg")
    file_d = Path("d.jpg")

    groups = merge_duplicate_groups(
        files=[file_a, file_b, file_c, file_d],
        exact_groups=[[file_a, file_b]],
        near_duplicate_pairs=[(file_c, file_d)],
    )

    assert len(groups) == 2
    group_sets = {frozenset(group) for group in groups}
    assert group_sets == {frozenset({file_a, file_b}), frozenset({file_c, file_d})}
