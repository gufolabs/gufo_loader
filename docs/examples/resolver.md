# Direct Path

Direct path scheme is a form of lazy import that resolves fully-qualified dot-separated Python object references at runtime.

## Operations

First, we define a module that implements available operations.

```  py title="ops.py" linenums="1"
--8<-- "examples/resolver/myapp/ops.py"
```

The code is straightforward.

```  py title="ops.py" linenums="1" hl_lines="1 2"
--8<-- "examples/resolver/myapp/ops.py"
```

We define function `add` which accepts two integers and returns a sum of them. The fully qualified path for this function will be `myapp.ops.add`

```  py title="ops.py" linenums="1" hl_lines="5 6"
--8<-- "examples/resolver/myapp/ops.py"
```

Then we define its `sub` counterpart. The fully qualified path for this function will be `myapp.ops.sub`

## Application Core
First, let's define the application's core:

``` py title="__main__.py" linenums="1"
--8<-- "examples/resolver/myapp/__main__.py"
```

Lets explain the code:

``` py title="__main__.py" linenums="1" hl_lines="1"
--8<-- "examples/resolver/myapp/__main__.py"
```

Import the Python modules `sys` to parse the CLI argument.

!!! warning

    We use `sys.argv` only for demonstration purposes. Use `argsparse` or alternatives
    in real-world applications.

``` py title="__main__.py" linenums="1" hl_lines="2"
--8<-- "examples/resolver/myapp/__main__.py"
```
We need a `Callable` type to define operations' signature.

``` py title="__main__.py" linenums="1" hl_lines="4"
--8<-- "examples/resolver/myapp/__main__.py"
```
We also need `ImportPartResolver` to perform lazy import.

``` py title="__main__.py" linenums="1" hl_lines="6"
--8<-- "examples/resolver/myapp/__main__.py"
```
`ImportPathResolver` provides a callable that resolves a fully-qualified import path into a Python object.

In this example, the resolver is expected to return a function that accepts two integer arguments and produces an integer result.

``` py title="__main__.py" linenums="1" hl_lines="7 8 9 10"
--8<-- "examples/resolver/myapp/__main__.py"
```

Next, we define the mapping between operation names and their implementations.


!!! note

    In this example, we do not explicitly import the modules upfront. Imports are performed lazily only when a specific operation is requested.

``` py title="__main__.py" linenums="1" hl_lines="13"
--8<-- "examples/resolver/myapp/__main__.py"
```

Our `main` function accepts the operation's name and two integer arguments. Then it prints the result.


``` py title="__main__.py" linenums="1" hl_lines="14"
--8<-- "examples/resolver/myapp/__main__.py"
```
We resolve operation names to fully-qualified import paths using the `OPS` mapping, and then resolve each path into the actual function implementation.

This is the point at which the corresponding module is imported and the target callable is loaded.

Your editor must be able to infer that `fn` is a function that accepts two integers and returns an integer.

``` py title="__main__.py" linenums="1" hl_lines="15"
--8<-- "examples/resolver/myapp/__main__.py"
```

Then we call `fn` method of the plugin. Your editor must
show the `r` variable has the type of `int`

``` py title="__main__.py" linenums="1" hl_lines="16"
--8<-- "examples/resolver/myapp/__main__.py"
```

Then we print the result, and our core function is finally complete.

``` py title="__main__.py" linenums="1" hl_lines="19"
--8<-- "examples/resolver/myapp/__main__.py"
```
We're extracting our arguments directly from `sys.argv`.
Then we call our core function. The core is complete.