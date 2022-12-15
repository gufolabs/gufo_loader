# Gufo Loader

*Generic Python class loader for robust plugin infrastructure*.

[![PyPi version](https://img.shields.io/pypi/v/gufo_loader.svg)](https://pypi.python.org/pypi/gufo_loader/)
![Python Versions](https://img.shields.io/pypi/pyversions/gufo_loader)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Build](https://img.shields.io/github/workflow/status/gufolabs/gufo_loader/Run%20Tests/master)
![Sponsors](https://img.shields.io/github/sponsors/gufolabs)

---

**Documentation**: [https://docs.gufolabs.com/gufo_loader/](https://docs.gufolabs.com/gufo_loader/)

**Source Code**: [https://github.com/gufolabs/gufo_loader/](https://github.com/gufolabs/gufo_loader/)

---

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

Examples:

    Plugins as the subclasses:

        loader = Loader[Type[BasePlugin]](base="myproject.plugins")

    Plugins as the singletones:

        loader = Loader[BasePlugin](base="myproject.plugins")

    Plugins as the protocols:

        loader = Loader[MyProtocol](base="myproject.plugins")

## Virtues

* Clean dict-like API.
* Full abstraction from the plugin internals.
* Custom plugins.
* Full Python typing support.
* Editor completion.
* Well-tested, battle-proven code.

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
[Gufo Stack]: https://gufolabs.com/products/gufo-stack/
[NOC]: https://getnoc.com/