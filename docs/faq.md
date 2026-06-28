---
hide:
    - navigation
---

## Getting Started with Gufo Loader

### What is "Gufo Loader"?

**Gufo Loader** is a generic Python class loader for robust plugin infrastructure. It provides a dict-like singleton API for late-loading plugins from one or many distributed package directories. Currently it supports three loading schemes: subclasses, singletons (instances), and structural protocols.

### Why shouldn't I just use `__import__` or `importlib`?

You can use `__import__` manually, but you will quickly need to write boilerplate code for directory walking, module discovery, caching, initialization, and error handling. You also lose static typing guarantees entirely. Gufo Loader provides a zero-`Any` statically typed interface, handles priority resolution across multiple plugin directories, and implements lazy-loading with thread-safe caching right out of the box.

### Which Python versions are supported?

Python 3.10 and later. The test matrix covers Python 3.10 through 3.14. There are no external runtime dependencies beyond the standard library.

### How does static typing work across plugin boundaries?

The `Loader[T]` class is parameterized with a specific type (e.g., `Type[BasePlugin]`, `BasePlugin`, or a `Protocol`). Type checkers (mypy, Pyright) understand that `loader["my_plugin"]` returns exactly the type defined in `T`. Unlike generic plugin systems which usually fallback to `Any` or dynamic attributes, Gufo Loader provides full IDE autocompletion and compile-time checks on your plugin code.

## Plugin Schemes

### What are the three loading schemes?

1. **Subclass** (`Loader[type[Base]]`) — yields plugin classes inheriting from `Base`. You instantiate them yourself when needed.
2. **Singleton** (`Loader[Base]`) — yields initialized plugin instances. If a name is requested twice, the same instance is reused.
3. **Protocol** (`Loader[MyProtocol]`) — yields objects that structurally satisfy `MyProtocol` (decorated with `@runtime_checkable`). Use this when you cannot change the plugin source code to inherit a base class.

### How do I choose the right scheme for my project?

- Choose **Subclass** if plugins require complex factory patterns, per-request initialization, or if lifecycle management is handled by your application framework.
- Choose **Singleton** if plugins are stateless or maintain global state scoped to the plugin name. It guarantees a single instance per name across the entire loader session.
- Choose **Protocol** when you need structural duck-typing (e.g., plugging into third-party classes you don't own). Make sure the target classes are decorated with `@runtime_checkable`.

### What is the difference between primary and secondary package directories?

When configuring multiple plugin directories (`bases`), Gufo Loader iterates them sequentially. Plugins defined in earlier entries take strict priority over later ones. This allows you to override or inject custom implementations from a "primary" source directory before falling back to default "secondary" plugins distributed in external packages.

### Can I load plugins from multiple sources simultaneously?

Yes. Pass a tuple of package names or paths to the `bases` parameter: `Loader[MyClass](bases=("my.plugins.primary", "my.plugins.secondary"))`. The loader checks each source in order and caches the first match it finds per plugin name.

## Usage Patterns

### How do I load and initialize all plugins on startup?

Iterate over `.items()` or `.values()`:
```python
list(loader.values())
```
These methods call `pkgutil.iter_modules()` to discover plugin names, then trigger the lazy-loading path for every single name. Caching is done automatically; subsequent `.get("name")` calls return instantly from memory.

### How do I exclude a specific plugin?

Pass the `exclude` parameter during initialization:
```python
loader = Loader[MyClass](base="my.plugins", exclude={"excluded_plugin"})
```
The exclude set is checked before any import logic runs, so excluded modules are never loaded or cached.

### Can I reload plugins after they have been loaded?

Not through the public API. Gufo Loader was designed for singleton persistence within a session's lifetime — once a class or instance is in `_classes`, it is returned as-is. If you absolutely need to force a reload during development or testing, clear the cache directly: `loader._classes.clear()`. The next `.get()` call will re-import and re-instantiate.

### Can I use entry_points (setup.py / pyproject.toml) instead of hardcoded package names?

Yes. You can dynamically discover entry points within your application code and pass them into the `bases` tuple exactly as you would a regular package path. Gufo Loader's plugin discovery (`pkgutil.iter_modules`) works identically for both hardcoded paths and dynamically discovered ones.

## Migration

### How do I migrate from Pluggy?

See the [Migration from Pluggy](migrating/pluggy.md) guide. It covers equivalent concepts (hooks, entry points, registration), how Gufo Loader's priority model maps to Pluggy's phase ordering, and provides side-by-side code snippets highlighting the elimination of `Any` types in your plugin logic.

### How do I migrate from raw `importlib` or `pkgutil`?

See the [Migration from importlib/pkgutil](migrating/importlib.md) guide. It demonstrates how to replace standard library boilerplate with Gufo Loader's lazy-loading, thread-safe cache, and exclusion sets in a handful of lines.

## Thread Safety & Performance

### Is Gufo Loader thread-safe?

Yes. The plugin discovery path uses `pkgutil.iter_modules()`, which is stateless and read-only. The cache population path within `_get_item()` uses a `threading.Lock` to prevent race conditions during the initial load (double-checked locking pattern). Once cached, all subsequent reads are lock-free. It is entirely safe to initialize plugins from multiple concurrent threads.

### Are there any known limitations with plugin imports?

The only constraint applies globally to Python's import system: circular plugin dependencies between `A.plugin` and `B.plugin` may result in partially initialized state during the initial load, because the lock is held while the module is being imported. Standard Python dependency management practices apply here.

## Support and License

### What license is Gufo Loader released under?

Gufo Loader is released under the [3-clause BSD License](https://opensource.org/licenses/BSD-3-Clause). You are free to use it in commercial, open-source, or private projects.

### Where can I get help or report a bug?

Please open a [GitHub Issue](https://github.com/gufolabs/gufo_loader/issues) for bugs, feature requests, or architectural questions. Discussions are welcome as well.

### Can I support the Gufo Stack project financially?

Yes. You can support our work via [GitHub Sponsors](https://github.com/sponsors/gufolabs) or [Buy Me a Coffee](https://www.buymeacoffee.com/dvolodin). Your contributions directly fund continued research and maintenance of the Gufo Stack components.

## About Gufo

### What does "Gufo" mean?

*Gufo* means *the Owl* in Italian.

### Why the owls?

We love owls — and the viable parts of our technologies were proven at a project literally named "the Owl" before becoming independent open-source components.

### What is "Gufo Stack"?

We've extracted core components behind the [NOC](https://getnoc.com/) network management platform and released them as independent packages, available under the terms of the 3-clause BSD license. Our software shares common code quality standards and is battle-proven under high load across large-scale ISP deployments. We hope our key components will help engineers build reliable networks and robust network management software.

### What is "Gufo Labs"?

[Gufo Labs](https://gufolabs.com/) is the Milan-based company specializing in network and IT consulting, and in software research for communications infrastructure.
