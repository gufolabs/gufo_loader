---
hide:
    - navigation
---
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To see unreleased changes, please see the [CHANGELOG on the master branch](https://github.com/gufolabs/gufo_loader/blob/master/CHANGELOG.md) guide.

## Unreleased

### Added

* Python 3.13 support.
* docs: Fancy front page.

## Removed

* Dropping Python 3.8 support

### Infrastructure

* devcontainer: Move settings to `customizations.vscode.settings`
* devcontainer: Python 3.13
* Ruff 0.11.2
* mypy 1.13.0
* mkdocs-material 9.4.8
* pytest 7.4.3
* coverage 7.3.2

## 1.0.3 - 2022-02-06

### Added

* `py.typed` file for PEP-561 compatibility
* docs: Supported standards
* Loader.__iter__() method.

## Changed

* docs: license.md renamed to LICENSE.md

### Infrastructure

* Adopt ruff
* Use `actions/checkout@v3`
* Use `actions/cache@v3`
* Project structure tests
* CI workflows tests
* Extend licence copyright years
* Dockerfile: Use `set -x` to log RUN commands
* docs: Use common Gufo Labs mkdocs plugins set

## 1.0.2 - 2022-11-06

### Added

* Python 3.11 support
* Add CITATION.cff
* Developer's Common Tasks

### Changed

* Move CHANGELOG.md to the project root

### Infrastructure

* Use Python 3.11 for dev container
* Use mkdocs-material 3.5.8
* Use pytest 7.2.0
* Use python-coverage 6.5.0

## 1.0.1 - 2022-04-15

### Added

* `__version__` attribute.

## 1.0.0 - 2022-03-03

### Added

* Initial implementation.