import csv
from pathlib import Path

from PIL import Image

from find_duplicates.report import DuplicateGroup, choose_keep, write_report

FIXTURES = Path(__file__).parent / "fixtures"


def test_largest_file_size_wins_even_with_lower_resolution():
    base = FIXTURES / "base.png"
    resized = FIXTURES / "base_resized.png"

    # base_resized.png has a lower resolution than base.png but a larger file
    # size (PNG compression of the downscaled image happens to be less
    # efficient here) -- file size takes priority over resolution.
    assert resized.stat().st_size > base.stat().st_size
    with Image.open(base) as base_img, Image.open(resized) as resized_img:
        assert (resized_img.width * resized_img.height) < (base_img.width * base_img.height)

    assert choose_keep([base, resized]) == resized


def test_tie_break_by_resolution_when_file_sizes_are_equal(tmp_path):
    small = Image.new("RGB", (50, 50), color=(10, 20, 30))
    large = Image.new("RGB", (200, 200), color=(10, 20, 30))
    small_path = tmp_path / "small.png"
    large_path = tmp_path / "large.png"
    small.save(small_path)
    large.save(large_path)

    size_diff = large_path.stat().st_size - small_path.stat().st_size
    assert size_diff >= 0
    with open(small_path, "ab") as f:
        f.write(b"\x00" * size_diff)
    assert small_path.stat().st_size == large_path.stat().st_size

    assert choose_keep([small_path, large_path]) == large_path


def test_write_report_writes_one_row_per_group(tmp_path):
    base = FIXTURES / "base.png"
    resized = FIXTURES / "base_resized.png"
    unrelated = FIXTURES / "unrelated.png"
    groups = [
        DuplicateGroup(members=[base, resized], similarity_score="exact", keep=base),
        DuplicateGroup(members=[base, unrelated], similarity_score="12", keep=base),
    ]
    output_path = tmp_path / "duplicates.csv"

    write_report(groups, output_path)

    with open(output_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0] == {
        "files": "base.png;base_resized.png",
        "similarity_score": "exact",
        "keep": "base.png",
    }
    assert rows[1] == {
        "files": "base.png;unrelated.png",
        "similarity_score": "12",
        "keep": "base.png",
    }


def test_write_report_with_no_groups_creates_header_only_csv(tmp_path):
    output_path = tmp_path / "duplicates.csv"

    write_report([], output_path)

    assert output_path.exists()
    with open(output_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows == []
