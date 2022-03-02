# Gufo Labs Loader

Generic class loader for robust plugin infrastructure.
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