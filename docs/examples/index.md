# Gufo Loader Examples

Consider the practical task. Let's write the simple integer calculator application.
The application must be called from the command line, accept the operation name and two
integer arguments, perform the operation and print the result.

I.e.

```
$ python -m myapp add 1 2
3
```

We'll learn 3 possible implementations, each with its own strong and weak sides:

* [Subclasses of the given class](subclass.md).
* [Classes sharing the protocol](protocol.md).
* [Singleton instances of the given class](singleton.md).
