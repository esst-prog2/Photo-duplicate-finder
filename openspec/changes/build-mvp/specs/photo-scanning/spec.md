## Purpose

Discovers the set of image files within a single target folder that the rest of the
pipeline (hashing, grouping, reporting) will operate on.

## ADDED Requirements

### Requirement: Scan a single folder for supported image files
The system SHALL scan exactly the folder given on the command line and SHALL NOT
descend into subfolders.

#### Scenario: Folder contains supported and unsupported files
- **WHEN** the target folder contains `.jpg`, `.png`, and other files (e.g. `.txt`, `.gif`)
- **THEN** only the `.jpg` and `.png` files are included in the scan results

#### Scenario: Folder contains subfolders
- **WHEN** the target folder contains a subfolder that itself contains `.jpg` files
- **THEN** the files inside the subfolder are not included in the scan results

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
