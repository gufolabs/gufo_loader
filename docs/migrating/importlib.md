---
title: Migrating from importlib to Gufo Loader
---

## Why Migrate

Using raw `importlib` and `pkgutil` for plugin discovery is the most common approach in Python — it's built into the standard library, requires no external dependencies, and gives you absolute control. However, writing your own loader inevitably leads to recurring boilerplate: path resolution, error handling across multiple modules, result caching, and type narrowing. Gufo Loader encapsulates all of this into a single generic class (`Loader[T]`), giving you full static typing without the maintenance overhead.

**What Gufo Loader gives you over raw imports:**

1. **Lazy loading & built-in caching**: Modules are loaded exactly once on first access, then cached in memory. No need to write your own `_cache = {}` or use `functools.lru_cache`.
2. **Strict error isolation**: If one plugin module has a syntax error or raises an exception during import, the loader continues scanning other modules and only fails at initialization if `strict=True`. With raw `importlib` you have to write the try/except yourself for every single file.
3. **Full static typing**: The generic parameter `T` propagates through every method (`get()`, `__getitem__`, `values()`, `items()`), so mypy, Pyright, and your IDE understand exactly what type each plugin is — zero `Any` leakage.
4. **Dict-like API**: Standard `loader["name"]`, `loader.get(name)`, `loader.keys()` — no need to learn a custom registry API.

## Migration Examples

### 1. Path Resolution and Module Scanning

Gufo Loader automatically resolves the path of your base package via its `__path__` attribute. With raw `importlib` you have to manually find and iterate over `pkgutil.iter_modules` yourself.

**Before (importlib + pkgutil)**:
```python
import importlib
import pkgutil
from typing import Optional, Type, Dict, Any

def discover_plugins() -> Dict[str, Any]:
    # Manual path resolution
    base_package = importlib.import_module("myapp.plugins")
    
    plugins: Dict[str, Any] = {}
    
    for importer, modname, ispkg in pkgutil.iter_modules(base_package.__path__):
        try:
            module = importlib.import_module(f"myapp.plugins.{modname}")
            # You then have to manually search for all classes/instances...
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, BasePlugin):  # manual type check!
                    # What about duplicates? Caching logic? Error handling?
                    plugins[modname] = obj
        except (ImportError, SyntaxError, AttributeError) as exc:
            print(f"Warning: failed to load {modname}: {exc}")
            
    return plugins

# Call it once at startup...
all_plugins = discover_plugins()  # eager scan on import!
```

**After (Gufo Loader)**:
```python
from gufo.loader import Loader
import myapp.plugins.base

loader = Loader(
    base="myapp.plugins",
    strict=False  # Continue on errors (default); set True to fail fast
)

# Lazy loading — modules aren't imported until you actually call get() or values()
instance: BasePlugin = loader["auth"]     # First access triggers import + cache
cached_again: BasePlugin = loader["auth"] # Returned from cache immediately
```

### 2. Type-Safe Retrieval

With raw `importlib` you typically end up returning a `Dict[str, Any]` or `Dict[str, object]`, because the compiler cannot know which type lives inside each dictionary value. Gufo Loader narrows types at compile time through generics.

**Before (importlib)**:
```python
def get_auth_plugin(all_plugins: Dict[str, Any]) -> None:
    plugin = all_plugins.get("auth")
    if plugin is not None:
        # IDE cannot help you here — no autocomplete!
        # mypy will complain or silently allow anything:
        result = plugin.authenticate(user="admin")  # ✗ No type checking
```

**After (Gufo Loader)**:
```python
from gufo.loader import Loader
import myapp.plugins.base as base

loader: Loader[base.Authenticator] = Loader(base="myapp.plugins.auth")

plugin = loader["auth"]          # ✅ Type is Authenticator everywhere!
result: User = plugin.authenticate(user="admin")  # ✅ Full type checking
```

### 3. Handling Defaults and Missing Plugins

Gufo Loader's `get(name, default)` method lets you specify a fallback value (or `None` if omitted). This mirrors the standard Python `dict.get()` behavior, which is more intuitive than raw `dict.get()` calls across manually built registries.

**Before (importlib)**:
```python
plugins = discover_plugins()
plugin = plugins.get("auth")  # Returns None if missing — manual dict lookups
if plugin is not None:
    plugin.authenticate(...)
```

**After (Gufo Loader)**:
```python
loader: Loader[base.Authenticator] = Loader(base="myapp.plugins.auth")

# If 'auth' is missing, returns the default (or None):
plugin = loader.get("auth", base.Authenticator(None))  # fallback instance
if plugin is not None:
    plugin.authenticate(user="admin")
```

## Key Differences Summary

| Feature | Raw importlib + pkgutil | Gufo Loader |
|---|---|---|
| Path resolution | Manual (`__path__[0]`) | Automatic from `base` package name |
| Error handling on bad module | You write try/except per file | Built-in; continues scanning (unless `strict=True`) |
| Type information at load time | Lost — you get `Dict[str, Any]` | Fully preserved via `Loader[T]` generics |
| Startup performance | Eager (scan all modules on boot) | Lazy (scan only when requested) |
| API surface | Manual dict or registry class | Dict-like: `get()`, `keys()`, `values()`, `items()` |

## When to Choose Gufo Loader over Raw Imports

* **Type safety matters**: If you want mypy/Pyright to understand your plugins without stubs or manual narrowing.
* **You're tired of boilerplate**: Stop writing the same path-resolution-and-caching logic in every new project.
* **Startup latency matters**: With Gufo Loader, unused plugin directories stay entirely unloaded — no need to write complex "lazy scan" logic yourself.
