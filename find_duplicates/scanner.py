from pathlib import Path

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
UNREAD_IMAGE_EXTENSIONS = {".heic", ".heif", ".gif", ".bmp", ".tif", ".tiff", ".webp"}


class ScanTargetError(Exception):
    """Raised when the folder to scan does not exist or is not a directory."""


def _files_in(folder: Path) -> list[Path]:
    folder = Path(folder)
    if not folder.exists():
        raise ScanTargetError(f"Folder not found: {folder}")
    if not folder.is_dir():
        raise ScanTargetError(f"Not a folder: {folder}")
    return sorted(path for path in folder.iterdir() if path.is_file())


def scan_folder(folder: Path) -> list[Path]:
    return [path for path in _files_in(folder) if path.suffix.lower() in SUPPORTED_EXTENSIONS]


def skipped_image_files(folder: Path) -> list[Path]:
    return [path for path in _files_in(folder) if path.suffix.lower() in UNREAD_IMAGE_EXTENSIONS]
