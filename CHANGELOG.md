# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To see unreleased changes, please see the [CHANGELOG on the master branch](https://github.com/gufolabs/gufo_loader/blob/master/CHANGELOG.md) guide.

## [Unreleased]

### Added

* `py.typed` file for PEP-561 compatibility
* docs: Supported standards

### Infrastructure

* Use `actions/checkout@v3`
* Use `actions/cache@v3`
* Project structure tests
* CI workflows tests
* Extend licence copyright years
* Dockerfile: Use `set -x` to log RUN commands

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