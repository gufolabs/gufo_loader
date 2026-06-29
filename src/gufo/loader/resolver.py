# ---------------------------------------------------------------------
# Gufo Loader: ImportPathResolver implementation.
# ---------------------------------------------------------------------
# Copyright (C) 2022-26, Gufo Labs
# ---------------------------------------------------------------------

"""ImportPathResolver implementation."""

# Python modules
import importlib
from threading import Lock
from typing import Generic, TypeVar

T = TypeVar("T")


class _Sentinel: ...


_sentinel = _Sentinel()


class ImportPathResolver(Generic[T]):
    """
    Resolve Python objects by import path.

    This resolver converts dot-separated import paths into Python objects
    using importlib, with optional caching and support for already resolved values.

    Both successful and (optionally) failed resolutions are cached:
    - Successful imports cache the resolved object.
    - Failed attribute lookups may be cached as negative results
      (controlled by `cache_negative`) to avoid repeated import attempts
      for missing symbols.

    Typical use case is dynamic resolution of callables, handlers, classes,
    or other runtime-imported symbols in configuration-driven systems.

    Example:
        resolver = ImportPathResolver[Callable]()
        func = resolver("package.module.func")
        func()

    Notes:
        This resolver is idempotent for string inputs.

        Negative caching is optional and controlled by `cache_negative`.
        When enabled, missing attributes are cached to prevent repeated
        import attempts for unresolved symbols.
    """

    def __init__(self, cache_negative: bool = True) -> None:
        self._lock = Lock()
        self._cache: dict[str, T | _Sentinel] = {}
        self._cache_negative = cache_negative

    def __call__(self, path: str | T) -> T:
        """
        Resolve item.

        Args:
            path:
                Dot-separated import path (e.g. "package.module.attr")
                or already resolved object.

                If value is not a string, it is returned as-is.

        Returns:
            Resolved object of type T.

        Raises:
            ValueError:
                If the provided import path is malformed or empty.
            ImportError:
                If module cannot be imported or attribute is missing.
        """

        def unwind(v: T | _Sentinel) -> T:
            """
            Raise import error if value is sentinel.

            Args:
                v: Value or sentinel item

            Returns:
                Value, when not sentinel.

            Raises:
                ImportError: when value is sentinel.
            """
            if isinstance(v, _Sentinel):
                msg = "not found"
                raise ImportError(msg)
            return v

        if not isinstance(path, str):
            return path  # as-is
        mod_name, _, attr_name = path.rpartition(".")
        if not mod_name:
            msg = f"malformed path: {path}"
            raise ValueError(msg)
        with self._lock:
            if path in self._cache:
                return unwind(self._cache[path])
            module = importlib.import_module(mod_name)  # Raises ImportError
            item = getattr(module, attr_name, _sentinel)
            if item is not _sentinel or self._cache_negative:
                self._cache[path] = item
            return unwind(item)
