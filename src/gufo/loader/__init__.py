# ---------------------------------------------------------------------
# Gufo Loader
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------

"""
Generic Python class loader for robust plugin infrastructure.

Loader delivers plugins from one or many plugin packages.

## Loader

Loader is the _dict_-like singleton providing the following services:

* plugin initialization and fetching.
* plugins enumeration.

Plugins are not dependent on the loader and do not need any registration
process. The loaders are lazy by nature, meaning the plugin will be imported
and initialized just in time when the user code requests the plugin.

## Plugins

Plugins are named entities dedicated to the given task. Each plugin
is defined in its python module. Depending on the loader settings
plugins can be:

* *Instances*: Singleton instances having the class as the ancestor.
* *Subclasses*: Classes having the common ancestor.
* *Protocols*: Classes following the set of methods.

## Plugin Packages

Plugin packages are plain Python packages: the directory containing
python files with plugins and the empty `__init__.py` file.

Plugin name must match the module name. For example, module
`my_plugin.py` will define the plugin `my_plugin`.

Example:
    Plugins as the subclasses:

    ``` py
    loader = Loader[Type[BasePlugin]](base="myproject.plugins")
    ```

Example:
    Plugins as the singletones:

    ``` py
    loader = Loader[BasePlugin](base="myproject.plugins")
    ```

Example:
    Plugins as the protocols:

    ``` py
    loader = Loader[MyProtocol](base="myproject.plugins")
    ```

Attributes:
    __version__: Current version
"""

# Python modules
import inspect
from pkgutil import iter_modules
from threading import Lock
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    Optional,
    Set,
    Tuple,
    TypeVar,
    cast,
    get_args,
)

__version__: str = "1.0.3"
T = TypeVar("T")


class Loader(Generic[T]):
    """
    Generic loader. Used as singleton instantiated from generic.

    Args:
        base: Plugins package name.
        bases: Iterable of plugin package names.
        strict: Ignore missed plugin packages if set to False, Fail otherwise.
        exclude: Iterable of names to be excluded from plugins lists.

    Note:
        `base` and `bases` parameters are mutually exclusive.
        Either `base` or `bases` must be provided.

    """

    def __init__(
        self: "Loader[T]",
        base: Optional[str] = None,
        bases: Optional[Iterable[str]] = None,
        strict: bool = False,
        exclude: Optional[Iterable[str]] = None,
    ) -> None:
        # Pass to generic
        super().__init__()
        self.strict = strict
        self._validate: Optional[Callable[[Any], bool]] = None
        # Check settinngs
        if base is not None and bases is None:
            self._bases = [base]
        elif base is None and bases is not None:
            self._bases = list(bases)
        else:
            msg = "Either base or bases should be set"
            raise RuntimeError(msg)
        # Map bases to physical paths
        self._paths = list(self._iter_paths(self._bases))
        if not self._paths:
            msg = "No valid bases"
            raise RuntimeError(msg)
        #
        self._classes: Dict[str, T] = {}  # name -> class
        self._lock = Lock()
        self._exclude: Set[str] = set(exclude or [])

    def _get_item_type(self: "Loader[T]") -> T:
        """
        Get type passed to generic.

        Returns:
            Item type.

        Note:
            Internal method. Must not be used directly.
        """
        return get_args(self.__orig_class__)[0]  # type: ignore

    def _get_validator(self: "Loader[T]") -> Callable[[Any], bool]:
        """
        Get item validator function depending of instance type.

        Returns:
            Validation callable accepting one argument and returning boolean.

        Note:
            Internal method. Must not be used directly.
        """
        if self._validate is not None:
            return self._validate
        item_type = self._get_item_type()
        if self._is_type(item_type):
            # Type[Class]
            self._validate = self._is_subclass_validator(
                get_args(item_type)[0]
            )
        else:
            self._validate = self._is_instance_validator(item_type)
        return self._validate

    @staticmethod
    def _is_instance_validator(
        t: Any,  # noqa: ANN401
    ) -> Callable[[Any], bool]:
        """
        Instance validator.

        Check if the item is the instance of given type.
        Used for subclass and protocol plugin schemes. i.e.

        ``` py
        Loader[BaseClass](...)
        ```

        Args:
            t: Arbitrary object from module to check.

        Returns:
            Validation callable accepting one argument and returning boolean.

        Note:
            Internal method. Must not be used directly.
        """

        def inner(x: Any) -> bool:  # noqa: ANN401
            return isinstance(x, t)

        return inner

    @staticmethod
    def _is_subclass_validator(
        t: Any,  # noqa: ANN401
    ) -> Callable[[Any], bool]:
        """
        Instance validator.

        Check if the item is subclass of generic class.
        Used for subclass scheme. i.e.

        ``` py
        Loader[Type[BaseClass]](...)
        ```

        Args:
            t: Arbitrary object from module to check.

        Returns:
            Validation callable accepting one argument and returning boolean.

        Note:
            Internal method. Must not be used directly.
        """

        def inner(x: Any) -> bool:  # noqa: ANN401
            return issubclass(x, t)

        return inner

    @staticmethod
    def _is_type(x: Any) -> bool:  # noqa: ANN401
        """
        Check if the type is the typing.Type generic.

        Args:
            x: t: Arbitrary object from module to check.

        Returns:
            true if `x` is the `typing.Type` generic.

        Note:
            Internal method. Must not be used directly.
        """
        return repr(x).startswith("typing.Type[")

    def _iter_paths(self: "Loader[T]", bases: Iterable[str]) -> Iterable[str]:
        """
        Iterate over all paths.

        Iterate all existing and importable paths for each
        `bases` item.

        Args:
            bases: Iterable of python packages name.

        Returns:
            Iterable of resolved paths.

        Note:
            Internal method. Must not be used directly.
        """
        for b in bases:
            try:
                m = __import__(b, {}, {}, "*")
                paths = getattr(m, "__path__", None)
                if paths:
                    yield paths[0]
            except ModuleNotFoundError as e:
                if self.strict:
                    msg = f"Module '{b}' is not found"
                    raise RuntimeError(msg) from e

    def __getitem__(self: "Loader[T]", name: str) -> T:
        """
        Get plugin by name.

        Returns plugin item depending on generic type.

        Args:
            name: Name of plugin.

        Returns:
            Plugin item depending on generic type.

        Raises:
            KeyError: if plugin is missed.
        """
        kls = self.get(name)
        if kls is None:
            raise KeyError(name)
        return kls

    def __iter__(self: "Loader[T]") -> Iterator[str]:
        """
        Iterate over plugin names.

        Iterate over all existing plugin names.
        Shortland for

        ``` py
        loader.keys()
        ```

        Returns:
            Iterable of plugin names.
        """
        return iter(self.keys())

    def get(
        self: "Loader[T]", name: str, default: Optional[T] = None
    ) -> Optional[T]:
        """
        Get plugin by name.

        Return `default` value if plugin is missed.

        Args:
            name: Name of plugin.
            default: Default value, if plugin is missed.

        Returns:
            Plugin item depending on generic type or default value.
        """
        kls = self._get_item(name)
        if kls is not None:
            return kls
        if default is not None:
            return default
        return None

    def _get_item(self: "Loader[T]", name: str) -> Optional[T]:
        """
        Get plugin by name.

        Search all the packages and get plugin named by `name`.

        Args:
            name: Plugin name

        Returns:
            Item found or None

        Note:
            Internal method. Must not be used directly.
        """
        if name in self._exclude:
            msg = "Trying to import excluded name"
            raise RuntimeError(msg)
        with self._lock:
            kls = self._classes.get(name)
            if kls is not None:
                return kls
            for b in self._bases:
                kls = self._find_item(f"{b}.{name}")
                if kls is not None:
                    self._classes[name] = kls
                    return kls
        return None

    def _find_item(self: "Loader[T]", name: str) -> Optional[T]:
        """
        Get plugin item from module `name`.

        Args:
            name: Module name.

        Returns:
            Item found or None

        Note:
            Internal method. Must not be used directly.
        """
        is_valid = self._get_validator()
        try:
            module = __import__(name, {}, {}, "*")
            for _, member in inspect.getmembers(module):
                # Check member is originated from same module
                if (
                    hasattr(member, "__module__")
                    and member.__module__ != module.__name__
                ):
                    continue
                # Check member is valid
                if not is_valid(member):
                    continue
                # Cast member to proper type
                return cast(T, member)
        except ImportError:
            pass
        return None

    def keys(self: "Loader[T]") -> Iterable[str]:
        """
        Iterate over plugin name.

        Iterable yielding all existing plugin names.

        Returns:
            Iterable of strings with all plugin names.

        Note:
            `keys()` do not force plugin module loading and instantination.
        """
        seen: Set[str] = set()
        for mi in iter_modules(self._paths):
            if mi.name not in seen and mi.name not in self._exclude:
                seen.add(mi.name)
        yield from sorted(seen)

    def values(self: "Loader[T]") -> Iterable[T]:
        """
        Iterate all found plugin items.

        Returns:
            Iterable of plugin items.

        Note:
            `values()` will force plugin module loading and instantination.
        """
        for name in self:
            item = self.get(name)
            if item is not None:
                yield item

    def items(self: "Loader[T]") -> Iterable[Tuple[str, T]]:
        """
        Iterate the (`name`, `item`) tuples for all plugin items.

        Return:
            Iterable of tuples of (`name`, `item`)

        None:
            `items()` will force plugin module loading and instantination.
        """
        for name in self:
            item = self.get(name)
            if item is not None:
                yield name, item
