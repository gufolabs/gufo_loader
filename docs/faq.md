# FAQ

    What is "Gufo"?

*Gufo* means *the Owl* in Italian.

    Why the owls?

We love owls and the viable parts of our technologies
were proven at the project, named "the Owl".

    What is "Gufo Labs"?

[Gufo Labs](https://gufolabs.com/) is the Milan-based company specialized on
network and IT consulting, and on software research.

    Why I shouldn't use the plain __import__ function?

You can use `__import__` function, but you need to add a boilerplate
code to find the real plugin implementation. Also, you need some kind
of wrapping to settle the type hinting. And you need to reimplement
it again and again in every new project. Consider the Gufo Labs Loader
as the library and the methodology, based on best practices.

    How can I load and initialize all plugins on startup?

[Loader.values()](reference.md#src.gufo.loader.Loader.values) and 
[Loader.items()](reference.md#src.gufo.loader.Loader.items) are
import the modules and perform all plugins initialization. So just wrap
them in the list:

```
list(loader.values())
```
