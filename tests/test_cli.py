from pathlib import Path

from click.testing import CliRunner
from openpyxl import load_workbook

from find_duplicates.cli import _categorize_distance, _group_similarity_score, main
from find_duplicates.hashing import DEFAULT_NEAR_DUPLICATE_THRESHOLD

FIXTURES = Path(__file__).parent / "fixtures"


def test_empty_folder_exits_cleanly_with_zero_counts(tmp_path):
    empty_folder = tmp_path / "photos"
    empty_folder.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [str(empty_folder)])

    assert result.exit_code == 0
    assert result.output.strip() == "0 exact duplicates found, 0 near-duplicate groups found."

    report_path = tmp_path / "duplicates.xlsx"
    assert report_path.exists()
    sheet = load_workbook(report_path).active
    assert sheet.max_row == 1
    assert sheet.cell(row=1, column=1).value is None


def test_categorize_distance_at_and_below_midpoint_is_very_similar():
    assert _categorize_distance(0, threshold=5) == "Very Similar"
    assert _categorize_distance(2, threshold=5) == "Very Similar"


def test_categorize_distance_above_midpoint_is_similar():
    assert _categorize_distance(3, threshold=5) == "Similar"
    assert _categorize_distance(5, threshold=5) == "Similar"


def test_group_similarity_score_for_exact_duplicates_is_exact():
    base = FIXTURES / "base.png"
    identical_copy = FIXTURES / "base_identical_copy.png"

    score = _group_similarity_score([base, identical_copy], DEFAULT_NEAR_DUPLICATE_THRESHOLD)

    assert score == "Exact"


def test_group_similarity_score_for_resized_copy_is_very_similar():
    base = FIXTURES / "base.png"
    resized = FIXTURES / "base_resized.png"

    score = _group_similarity_score([base, resized], DEFAULT_NEAR_DUPLICATE_THRESHOLD)

    assert score == "Very Similar"


def test_group_similarity_score_for_mixed_exact_and_near_group_is_not_exact():
    base = FIXTURES / "base.png"
    identical_copy = FIXTURES / "base_identical_copy.png"
    resized = FIXTURES / "base_resized.png"

    # base and identical_copy are exact duplicates, but resized only matches by
    # perceptual distance -- the group as a whole should not be labeled "Exact".
    score = _group_similarity_score(
        [base, identical_copy, resized], DEFAULT_NEAR_DUPLICATE_THRESHOLD
    )

    assert score != "Exact"


def test_folder_with_no_matching_images_exits_cleanly_with_zero_counts(tmp_path):
    folder = tmp_path / "photos"
    folder.mkdir()
    (folder / "notes.txt").write_text("not an image")

    runner = CliRunner()
    result = runner.invoke(main, [str(folder)])

    assert result.exit_code == 0
    assert result.output.strip() == "0 exact duplicates found, 0 near-duplicate groups found."

    report_path = tmp_path / "duplicates.xlsx"
    assert report_path.exists()
    sheet = load_workbook(report_path).active
    assert sheet.max_row == 1
    assert sheet.cell(row=1, column=1).value is None
