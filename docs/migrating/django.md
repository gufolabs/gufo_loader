---
title: Migrating from Django import_string to Gufo Loader's ImportPathResolver
---

## Why Migrate

Django provides `django.utils.module_loading.import_string` — a utility that resolves dotted strings like `"package.module.ClassName"` into actual Python objects. It serves the same purpose as Gufo Loader's [`ImportPathResolver`][ImportPathResolver]: resolving runtime configuration references without hardcoding imports.

However, Django's API is tied to its ecosystem and offers no typing beyond `Any`. If your project already uses or plans to adopt `gufo_loader`, switching gives you:

1. **Full static typing**: The generic parameter `T` ensures your IDE and mypy know the exact return type of every resolution call.
2. **Built-in caching (negative too)**: Failed lookups are cached by default so downstream code does not re-import on every call — equivalent to a manual `functools.lru_cache` around a custom helper.
3. **Idempotent reuse**: Create one resolver instance and pass it around; no global module-level state or per-call overhead of repeated imports.

## Migration Examples

### 1. Basic Resolver Usage

**Before (Django)**:
```python
from django.utils.module_loading import import_string

handler_cls = import_string("myapp.handlers.MainHandler")
instance = handler_cls()
result = instance.handle(data="hello")
```

**After (Gufo Loader)**:
```python
from gufo.loader.resolver import ImportPathResolver
from typing import Callable

resolver = ImportPathResolver[Callable]()

handler_cls = resolver("myapp.handlers.MainHandler")
instance = handler_cls()
result = instance.handle(data="hello")
```

*The type parameter `Callable` guarantees the resolver never returns an unrelated string or unexpected object — mypy will flag mismatches at static analysis time.*

### 2. Reusing a Single Resolver Instance

**Before (Django)**:
```python
from django.utils.module_loading import import_string

# Every call re-imports the module + getattr — no caching!
service = import_string("myapp.services.UserService")
auth    = import_string("myapp.middleware.AuthMiddleware")
report  = import_string("myapp.reports.MonthlyReport")
```

**After (Gufo Loader)**:
```python
from gufo.loader.resolver import ImportPathResolver
from typing import Callable, Type

resolver = ImportPathResolver[Any]()

service    = resolver("myapp.services.UserService")
auth       = resolver("myapp.middleware.AuthMiddleware")
report     = resolver("myapp.reports.MonthlyReport")  # all three cached internally
```

### 3. Passing Resolved Objects Directly

Both Django and Gufo Loader support passing already-resolved objects as configuration values, but only Gufo Loader does this without any module-level side-effects:

**Before (Django)**:
```python
# This works because import_string returns the object if it's not a string —
# but it's an undocumented quirk, not a guarantee.
def get_handler(path_or_obj):
    cls = import_string(path_or_obj)  # if already a class, returned as-is by accident
    return cls()
```

**After (Gufo Loader)**:
```python
# Supported explicitly in the API contract — resolver returns non-string inputs unchanged.
def get_handler(path_or_cls):
    cls = resolver(path_or_cls)
    return cls()
```

### 4. Error Handling

**Before (Django)**:
```python
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured

try:
    handler = import_string("myapp.handlers.NonExistent")
except ImportError as e:
    raise ImproperlyConfigured(e) from e
```

**After (Gufo Loader)**:
```python
from gufo.loader.resolver import ImportPathResolver

resolver = ImportPathResolver[Any]()

try:
    handler = resolver("myapp.handlers.NonExistent")
except ImportError:  # raised for both missing module and missing attribute
    handler = None  # or some fallback default
```

## Key Differences Summary

| Feature | `import_string` (Django) | `ImportPathResolver` (Gufo Loader) |
|---|---|---|
| Return type hint | `Any` | Generic `T` — fully typed |
| Caching | None | Yes, successes and optional negatives |
| Thread safety | Yes (module-level) | Yes (per-instance lock) |
| Reusability | Per-call function | Single instance reused across app |
| Non-string passthrough | Implicit quirk | Explicit API contract |
| Custom error types | Always raises `ImportError` | Raises `ImportError` / `ValueError` as documented |
| Deep attribute chains | Only 2-level (`module.attribute`) | Same — use `pathlib.PurePath` or custom logic for deeper chains |

## When to Stay with Django

Keep `import_string` if:

* Your project is tightly coupled to a Django codebase and imports from `django.utils.module_loading` are already widespread.
* You don't need static typing on the resolved objects (e.g., one-off scripts).
* Adding `gufo_loader` as a dependency is overkill for your use case — `import_string` works with zero extra dependencies.

## Key Differences Summary

| Feature | `import_string` (Django) | `ImportPathResolver` (Gufo Loader) |
|---|---|---|
| Return type hint | `Any` | Generic `T` — fully typed |
| Caching | None | Yes, successes and optional negatives |
| Thread safety | Module-level singleton lock | Per-instance threading.Lock |
| Reusability | One function per call | Single resolver instance reused everywhere |
| Non-string passthrough | Implicit quirk | Explicit API contract |
| Custom error types | Always ImportError/ImproperlyConfigured | `ImportError` / `ValueError` as documented at construction time |

## When to Stay with Django

Keep `import_string` if:

* Your project is tightly coupled to a Django codebase and imports from `django.utils.module_loading` are already widespread.
* You don't need static typing on the resolved objects (e.g., one-off scripts).
* Adding `gufo_loader` as a dependency is overkill for your use case — `import_string` works with zero extra dependencies.

[ImportPathResolver]: ../reference.md#importpathresolver
