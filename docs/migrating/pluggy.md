---
title: Migrating from Pluggy to Gufo Loader
---

## Why Migrate

Pluggy is the standard plugin framework for Python (used by `pytest`, `pre-commit`), but it relies on dynamic dispatch via `hookspec` and `@hookimpl`. This approach has several pain points:

1.  **Loss of Type Information**: When you call `plugin_manager.get_plugin("name")`, you get an opaque object or `Any`. IDE autocomplete stops working, and static analyzers like `mypy` cannot validate your plugin's methods until runtime.
2.  **Global Registration State**: Pluggy maintains a global `PluginManager` singleton. You must explicitly register plugins with specific hook specs before they can be used by other parts of the system.
3.  **Verbose Boilerplate**: Every plugin file must import and reference `hookspecs`.

Gufo Loader solves these problems by using standard Python inheritance (or protocols) over a dynamic registry. It replaces string-based event dispatching with generic type parameters that are fully understood by your IDE, mypy, and AI coding assistants.

## Migration Examples

### 1. The Plugin Interface

In Pluggy, you first define a `hookspec` module. In Gufo Loader, you simply define a standard base class or protocol.

**Before (Pluggy - `hookspecs.py`)**:
```python
import pluggy

hookspec = pluggy.HookspecMarker("myapp")

class MyHookSpec:
    @hookspec
    def process(self, data: str) -> str:
        """A processing hook."""
```

**After (Gufo Loader - `plugins/base.py`)**:
```python
from abc import ABC, abstractmethod

class PluginBase(ABC):
    @abstractmethod
    def process(self, data: str) -> str:
        """A processing hook."""
```
*No external hooks library is needed in your plugin files. Just inherit from `PluginBase` like any other class.*

### 2. Implementing a Plugin

In Pluggy, you must decorate methods with `@hookimpl`. In Gufo Loader, the implementation is just a standard Python class.

**Before (Pluggy)**:
```python
from .hookspecs import hookimpl

class MyPluginImpl:
    @hookimpl  # <-- Must remember this decorator!
    def process(self, data: str) -> str:
        return data.upper()
```

**After (Gufo Loader)**:
```python
from plugins.base import PluginBase

class MyPlugin(PluginBase):
    def process(self, data: str) -> str:
        # No decorators required. Standard inheritance!
        return data.upper()
```

### 3. Loading and Enumerating Plugins

Pluggy requires you to iterate over `plugin_manager.list_name_plugin` or look up plugins by exact string keys. This works well at runtime but leaves your static type checker blind. Gufo Loader replaces this with a generic `Loader[T]` class.

**Before (Pluggy)**:
```python
import pluggy

# Global mutable state!
_pm = pluggy.PluginManager("myapp")
_pm.add_hookspecs(hookspecs)  # Requires registration
_pm.load_setuptools_entrypoints("myapp")  # Discovers plugins from setup.py

for plugin in _pm.registered_plugins:
    hook = _pm.hook
    result = hook.process(data="hello") # Return type is opaque (often a list of Any)
```

**After (Gufo Loader)**:
```python
from gufo.loader import Loader
import myplugins.base  # The discovered plugins live in 'myplugins' package

# Generic type parameter 'base.PluginBase' ensures perfect static typing!
loader = Loader[base.PluginBase](
    base="myplugins", 
    strict=True  # Fails fast if a module inside 'myplugins' has syntax errors
)

instance = loader["MyPlugin"]()  # IDE knows the exact type here
result = instance.process(data="hello")          # Full autocomplete, full mypy support
```

## Key Differences Summary

| Feature | Pluggy via `hookimpl` | Gufo Loader via Generics |
|---|---|---|
| Plugin registration | Explicit (via decorators or setup.py) | Automatic discovery within the `base` package |
| Return type from registry | Opaque (often a list of results) | Fully typed (`PluginBase`) |
| Startup speed | Eager scanning of all paths on boot | Lazy (loads only when `loader.get()` is called) |
| Error handling | Silently skips plugins that don't match hooks | Raises immediately if `strict=True` and a file has a syntax error |

## When to Choose Gufo Loader over Pluggy

*   **Prefer standard Python**: If your team dislikes Pluggy's "magic" decorators (`@hookimpl`) or its strict dependency on the `pluggy` namespace.
*   **Need better type checking**: If you rely heavily on mypy/pyright and want to ensure plugins strictly follow their base class/interface.
*   **Startup latency matters**: Gufo Loader loads modules only when accessed, reducing cold start times for applications with hundreds of optional plugins.
