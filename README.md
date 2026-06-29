# Gufo Loader

*Typed runtime object resolution for Python.*

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

Gufo Loader provides tools to resolve Python objects at runtime from string identifiers with full typing and IDE support.

It is designed for applications where object selection is driven by configuration or runtime state.

## Two resolution models

Gufo Loader supports two complementary ways to resolve Python objects.

```text
          String identifier
                 │
      ┌──────────┴──────────┐
      │                     │
 Full import path      Logical name
      │                     │
ImportPathResolver        Loader
      └──────────┬──────────┘
                 │
          Python object
```          

### Direct resolution (full import path)
A Python object is identified by its fully qualified import path. 

```python
"myproject.handlers.process"
```

Use `ImportPathResolver`:
```python
resolver = ImportPathResolver[Callable[..., Any]]()
handler = resolver("myproject.handlers.process")
```

Use this when the exact location of the object is known.

### Named resolution (logical name)
A Python object is referenced by a short logical name:
```python
"json"
```

The system resolves it to a concrete implementation. Use `Loader`:
```python
loader = Loader[type[BasePlugin]](base="myproject.plugins")
plugin = loader["json"]
```
Use this when behavior is selected by configuration or convention.

## ImportPathResolver

Resolves full Python import paths into objects.

```python
resolver("package.module.symbol")
```

**Properties:**

- works with any Python object
- caching of successful resolutions
- optional negative caching
- strict typing support
- safe, deterministic import behavior

## Loader
Loader discovers and resolves typed objects from one or more Python packages.

It supports three plugin models:

**Class-based plugins**
```python
Loader[type[BasePlugin]]
```

**Singleton instances**
```python
Loader[BasePlugin]
```

**Protocol-based plugins**
```python
Loader[MyProtocol]
```

**Properties:**

- subclasses, instances and protocols
- no registration
- multiple package namespaces
- lazy discovery
- type validation
- predictable resolution behavior

## Features

- **Zero dependencies** — no external runtime dependencies
- **Fully typed API** — generics, protocols, subclass-safe resolution
- **IDE-friendly** — autocompletion and static type inference support
- **Lazy loading** — modules imported only when needed
- **Caching** — resolved objects are cached for performance
- **Negative caching** — failed resolutions are cached to avoid repeated lookups
- **Secure by design** — only explicit Python imports are performed
- **Deterministic behavior** — predictable resolution for identical inputs
- **Multi-package support** — load plugins from multiple namespaces

## On Gufo Stack

This product is a part of [Gufo Stack][Gufo Stack] - the collaborative effort 
led by [Gufo Labs][Gufo Labs]. Our goal is to create a robust and flexible 
set of tools to create network management software and automate 
routine administration tasks.

To do this, we extract the key technologies that have proven themselves 
in the [NOC][NOC] and bring them as separate packages. Then we work on API,
performance tuning, documentation, and testing. The [NOC][NOC] uses the final result
as the external dependencies.

[Gufo Stack][Gufo Stack] makes the [NOC][NOC] better, and this is our primary task. But other products
can benefit from [Gufo Stack][Gufo Stack] too. So we believe that our effort will make 
the other network management products better.

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[NOC]: https://getnoc.com/