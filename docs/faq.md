# FAQ

> What is "Gufo"?

*Gufo* means *the Owl* in Italian.

> Why the owls?

We love owls and the viable parts of our technologies
were proven at the project, named "the Owl".

> What is "Gufo Labs"?

[Gufo Labs](https://gufolabs.com/) is the Milan-based company specialized on
network and IT consulting, and on software research.

> What is "Gufo Stack"?

We've extracted core components behind the [NOC](https://getnoc.com/) 
and released them as independent packages, available under the terms 
of the 3-clause BSD license. Our software shares common code quality standards 
and is battle-proven under the high load. We hope our key components will help 
the engineers and the developers to build reliable networks and robust network 
management software. 
See [more for details](https://gufolabs.com/products/gufo-stack/).

> Why I shouldn't use the plain `__import__` function?

You can use `__import__` function, but you need to add a boilerplate
code to find the real plugin implementation. Also, you need some kind
of wrapping to settle the type hinting. And you need to reimplement
it again and again in every new project. Consider the Gufo Labs Loader
as the library and the methodology, based on best practices.

> How can I load and initialize all plugins on startup?

[Loader.values()](reference.md#src.gufo.loader.Loader.values) and 
[Loader.items()](reference.md#src.gufo.loader.Loader.items) are
import the modules and perform all plugins initialization. So just wrap
them in the list:

``` python
list(loader.values())
```
