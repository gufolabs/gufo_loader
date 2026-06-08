---
title: Overview - Migrating to Gufo Loader
---

## Overview

This section provides detailed migration guides for developers transitioning their codebase to **Gufo Loader** from other popular plugin loading systems.

The primary advantages of migrating are:

*   **Full Static Typing**: Unlike dynamic registry approaches, `gufo_loader` returns typed objects (`Loader[T]`) that IDEs and static analyzers understand perfectly.
*   **Zero Boilerplate**: No registration loops or complex hook specifications. You simply point the loader at a package directory, and it handles discovery automatically.
*   **Lazy Loading & Caching**: Plugins are imported only when requested and cached internally, preventing startup spikes in large applications.

### Available Guides

*   [Migrating from Pluggy](pluggy.md) — replacing `pluggy` entry points with a type-safe generator API.
*   [Migrating from `importlib`] — dropping manual path scanning (with `pkgutil`) in favor of generic, lazy-loaded discovery.

!!! note "Benefits for AI agents"

    Because Gufo Loader relies on strict Python types rather than dynamic string lookups or `__dict__` manipulation, AI coding assistants and automated code analysis tools can perfectly understand your plugin structure without needing special parsing rules. This means better autocomplete, fewer hallucinations, and faster refactoring speeds when you use tools like GitHub Copilot or Cursor.
