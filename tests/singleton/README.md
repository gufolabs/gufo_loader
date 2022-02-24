# Singleton tests packages

All plugins are the innstances of `BasePlugin` subclasses. Only one singleton instance will be instantiated during process runtime.

Contains files:

* `base.py` - contains `BaseProtocol` class.
* `primary/` - primary plugin package. Take precedence over `secondary/`.
  
  * `__init__.py` - empty file to denote package.
  * `a.py` - `a` plugin.
  * `b.py` - `b` plugin.

* `secondary/` - secondary plugin package. Overload by `primary/`.

  * `__init__.py` - empty file to denote package.
  * `b.py` - should be hidden by `primary/a.py`.
  * `c.py` - `c` plugin, contains additional.decoy classes and variables to mess the loader
  * `d.py` - imports plugin from another module, must be ignored.