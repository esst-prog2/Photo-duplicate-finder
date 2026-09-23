from pathlib import Path

SUPPORTED_EXTENSIONS = {".jpg", ".png"}


class ScanTargetError(Exception):
    """Raised when the folder to scan does not exist or is not a directory."""


def scan_folder(folder: Path) -> list[Path]:
    folder = Path(folder)
    if not folder.exists():
        raise ScanTargetError(f"Folder not found: {folder}")
    if not folder.is_dir():
        raise ScanTargetError(f"Not a folder: {folder}")
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
