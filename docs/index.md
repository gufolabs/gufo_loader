---
template: index.html
hide:
    - navigation
    - toc
hero:
    title: Gufo Loader
    subtitle: The flexible and robust foundation for Python plugins architecture
    install_button: Getting Started
    source_button: Source Code
---
## Software Evolution

Software tends to grow larger and larger. Even the small
pet projects may end as the huge monsters. Software growth
imposes new challenges:

* Large amounts of code are hard to test and maintain.
* Software is complex. Only small amount of functions is 
  necessary for the single users' task. But all of them are present
  and consume the memory. Large amount of unused functions
  affect application load time.
* Software should be extendable. Users would add the new functions
  to tie software to their needs. Third-party developers should offer
  the packs of the new functions.  

Software developers adopted the modular approach decades ago.
Functions may be groupped into larger units, called the modules.
Sometimes, the modules form the groups, when each member of 
group interacts with the rest of application in similar way.
The way of interaction is the interface. Interfaces are the
barriers, separating parts of applications from each other.
Each side of application may realize the part over the barries
as the black box. Internals of the black box doesn't matter all all.
Only the interface matters.

The breaktrough is the fact that such black boxes are changeable.
Black box must perform some kind of function, regardless of implementation
and of the final result. Just replace the box with another one and application
will act differently. Black boxes is relatilevy small and observable
and may be tested as the independed entity.

So the software may be designed as the orchestration core, which
communnicates and distributes the tasks to the black boxes, leaving
all the complexity and the dirty job to them.

We'd got rid of the complexity and the application may be extended
in relatively easy way. But how to use only boxes necessary for the user's
taks? How to replace the boxes? How to add the own ones?

Computer software industry has developed a mighty spell. Let's shout it:
**PLUGINS**.

## Plugins

Plugins are modules, sharing common interface and dedicated to particular kind
of tasks. Developers may pack plugins along with application or distribute them
as the separate packs.

## The Loader

*Gufo Loader* is the simple Python library supplied with the best practices.
Loader managed the Python plugins lifecycle in the clean and sound way. Application
core may use the Loader to enumerate and load the plugins.

Depending on the requirements, Plugins may be:

* [Subclasses of the given class](examples/subclass.md).
* [Classes sharing the protocol](examples/protocol.md).
* [Singleton instances of the given class](examples/singleton.md).

## Features

* Clean dict-like API.
* Full abstraction from the plugin internals.
* Custom plugins.
* Full Python typing support.
* Editor completion.
* Well-tested, battle-proven code.
* 100% test coverage.

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