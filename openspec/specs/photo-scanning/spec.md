# photo-scanning Specification

## Purpose
Discovers the set of image files within a single target folder that the rest of the
pipeline (hashing, grouping, reporting) will operate on.

## Requirements

### Requirement: Scan a single folder for supported image files
The system SHALL scan exactly the folder given on the command line and SHALL NOT
descend into subfolders. Only files with a `.jpg` or `.png` extension are supported,
and the extension SHALL be matched case-insensitively (so `PHOTO.JPG` is supported).

#### Scenario: Folder contains supported and unsupported files
- **WHEN** the target folder contains `.jpg`, `.png`, and other files (e.g. `.txt`, `.gif`)
- **THEN** only the `.jpg` and `.png` files are included in the scan results

#### Scenario: Extensions in capital letters
- **WHEN** the target folder contains `PHOTO.JPG` and `Scan.PNG`
- **THEN** both files are included in the scan results

#### Scenario: Folder contains subfolders
- **WHEN** the target folder contains a subfolder that itself contains `.jpg` files
- **THEN** the files inside the subfolder are not included in the scan results

#### Scenario: Folder has no matching images
- **WHEN** the target folder exists but is empty, or contains no `.jpg`/`.png` files
- **THEN** the scan completes with an empty result (not an error), and the rest of
  the pipeline proceeds to report zero duplicate groups

### Requirement: Say when image files are skipped
The system SHALL NOT silently ignore image files in a format it does not read. When
the target folder contains files with a common image extension other than `.jpg`
and `.png` (for example `.jpeg`, `.heic`, `.gif` or `.webp`), the system SHALL print
a warning to the error stream saying how many such files were skipped and how many
there were of each extension, and SHALL otherwise finish normally, with the same
summary, report and exit status. Files that are not images (for example `.txt`) are
skipped without a warning.

#### Scenario: Image files in formats that are not read
- **WHEN** the target folder contains `kept.jpg`, `phone.jpeg` and two `.heic` files
- **THEN** the system prints a warning to the error stream that 3 image files were
  skipped (`.heic`: 2, `.jpeg`: 1), and still prints the summary and exits normally

#### Scenario: Only files that are not images are skipped
- **WHEN** the target folder contains only `notes.txt`
- **THEN** the system prints no warning

### Requirement: Report an error for an invalid target
The system SHALL fail with a clear error message if the given path does not exist or
is not a folder.

#### Scenario: Path does not exist
- **WHEN** the user runs the CLI with a path that does not exist
- **THEN** the system prints an error message identifying the invalid path and exits
  without writing a report

#### Scenario: Path is a file, not a folder
- **WHEN** the user runs the CLI with a path that points to a file
- **THEN** the system prints an error message and exits without writing a report
