# Gufo Loader

*Generic Python class loader for robust plugin infrastructure.*

[![PyPi version](https://img.shields.io/pypi/v/gufo_loader.svg)](https://pypi.python.org/pypi/gufo_loader/)
![Downloads](https://img.shields.io/pypi/dw/gufo_loader)
![Python Versions](https://img.shields.io/pypi/pyversions/gufo_loader)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Build](https://img.shields.io/github/actions/workflow/status/gufolabs/gufo_loader/py-tests.yml?branch=master)
[![codecov](https://codecov.io/gh/gufolabs/gufo_loader/graph/badge.svg?token=WPQTHR6C59)](https://codecov.io/gh/gufolabs/gufo_loader)
![Sponsors](https://img.shields.io/github/sponsors/gufolabs)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)

---

**Documentation**: [https://docs.gufolabs.com/gufo_loader/](https://docs.gufolabs.com/gufo_loader/)

**Source Code**: [https://github.com/gufolabs/gufo_loader/](https://github.com/gufolabs/gufo_loader/)

---

Load plugins lazily — and keep full static typing throughout. Unlike traditional plugin managers that return `Any` or an untyped spec object, **Gufo Loader** uses Python Generics to preserve the exact type of every loaded plugin: your IDE sees everything, and static analyzers catch errors before you hit run.

## The Problem

Most plugin frameworks lose types at the point of dynamic loading. You call a method to fetch `"my_database"` driver and get back an opaque object — autocomplete stops working, `mypy` complains about `Any`, and refactoring becomes guesswork.

```python
# ❌ Traditional approach: any return type
plugin = manager.get_plugin("my_database")  # -> Any
plugin.commit()  # no autocomplete, no static analysis
```

## The Gufo Loader Way

Every call in the dict-like API retains the generic type `T`. Your plugin modules are inspected automatically — no registration needed — and IDEs show full signatures for every loaded plugin.

```python
# ✅ Fully typed from import to usage
from gufo.loader import Loader
import my_plugins.plugins

plugins: Loader[my_plugins.BaseDB] = Loader(
    base="my_plugins",
)

db: my_plugins.BaseDB = plugins["primary_db"]  # type is BaseDB, not Any
conn = db.connect(...)                          # full autocomplete
print(db.dialect)                               # static analyzer knows the type
```

This works across all three loading schemes described below.

## Plugin Schemes

Plugins are named entities stored in a Python package (a directory with `__init__.py`). The plugin name always matches its module name — `auth.py` defines plugin `auth`. There is **no registration process**: the loader discovers plugins by scanning the package and instantiating or filtering them according to the generic type parameter.

| Scheme | Generic Parameter | What Gets Loaded |
| --- | --- | --- |
| Subclass | `Loader[Type[BaseClass]]` | Classes inheriting from `BaseClass` |
| Singleton | `Loader[BaseClass]` | Instances of `BaseClass` (or its subclasses) |
| Protocol | `Loader[MyProtocol]` | Objects satisfying the protocol's structural interface |

Quick start for each scheme:

```python
# Subclass loader — yields classes
plugins: Loader[Type[BasePlugin]] = Loader(base="myproject.plugins")
plugin_cls = plugins["webdriver"]  # -> Type[BasePlugin]

# Singleton loader — yields instances
plugins: Loader[BasePlugin] = Loader(base="myproject.plugins")
instance = plugins["webdriver"]    # -> BasePlugin instance
```

## Features

* **Full static typing** — `py.typed` bundle, generic API, zero `Any` leakage.
* **Dictionary-like interface** — intuitive `loader[name]`, `loader.get(name)`, iteration over keys/values/items.
* **Lazy loading** — plugins are imported into memory only when first requested and cached thereafter.
* **Thread-safe** — built-in lock guards the discovery cache.
* **Three schemes** — subclass, singleton (instance), and protocol-based plugin discovery.
* **No registration overhead** — plugins live in plain Python packages. The loader finds them automatically.
* **Security-first** — strict mode rejects missing base packages at initialization; exclude lists filter known-safe names.

## Getting Started

1. Install the package:

   ```bash
   pip install gufo-loader
   ```

2. Define a plugin interface and two implementations:

   ```python
   # plugins/base.py
   class BasePlugin(ABC):
       @abstractmethod
       def execute(self) -> str: ...
   ```

3. Create plugins in the same package:

   ```python
   # plugins/alpha.py
   from .base import BasePlugin

   class AlphaPlugin(BasePlugin):
       def execute(self) -> str:
           return "alpha"
   ```

4. Load and use them:

   ```python
   from gufo.loader import Loader
   from typing import Type
   from plugins.base import BasePlugin

   loader: Loader[Type[BasePlugin]] = Loader(base="plugins")
   plugin_cls = loader["alpha"]  # fully typed at import time
   instance = plugin_cls()       # -> AlphaPlugin
   print(instance.execute())     # "alpha"
   ```

## On Gufo Stack

This product is part of [Gufo Stack][Gufo Stack] — a collaborative effort led by [Gufo Labs][Gufo Labs]. Our goal is to build a robust, flexible toolkit for network management software and automation.

We extract proven technologies from the [NOC][NOC] project, refine their APIs, performance, documentation, and testing as standalone packages. NOC consumes these as final external dependencies. Other products benefit from Gufo Stack too — we believe better shared tools make better infrastructure.

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[NOC]: https://getnoc.com/
