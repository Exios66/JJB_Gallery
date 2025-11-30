# CHANGELOG

## [0.0.2] - 11-29-25

### Changed in v0.0.2

- Resolved Git repository corruption issues: Fixed corrupted remote references and missing object errors
- Improved repository organization: Moved all macOS resource fork files (._* files) to Xtra_Copies directory

### Fixed in v0.0.2

- Repository corruption: Resolved issues with corrupted refs/remotes/origin/gh-pages and missing Git objects
- File organization: Cleaned up macOS metadata files by consolidating them in Xtra_Copies
- Dependency Management: Resolved Python environment corruption caused by disk space exhaustion; recreated virtual environment and reinstalled all dependencies
- Documentation: Fixed Table of Contents overlay issue in index.html by updating Quarto configuration

### Repository Configuration

- Updated .gitignore to ignore macOS resource fork files (._*) and .DS_Store files
- Removed all tracked ._* files from Git repository

## [0.0.1] - 11-21-25

### Added in v0.0.1

- Added project subdirectory
- Added Jupyter notebooks of both pandas and SciKit Learn essentials.
- Added a Quarto document on the essentials underlying the random forest algorithm.
- Added a Quarto document on the random forest algorithm in practice.
- Added a script to render the random forest document to a html and pdf file.
- Added a script to start a preview server for the random forest document.
- Enhanced documentation and structure: Added Quarto document on random forest application, updated CHANGELOG, modified index.html for improved responsiveness, and expanded CrewAI project README with detailed agent swarm descriptions.

## [0.0.0] - 2025-11-21

### Added in v0.0.0

#### Initial release

- Added requirements.txt with the following dependencies:
  - numpy
  - pandas
  - seaborn
  - matplotlib
  - scikit-learn

- Added .gitignore
- Improved README documentation

### Changed

- N/A

### Removed

- N/A
