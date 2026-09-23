from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from openpyxl import load_workbook

from find_duplicates.cli import (
    _categorize_distance,
    _group_similarity_score,
    _report_filename,
    main,
)
from find_duplicates.hashing import DEFAULT_NEAR_DUPLICATE_THRESHOLD

FIXTURES = Path(__file__).parent / "fixtures"


def test_report_filename_includes_date_and_time_to_the_minute():
    now = datetime(2026, 9, 23, 14, 5)

    assert _report_filename(now) == "duplicates_20260923_1405.xlsx"


def test_empty_folder_exits_cleanly_with_zero_counts(tmp_path):
    empty_folder = tmp_path / "photos"
    empty_folder.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [str(empty_folder)])

    assert result.exit_code == 0
    assert result.output.strip() == "0 exact duplicates found, 0 near-duplicate groups found."

    report_paths = list(tmp_path.glob("duplicates_*.xlsx"))
    assert len(report_paths) == 1
    sheet = load_workbook(report_paths[0]).active
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


def test_no_overwrite_prompt_when_target_filename_does_not_exist(tmp_path):
    folder = tmp_path / "photos"
    folder.mkdir()

    with patch("find_duplicates.cli.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 9, 23, 14, 5)
        runner = CliRunner()
        # No `input=` given: if a prompt were wrongly triggered, reading from
        # empty stdin would abort the command and exit_code would be non-zero.
        result = runner.invoke(main, [str(folder)])

    assert result.exit_code == 0
    assert "already exists" not in result.output
    report_path = tmp_path / _report_filename(datetime(2026, 9, 23, 14, 5))
    assert report_path.exists()


def test_declining_overwrite_prompt_aborts_without_writing(tmp_path):
    folder = tmp_path / "photos"
    folder.mkdir()
    existing_report = tmp_path / _report_filename(datetime(2026, 9, 23, 14, 5))
    existing_report.write_text("pre-existing content")

    with patch("find_duplicates.cli.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 9, 23, 14, 5)
        runner = CliRunner()
        result = runner.invoke(main, [str(folder)], input="n\n")

    assert result.exit_code != 0
    assert "already exists" in result.output
    assert existing_report.read_text() == "pre-existing content"


def test_confirming_overwrite_prompt_replaces_the_existing_file(tmp_path):
    folder = tmp_path / "photos"
    folder.mkdir()
    existing_report = tmp_path / _report_filename(datetime(2026, 9, 23, 14, 5))
    existing_report.write_text("pre-existing content")

    with patch("find_duplicates.cli.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 9, 23, 14, 5)
        runner = CliRunner()
        result = runner.invoke(main, [str(folder)], input="y\n")

    assert result.exit_code == 0
    assert "already exists" in result.output
    sheet = load_workbook(existing_report).active
    assert sheet.max_row == 1
    assert sheet.cell(row=1, column=1).value is None


def test_folder_with_no_matching_images_exits_cleanly_with_zero_counts(tmp_path):
    folder = tmp_path / "photos"
    folder.mkdir()
    (folder / "notes.txt").write_text("not an image")

    runner = CliRunner()
    result = runner.invoke(main, [str(folder)])

    assert result.exit_code == 0
    assert result.output.strip() == "0 exact duplicates found, 0 near-duplicate groups found."

    report_paths = list(tmp_path.glob("duplicates_*.xlsx"))
    assert len(report_paths) == 1
    sheet = load_workbook(report_paths[0]).active
    assert sheet.max_row == 1
    assert sheet.cell(row=1, column=1).value is None
