# Attribute test plugins

The `plugins/` package contains modules whose plugin instance is exposed
through the fixed `singleton` attribute. `example.py` also exports a second
valid plugin instance as a decoy, so the test verifies that `Loader` selects
only the configured attribute.
