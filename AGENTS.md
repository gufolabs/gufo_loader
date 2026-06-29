# Gufo Loader - Project Reference for Agents

## Overview
**Gufo Loader** — generic Python class loader for robust plugin infrastructure. Part of [Gufo Stack](https://docs.gufolabs.com/) by Gufo Labs. Provides dict-like singleton API for late-loading plugins from one or many plugin packages. Supports three schemes: subclasses, singletons (instances), and protocols. Python >= 3.10. BSD-3-Clause.

## Architecture

### Core Engine
Source in `src/gufo/loader/`: Loader class module (`loader.py`), ImportPathResolver module (`resolver.py`) + exports (`__init__.py`). Max 3 files total.

**Loader[T]** — generic class implementing dict-like singleton loader (in `loader.py`):
- `__init__(base, bases, strict, exclude)` — base/bases mutually exclusive; both optional (neither = no error until validation). Sets `_paths` via `_iter_paths()`, initializes `_classes={}`, `_lock` (threading.RLock), `_exclude=set`.
- `_get_item_type()` → `T` — extracts generic type arg from `__orig_class__` via `get_args()`.
- `_get_validator()` → `Callable[[Any], bool]` — cached on `_validate`. Distinguishes Type[Class] (subclass validation) vs Class (instance validation).
- `_is_type(x)` — checks `get_origin(x) is type`.
- `_is_instance_validator(t)` — returns `lambda x: isinstance(x, t)`.
- `_is_subclass_validator(t)` — returns `lambda x: issubclass(x, t)`.
- `_iter_paths(bases)` — yields `__import__(b, {}, {}, "*").__path__[0]` for each base. Raises if strict and ModuleNotFoundError.
- `get(name, default=...)` → first calls `_get_item()`, then returns default or None. Note: falsy defaults (e.g. `get(name, "")`) may return None due to `if default is not None` check — use explicit sentinel if needed.
- `_get_item(name)` — lazy loading: checks `_exclude`, locks, checks cache, iterates `self._bases` trying `_find_item(f"{b}.{name}")`. Caches in `_classes[name]` on success. Thread-safe via RLock (supports recursive plugin deps without deadlock).
- `_find_item(name)` — imports module, uses `inspect.getmembers(module)`, filters members by same module, validates with validator. Returns first match or None.
- `[__getitem__, __iter__, keys, values, items]` — dict-like interface. `keys()` uses `pkgutil.iter_modules(self._paths)` (no loading). `values()/items()` iterate all names and call `get()` (forces loading/instantiation).

**ImportPathResolver[T]** (in `resolver.py`) — resolves dotted import strings (`"package.module.attr"`) to objects via `importlib`. Features:
- `__call__(path)` — accepts string path or pre-resolved object (returned as-is)
- Optional negative caching for failed lookups (`cache_negative=True` by default)
- Idempotent for string inputs
- Raises `ValueError` for malformed paths, `ImportError` on lookup failure

### Plugin Schemes
Three modes distinguished by generic parameter:
- **Subclass**: `Loader[type[BasePlugin]](base="...")` — yields classes inheriting from BasePlugin.
- **Singleton**: `Loader[BaseClass](base="...")` — yields instances of BaseClass.
- **Protocol**: `Loader[MyProtocol](base="...")` — checks via isinstance against protocol base class. Protocol classes must be decorated with `@runtime_checkable` (from typing module), otherwise this works only for structural duck-typing at load time without type enforcement. Does NOT use Type wrapper like Subclass scheme.

### Directory Layout
```
gufo_loader/
├── src/gufo/loader/                 # core modules
│   ├── loader.py                    # Loader[T] implementation
│   ├── resolver.py                  # ImportPathResolver[T] implementation
│   └── py.typed                     # PEP-561 marker
├── tests/                          # pytest suite (100% target)
│   ├── singleton/, subclass/, protocol/  # each scheme's fixtures
│   │   ├── base.py                 # common base class
│   │   └── primary/secondary/      # nested plugin packages (a, b, c, d)
│   ├── test_common.py              # shared tests for all schemes
│   ├── test_docs.py                # docs build validation
│   ├── test_ci.py                  # CI workflow validation
│   ├── test_example.py             # example app validation
│   ├── test_project.py             # project conventions validation
│   └── {test_subclass, test_singleton, test_protocol}.py  # per-scheme tests
├── examples/                       # runnable example apps per scheme
│   ├── singleton/, subclass/, protocol/
│       └── myapp/
│           ├── __init__.py
│           ├── __main__.py         # entry point
│           ├── base.py             # common base class
│           └── plugins/
│               ├── __init__.py
│               ├── add.py          # plugin A
│               └── sub.py          # plugin B
├── docs/                           # mkdocs-material docs (source of truth)
│   ├── index.md                    # home page
│   ├── installation.md             # installation guide
│   ├── reference.md                # API reference index
│   ├── faq.md                      # frequently asked questions
│   ├── examples/                   # example overview pages
│   │   ├── index.md
│   │   ├── subclass.md
│   │   ├── singleton.md
│   │   └── protocol.md
│   ├── migrating/                  # migration guides
│   │   ├── index.md
│   │   ├── pluggy.md               # migrating from pluggy
│   │   └── importlib.md            # migrating from importlib/pkgutil
│   ├── dev/                        # developer guides
│   │   ├── index.md                # overview
│   │   ├── environment.md          # dev environment setup
│   │   ├── testing.md              # building and testing
│   │   ├── common.md               # common tasks
│   │   ├── codequality.md          # code quality configuration
│   │   ├── codebase.md             # project structure reference
│   │   ├── standards.md            # supported standards
│   │   ├── CONTRIBUTING.md         # contributing guide (symlink to root)
│   │   └── CODE_OF_CONDUCT.md     # code of conduct (symlink to root)
│   ├── overrides/                  # custom theme overrides
│   │   └── index.html
│   ├── CHANGELOG.md               # symlink to ../CHANGELOG.md
│   ├── LICENSE.md                 # symlink to ../LICENSE.md
│   └── assets/                    # logo, illustrations
├── .github/                        # GitHub config
│   ├── workflows/                  # CI/CD (4 workflows)
│   │   ├── py-tests.yml            # tests + linting + publishing
│   │   ├── build-docs.yml          # mkdocs gh-deploy
│   │   ├── codeql.yml              # CodeQL analysis
│   │   └── security.yml            # dependency vulnerability scanning (manual)
│   ├── ISSUE_TEMPLATE/             # bug-report.yml, feature-request.yml
│   ├── CODEOWNERS                  # repository ownership rules
│   └── FUNDING.yml                 # funding profile link
├── .devcontainer/                  # VSCode Dev Container (Dockerfile target "dev")
├── Dockerfile                      # container builds (target "dev" has full dev env)
├── CITATION.cff                    # academic citation metadata
├── CONTRIBUTING.md                 # contributing guide for contributors
├── SECURITY.md                     # security policy and reporting
├── pyproject.toml                  # build config (setuptools), tool configs
├── mkdocs.yml                      # doc site config → docs.gufolabs.com/gufo_loader/
├── README.md                       # package readme → PyPI
└── LICENSE.md / CHANGELOG.md       # BSD-3-Clause / Keep a Changelog + SemVer
```

## Development Conventions
- Python 3.10+ target, tested on 3.10–3.14 (no mypy typing issues).
- Max 3 files in `src/gufo/loader/`: loader.py, resolver.py, __init__.py. No more submodules unless clearly needed; new public API goes into a dedicated file <64 lines.
- Thread-safe via RLock on `_get_item()` (caching path). RLock allows reentrant locks for recursive plugin deps without deadlock. No global state beyond instance attributes.
- Lazy loading — plugins loaded/instantiated on first `get(name)` call, cached in `self._classes`.
- Test naming: `{test_subclass.py, test_singleton.py, test_protocol.py}` for per-scheme tests, plus `test_common.py, test_docs.py, test_ci.py, test_example.py, test_project.py` for shared validation.
- Each test scheme has primary/secondary subpackages with overlap plugins (a–d) to test priority resolution (primary > secondary). Test fixture dirs include README.md explaining setup.
- Build backend: setuptools (not hatch/poetry). Version resolved from `gufo.loader.__version__` via dynamic attr in pyproject.toml `[tool.setuptools.dynamic]`.

## Build, Test, Lint

### Virtual environment setup
```bash
cd gufo_loader
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test,lint]"  # installs dev deps too
export PYTHONPATH=src  # or set in .env/IDE config
```

### Devcontainer (recommended)
Open in VSCode with Remote Containers extension. `Dockerfile target=dev` provides full env. PYTHONPATH auto-set to src.

### Linting & formatting (in this order)
```bash
ruff format   # autofix (via pyproject [tool.ruff] config)
ruff check -q  # noqa: ANN401 tolerated, __init__.py ignores E402
mypy src/    # strict mode, explicit_package_bases=true
```

Ruff lints `examples/ src/ tests/` (see workflows). MyPy uses strict mode with `warn_unused_ignores=false`. isort configured for known-first-party: `["src"]`. Docstrings use google convention, double quotes. Ruff ignores D203/D212/D107; test files ignore D1xx/S101/S603/PLR2004.

### Testing
```bash
pytest -v tests/                # standard run
pytest -v --cov --cov-branch    # coverage report
mypy src/                       # type checking (required for CI)
ruff format --check examples/ src/ tests/  # formatting check
ruff check -q examples/ src/ tests/       # linting
```

### Building package
```bash
pip install --upgrade build
python -m build --sdist --wheel
# outputs to dist/. Not tracked in git.
```

## CI Workflows (.github/workflows/)
- **py-tests.yml** — lint job (ruff format + ruff check + mypy), test-coverage job (pytest -v --cov --cov-branch → upload to Codecov), test-matrix job (Python 3.10–3.14), publish job (tagged only, PyPI via pypa/gh-action-pypi-publish).
- **build-docs.yml** — mkdocs gh-deploy on master when docs/examples/py/md files change. Site: docs.gufolabs.com/gufo_loader/.
- **codeql.yml** — CodeQL analysis (python + actions languages) on push/PRs to master for src/ and workflows only.
- **security.yml** — manual-only workflow running pyupio/safety-action for dependency vulnerability scanning. Requires `SAFETY_API_KEY` secret.

### Safety check
Triggered manually via the security.yml workflow described above. API key: SAFETY_API_KEY secret.

## Documentation
- Source → built target → published URL: `docs/` → `dist/docs/` → docs.gufolabs.com/gufo_loader/.
- Material theme with deep purple palette + dark slate mode.
- mkdocstrings for API reference generation.
- Build output goes to `dist/docs/` (not tracked in git). Also writes to `build/` (intermediate build files, not tracked).

## Key Files
- **pyproject.toml** — build config (setuptools dynamic version), ruff settings, coverage, mypy strict mode.
- **mkdocs.yml** — site config with nav sections for Home, Installation, Reference, Examples, Migrating, Developers' Guide, FAQ.
- **src/gufo/loader/** — Loader[T] class (loader.py), ImportPathResolver (resolver.py), exports + version (__init__.py).
