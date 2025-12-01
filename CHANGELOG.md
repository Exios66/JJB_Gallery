# CHANGELOG

## [0.0.3] - 11-30-25

### Changed in v0.0.3

- Overhauled mathematical and explanatory sections for the random forest algorithm in `randomforest.qmd`; enhanced with formal model equations, clearer bootstrap sampling explanations, and updated diagrams.
- Revised the Quarto/Notebooks project structure to separate theoretical content from hands-on tutorials—enabling streamlined navigation between core concepts and practical walkthroughs.
- Unified environment dependencies across all Quarto documents and notebooks, adding robust setup scripts for reproducibility.
- Improved documentation linking—ensured that all new guides and references are indexed in navigation menus and README files for both accessibility and completeness.

### Fixed in v0.0.3

- Corrected previous path and reference inconsistencies in changelogs, Git protocol documentation, and associated navigation menus.
- Addressed outdated commands and formatting errors in Git workflow documentation; provided updated and tested CLIs and authentication instructions.
- Prevented possible documentation drift by automating file references and ensuring all new materials are reflected in existing indices.
- Resolved minor visual inconsistencies in mathematical notation and figure rendering in Quarto documents.
- Updated `.gitignore` and project settings to prevent accidental inclusion of generated or system files in the repository.

### Added in v0.0.3

- Added a new Quarto document (`randomforest.qmd`) detailing the mathematical foundations and practical application of the random forest algorithm—including model equations, bootstrapping explanations, visualizations, and end-to-end Python code for reproducible training, evaluation, and interpretation.
- Implemented an environment setup section in `randomforest.qmd` with robust dependency checking and installation routine.
- Expanded Quarto/Notebooks project structure to facilitate clear separation between math/theory and hands-on practical guides for machine learning algorithms.
- Added a comprehensive workflow guide: `docs/GIT_PROTOCOL_GUIDE.md`—includes best practices for using both SSH and HTTPS Git protocols, complete with command snippets, security recommendations, and branch management strategies.
- Added alternate Markdown version of the Git protocol guide as `docs/GIT_PROTOCOL_GUIDE 2.md` for compatibility.

### Improved in v0.0.3

- Updated breast cancer dataset example and documentation for clarity; enhanced narrative with explanatory footnotes and statistical justifications in the new Quarto documents.
- Improved project documentation by providing explicit instructions for Python environment setup and notebook/practical reproducibility.
- Applied new documentation standards to changelogs and guides for increased transparency and project maintainability.

### Fixed in v0.0.3

- Addressed confusions in environment configuration: clarified recommended dependency installation workflow to mitigate virtual environment corruption.
- Fixed prior documentation referencing errors regarding the location of project notebooks and Quarto docs in various READMEs.

### Repository Configuration

- Ensured all new documentation files are automatically referenced in the appropriate indexes and navigation menus.
- Updated `.gitignore` for consistency with recent changes and future growth of documentation subdirectories.

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
