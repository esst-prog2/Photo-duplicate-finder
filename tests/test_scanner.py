import pytest

from find_duplicates.scanner import ScanTargetError, scan_folder


def test_only_supported_extensions_are_included(tmp_path):
    (tmp_path / "photo.jpg").write_bytes(b"jpg-bytes")
    (tmp_path / "photo.png").write_bytes(b"png-bytes")
    (tmp_path / "notes.txt").write_bytes(b"text")
    (tmp_path / "anim.gif").write_bytes(b"gif-bytes")

    result = scan_folder(tmp_path)

    assert {p.name for p in result} == {"photo.jpg", "photo.png"}


def test_subfolder_contents_are_excluded(tmp_path):
    (tmp_path / "top.jpg").write_bytes(b"top-bytes")
    subfolder = tmp_path / "nested"
    subfolder.mkdir()
    (subfolder / "inner.jpg").write_bytes(b"inner-bytes")

    result = scan_folder(tmp_path)

    assert {p.name for p in result} == {"top.jpg"}


def test_empty_folder_returns_empty_list(tmp_path):
    result = scan_folder(tmp_path)

    assert result == []


def test_missing_path_raises_scan_target_error(tmp_path):
    missing = tmp_path / "does-not-exist"

    with pytest.raises(ScanTargetError):
        scan_folder(missing)


def test_path_is_a_file_raises_scan_target_error(tmp_path):
    file_path = tmp_path / "photo.jpg"
    file_path.write_bytes(b"jpg-bytes")

    with pytest.raises(ScanTargetError):
        scan_folder(file_path)
