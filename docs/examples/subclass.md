# Subclass Scheme

The *subclass* scheme is the simplest to implement and to understand.
We need the base class to define the scheme, then inherit the plugins.

## Plugin Base

First, let's define the plugins base class:

```  py title="base.py" linenums="1"
--8<-- "examples/subclass/myapp/base.py"
```

The code is straightforward

```  py title="base.py" linenums="1" hl_lines="1"
--8<-- "examples/subclass/myapp/base.py"
```

Define a base class for our plugins. We have no particular requirements,
so we can derive it from `object`.

```  py title="base.py" linenums="1" hl_lines="2 3 4"
--8<-- "examples/subclass/myapp/base.py"
```

Though docstrings are advisory, it will help to navigate our code,
so describe plugin tasks and features.

```  py title="base.py" linenums="1" hl_lines="6"
--8<-- "examples/subclass/myapp/base.py"
```

Our main function of the plugin, do not to forget to place the proper type hints to allow
static type checking.

```  py title="base.py" linenums="1" hl_lines="7 8 9"
--8<-- "examples/subclass/myapp/base.py"
```

The main function of the plugin already should be documented.

```  py title="base.py" linenums="1" hl_lines="10"
--8<-- "examples/subclass/myapp/base.py"
```

Ellipses operator (`...`) shows the implementation is abstract. 
If missed, [mypy](https://mypy.readthedocs.io/en/stable/)
will complain the function doesn't return an integer value.

## Application Core
First, lets define the application's core:

``` py title="__main__.py" linenums="1"
--8<-- "examples/subclass/myapp/__main__.py"
```

Lets explain the code:

``` py title="__main__.py" linenums="1" hl_lines="1 2"
--8<-- "examples/subclass/myapp/__main__.py"
```

Import the Python modules `sys` and `typing`. We need the `typing` to define the loader's type.
`sys` is used to parse the CLI argument.

!!! warning

    We use `sys.argv` only for demonstration purposes. Use `argsparse` or alternatives
    in real-world applications.

``` py title="__main__.py" linenums="1" hl_lines="3"
--8<-- "examples/subclass/myapp/__main__.py"
```

Import `Loader` class.

``` py title="__main__.py" linenums="1" hl_lines="4"
--8<-- "examples/subclass/myapp/__main__.py"
```

Import `PluginBase` class to define `Loader` type.

``` py title="__main__.py" linenums="1" hl_lines="6"
--8<-- "examples/subclass/myapp/__main__.py"
```

Then let's create a loader instance. You need only one loader instance per each type for your application. So loaders are usually singletons.

Loader is the generic type, so we must pass the exact plugin type. In the subclass scheme
plugins are classes, derived from the `BasePlugin` class. In Python's typing terms,
the subclass of `BasePlugin` has the `Type[BasePlugin]` type. We'd placed the type into
the brackets just after the `Loader`.

After defining the plugin's type, we need to initialize the loader itself.
Loader has several initialization parameters, see [Reference](../reference.md#src.gufo.loader.Loader)
for details. Here we consider our plugins will be in `plugins` folder of our applications.

``` py title="__main__.py" linenums="1" hl_lines="9"
--8<-- "examples/subclass/myapp/__main__.py"
```

Our `main` function accepts the operation's name and two integer arguments.
Then it prints the result.

``` py title="__main__.py" linenums="1" hl_lines="10"
--8<-- "examples/subclass/myapp/__main__.py"
```

Loader supports dict-like interface to access the modules. For this example, we will 
use bracket notation. We use `op` parameter as the plugin name.

``` py title="__main__.py" linenums="1" hl_lines="11"
--8<-- "examples/subclass/myapp/__main__.py"
```

Loader returns the class. We create the instance to show we can use some plugin initialization
tasks. We can also define the `execute` method as a `@classmethod` to skip 
the initialization step.

``` py title="__main__.py" linenums="1" hl_lines="12"
--8<-- "examples/subclass/myapp/__main__.py"
```

Then we call `execute` method of the plugin. Your editor must
show the `r` variable has the type of `int`

``` py title="__main__.py" linenums="1" hl_lines="13"
--8<-- "examples/subclass/myapp/__main__.py"
```

Then we print the result, and our core function is finally complete.

``` py title="__main__.py" linenums="1" hl_lines="16"
--8<-- "examples/subclass/myapp/__main__.py"
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
--8<-- "examples/subclass/myapp/plugins/add.py"
```

The code is pretty and clean

``` py title="plugins/add.py" linenums="1" hl_lines="1"
--8<-- "examples/subclass/myapp/plugins/add.py"
```
Import the base class `BasePlugin`. Note, we use relative import to clean up our code.

``` py title="plugins/add.py" linenums="1" hl_lines="4"
--8<-- "examples/subclass/myapp/plugins/add.py"
```
Create new plugin class and inherit it from `BasePlugin`.

``` py title="plugins/add.py" linenums="1" hl_lines="5"
--8<-- "examples/subclass/myapp/plugins/add.py"
```
Then override the `execute` function.

``` py title="plugins/add.py" linenums="1" hl_lines="6"
--8<-- "examples/subclass/myapp/plugins/add.py"
```
All we need is to add two numbers and return the result. Our plugin is complete.

### sub Plugin

Let's create another plugin for subtraction.
Our plugin has the name `sub`, so we're placing it into `sub.py` file.

``` py title="plugins/sub.py" linenums="1"
--8<-- "examples/subclass/myapp/plugins/sub.py"
```

Pretty like the `add` plugin, only the class name and implementation differ.

``` py title="plugins/sub.py" linenums="1" hl_lines="6"
--8<-- "examples/subclass/myapp/plugins/sub.py"
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

We have learned how to create simple and extendable applications using subclass-based
approach.