# Protocol Scheme

The *protocol* scheme is similar with the [subclass](subclass.md) one,
except for one point: instead of using and inheriting the base class,
we define the *Protocol*.

Python typing [protocols](https://docs.python.org/3/library/typing.html#typing.Protocol)
are the class signatures. Instead of defining the base class and inherit
from it, we define the functions and their signatures.

The major advantage of the protocol scheme is the fact we need no to import
something from the core in our plugins.

## Plugin Protocol

First, lets define the plugin's protocol

```  py title="base.py" linenums="1"
--8<-- "examples/protocol/myapp/base.py"
```

More complicated, then subclass, but still simple.

```  py title="base.py" linenums="1" hl_lines="1"
--8<-- "examples/protocol/myapp/base.py"
```

We need `Protocol` and `runtime_checkable` from the Python
`typing` module.

```  py title="base.py" linenums="1" hl_lines="4"
--8<-- "examples/protocol/myapp/base.py"
```
`@runtime_checkable` decorator is necessary for Loader
to be able to check plugins signatures. Do not forget it.

```  py title="base.py" linenums="1" hl_lines="5"
--8<-- "examples/protocol/myapp/base.py"
```
Protocols are derived from `Protocol` generic class.

```  py title="base.py" linenums="1" hl_lines="6 7 8"
--8<-- "examples/protocol/myapp/base.py"
```

Though docstrings are advisory it will help to navigate our code,
so describe plugin tasks and features.

```  py title="base.py" linenums="1" hl_lines="10"
--8<-- "examples/protocol/myapp/base.py"
```

Our plugins has no initialization parameters, so we declare plain `__init__` constructor.

```  py title="base.py" linenums="1" hl_lines="11"
--8<-- "examples/protocol/myapp/base.py"
```

All protocol functions are abstract, so we add `...` operator to skip the implementation.

```  py title="base.py" linenums="1" hl_lines="13"
--8<-- "examples/protocol/myapp/base.py"
```

Our main function of the plugin, do not to forget to place the proper type hints to allow
static type checking.

```  py title="base.py" linenums="1" hl_lines="14 15 16"
--8<-- "examples/protocol/myapp/base.py"
```

The main function of the plugin already should be documented.

```  py title="base.py" linenums="1" hl_lines="17"
--8<-- "examples/protocol/myapp/base.py"
```

Ellipses operator (`...`) shows the implementation is abstract. 
If missed, [mypy](https://mypy.readthedocs.io/en/stable/)
will complain the function doesn't return an integer value.

## Application Core
Let's define the application's core.

``` py title="__main__.py" linenums="1"
--8<-- "examples/protocol/myapp/__main__.py"
```

Almost similar to the [subclass](subclass.md#application-core) core,
except for the Loader type.

``` py title="__main__.py" linenums="1" hl_lines="1"
--8<-- "examples/protocol/myapp/__main__.py"
```

Import `sys` module to parse the CLI argument.

!!! warning

    We use `sys.argv` only for demonstration purposes. Use `argsparse` or alternatives
    in real-world applications.
``` py title="__main__.py" linenums="1" hl_lines="2"
--8<-- "examples/protocol/myapp/__main__.py"
```

Import `Loader` class.

``` py title="__main__.py" linenums="1" hl_lines="3"
--8<-- "examples/protocol/myapp/__main__.py"
```

Import `PluginBase` class to define `Loader` type.

``` py title="__main__.py" linenums="1" hl_lines="5"
--8<-- "examples/protocol/myapp/__main__.py"
```

Then let's create a loader instance. You need only one loader instance per each type for your application. So loaders are usually singletons.

Loader is the generic type, so we must pass the exact plugin type. In the protocol scheme
plugins are classes, following from the `PluginProtocol` protocol. In Python's typing terms,
the protocol type is the `PluginProtocol`. We'd placed the type into
the brackets just after the `Loader`.

After defining the plugin's type, we need to initialize the loader itself.
Loader has several initialization parameters, see [Reference](../reference.md#src.gufo_loader.Loader)
for details. Here we consider our plugins will be in `plugins` folder of our applications.

``` py title="__main__.py" linenums="1" hl_lines="8"
--8<-- "examples/protocol/myapp/__main__.py"
```

Our `main` function accepts the operation's name and two integer arguments.
Then it prints the result.

``` py title="__main__.py" linenums="1" hl_lines="9"
--8<-- "examples/protocol/myapp/__main__.py"
```

Loader supports dict-like interface to access the modules. For this example, we will 
use bracket notation. We use `op` parameter as the plugin name.

``` py title="__main__.py" linenums="1" hl_lines="10"
--8<-- "examples/protocol/myapp/__main__.py"
```

Loader returns the class. We create the instance to show we can use some plugin initialization
tasks. We can also define the `execute` method as a `@classmethod` to skip 
the initialization step.

``` py title="__main__.py" linenums="1" hl_lines="11"
--8<-- "examples/protocol/myapp/__main__.py"
```

Then we call `execute` method of the plugin. Your editor must
show the `r` variable has the type of `int`

``` py title="__main__.py" linenums="1" hl_lines="12"
--8<-- "examples/protocol/myapp/__main__.py"
```

Then we print the result, and our core function is finally complete.

``` py title="__main__.py" linenums="1" hl_lines="15"
--8<-- "examples/protocol/myapp/__main__.py"
```
We're extracting our arguments directly from `sys.argv`.
Then we call our core function. The core is complete.

## Plugins

Next we need to implement plugins itself. First, create
directory `plugins` for our plugins packages.
Then add empty `__init__.py` file. 

We're ready to write our plugins.

### add Plugin

Lets implement the plugin for adding numbers. Our plugin has the name `add`,
so we're placing it into `add.py` file.

``` py title="plugins/add.py" linenums="1"
--8<-- "examples/protocol/myapp/plugins/add.py"
```

The code is pretty and clean and ever simple than [subclass](subclass.md#add-plugin) scheme.

``` py title="plugins/add.py" linenums="1" hl_lines="1"
--8<-- "examples/protocol/myapp/plugins/add.py"
```
Create the new plugin class. Class must follow `PluginProtocol` signature
but we need no the point it explicitly. So we may derive our plugin from any class.
Let's start from `object`.

``` py title="plugins/add.py" linenums="1" hl_lines="2"
--8<-- "examples/protocol/myapp/plugins/add.py"
```
Then override the `execute` function.

``` py title="plugins/add.py" linenums="1" hl_lines="3"
--8<-- "examples/protocol/myapp/plugins/add.py"
```
All we need is to add two numbers and return the result. Our plugin is complete.

### sub Plugin

Let's create another plugin for subtraction.
Our plugin has the name `sub`, so we're placing it into `sub.py` file.

``` py title="plugins/sub.py" linenums="1"
--8<-- "examples/protocol/myapp/plugins/sub.py"
```

Pretty like the `add` plugin, only the class name and implementation differ.

``` py title="plugins/sub.py" linenums="1" hl_lines="3"
--8<-- "examples/protocol/myapp/plugins/sub.py"
```
All we need is to subtract two numbers and return the result. Our plugin is complete.

## Testing

```
$ python3 -m myapp add 1 2
3
```

```
$ python3 -m myapp sub 2 1
1
```

## Summary

We have learned how to create simple and extendable applications using protocol-based
approach.