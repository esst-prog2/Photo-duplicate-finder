from pathlib import Path

from openpyxl import load_workbook
from PIL import Image

from find_duplicates.report import KEEP_FILL, DuplicateGroup, choose_keep, write_report

FIXTURES = Path(__file__).parent / "fixtures"


def test_real_photo_keeps_the_larger_higher_resolution_original():
    base = FIXTURES / "base.jpg"
    resized = FIXTURES / "base_resized.jpg"

    assert base.stat().st_size > resized.stat().st_size
    with Image.open(base) as base_img, Image.open(resized) as resized_img:
        assert (base_img.width * base_img.height) > (resized_img.width * resized_img.height)

    assert choose_keep([base, resized]) == base


def test_largest_file_size_wins_even_with_lower_resolution(tmp_path):
    # A small, low-resolution image padded to be the larger file, vs a bigger,
    # higher-resolution image that happens to compress smaller -- file size
    # takes priority over resolution per the keep-candidate rule.
    small_resolution = Image.new("RGB", (50, 50), color=(10, 20, 30))
    large_resolution = Image.new("RGB", (200, 200), color=(10, 20, 30))
    small_path = tmp_path / "small_resolution.png"
    large_path = tmp_path / "large_resolution.png"
    small_resolution.save(small_path)
    large_resolution.save(large_path)

    size_diff = large_path.stat().st_size - small_path.stat().st_size + 1
    with open(small_path, "ab") as f:
        f.write(b"\x00" * max(size_diff, 0))
    assert small_path.stat().st_size > large_path.stat().st_size

    assert choose_keep([small_path, large_path]) == small_path


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


def test_write_report_writes_one_table_per_group_with_blank_row_between(tmp_path):
    base = FIXTURES / "base.jpg"
    resized = FIXTURES / "base_resized.jpg"
    unrelated = FIXTURES / "unrelated.jpg"
    groups = [
        DuplicateGroup(members=[base, resized], similarity_score="Very Similar", keep=resized),
        DuplicateGroup(members=[base, unrelated], similarity_score="Similar", keep=base),
    ]
    output_path = tmp_path / "duplicates.xlsx"

    write_report(groups, output_path)

    sheet = load_workbook(output_path).active
    rows = [tuple(cell.value for cell in row) for row in sheet.iter_rows(max_col=2)]

    assert rows == [
        ("File", "Similarity Score"),
        ("base.jpg", "Very Similar"),
        ("base_resized.jpg", "Very Similar"),
        (None, None),
        ("File", "Similarity Score"),
        ("base.jpg", "Similar"),
        ("unrelated.jpg", "Similar"),
    ]


def test_write_report_highlights_the_keep_row(tmp_path):
    base = FIXTURES / "base.jpg"
    resized = FIXTURES / "base_resized.jpg"
    groups = [DuplicateGroup(members=[base, resized], similarity_score="Very Similar", keep=resized)]
    output_path = tmp_path / "duplicates.xlsx"

    write_report(groups, output_path)

    sheet = load_workbook(output_path).active
    # Row 2 is base.jpg (not kept), row 3 is base_resized.jpg (kept).
    assert sheet.cell(row=2, column=1).fill.start_color.rgb != KEEP_FILL.start_color.rgb
    assert sheet.cell(row=3, column=1).fill.start_color.rgb == KEEP_FILL.start_color.rgb
    assert sheet.cell(row=3, column=2).fill.start_color.rgb == KEEP_FILL.start_color.rgb


def test_write_report_with_no_groups_creates_valid_empty_workbook(tmp_path):
    output_path = tmp_path / "duplicates.xlsx"

    write_report([], output_path)

    assert output_path.exists()
    sheet = load_workbook(output_path).active
    assert sheet.max_row == 1
    assert sheet.cell(row=1, column=1).value is None
