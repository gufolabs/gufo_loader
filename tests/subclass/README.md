# Subclass tests packages

All plugins are the classes derived from `BasePlugin` class defined in the`base.py`. Multiple instances of plugin may be instantiated by loader users.

Contains files:

* `base.py` - contains `BasePlugin` class.
* `primary/` - primary plugin package. Take precedence over `secondary/`.
  
  * `__init__.py` - empty file to denote package.
  * `a.py` - `a` plugin.
  * `b.py` - `b` plugin.

* `secondary/` - secondary plugin package. Overload by `primary/`.

  * `__init__.py` - empty file to denote package.
  * `b.py` - should be hidden by `primary/a.py`.
  * `c.py` - `c` plugin, contains additional.decoy classes and variables to mess the loader
  * `d.py` - imports plugin from another module, must be ignored.