---
template: index.html
hide:
    - navigation
    - toc
hero:
    title: Gufo Loader
    subtitle: Fully typed plugin loading with zero Any leakage
    install_button: Getting Started
    source_button: Source Code
---

## Software Evolution

Software tends to grow larger and larger. Even small pet projects can eventually become huge monoliths. This growth introduces new challenges:

* Large codebases are hard to test and maintain.
* Only a small fraction of functions serves any single user task, yet all of them consume memory and slow load time.
* Software needs to be extendable. End-users require custom features, and third-party developers need a way to distribute them.

Software engineers adopted the modular approach decades ago: code is grouped into modules, which sometimes form coordinated groups interacting through well-defined interfaces. These interfaces create boundaries between system components, allowing each side to operate as a black box—the internals don't matter; only the interface does.

Black boxes are swappable. They perform specific functions regardless of their implementation details. Replace one box with another and the overall application behaviour changes without touching the core.

So modern software is designed as an orchestration layer that distributes tasks to pluggable subsystems, leaving complexity to them.

But how do you load only the plugins needed for a given task? How do you swap or extend them?

The computer industry has answered with one word: **PLUGINS**.

## Plugins

Plugins share a common interface and are dedicated to specific kinds of tasks. They can be bundled with an application or distributed as separate packages.

Gufo Loader manages the plugin lifecycle in a clean, type-safe way—discovering, loading, and caching them so your core application stays focused on its orchestration logic.

Depending on the requirements, plugins can be:

* [Subclasses of a given base class](examples/subclass.md).
* [Protocols sharing a structural interface](examples/protocol.md).
* [Singleton instances of a given class](examples/singleton.md).

## Features

* **Full static typing** — Generic type parameter preserves plugin types through the entire API; zero `Any` leakage.
* **Dictionary-like interface** — Intuitive `loader[name]`, `loader.get(name)`, and iteration over keys/values/items.
* **Lazy loading and caching** — Plugins are imported on first request and cached for subsequent calls.
* **Thread-safe** — Built-in locking protects the discovery cache from concurrent access.
* **Three schemes** — Subclass, singleton (instance), and protocol-based plugin discovery.
* **No registration overhead** — Plugins live in plain Python packages; the loader discovers them automatically.
* **Security-first** — Strict mode rejects missing base packages at initialization; exclude lists filter known-safe names.

## On Gufo Stack

This product is part of [Gufo Stack][Gufo Stack] — a collaborative effort led by [Gufo Labs][Gufo Labs]. Our goal is to build a robust, flexible toolkit for network management software and automation.

We extract proven technologies from the [NOC][NOC] project, refine their APIs, performance, documentation, and testing as standalone packages. NOC consumes these as final external dependencies. Other products benefit from Gufo Stack too — better shared tools make better infrastructure.

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[NOC]: https://getnoc.com/
[Protocols]: examples/protocol.md
[Singleton instances]: examples/singleton.md
