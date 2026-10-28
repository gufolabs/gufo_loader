# ---------------------------------------------------------------------
# Gufo Loader: Subclass tests
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from typing import Any

# Third-party modules
import pytest

# Gufo Loader modules
from gufo.loader import Loader
from gufo.loader.loader import ModulePolicy

from .subclass.base import BasePlugin

PLUGIN_BASES = ["tests.subclass.primary", "tests.subclass.secondary"]
LoaderType = Loader[type[BasePlugin]]


@pytest.fixture(scope="module")
def loader() -> LoaderType:
    return Loader[type[BasePlugin]](bases=PLUGIN_BASES)


@pytest.mark.parametrize(
    ("name", "expected_name"),
    [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
    ],
)
def test_getitem(name: str, expected_name: str, loader: LoaderType) -> None:
    kls = loader[name]
    assert issubclass(kls, BasePlugin)
    item = kls()
    assert item.get_name() == expected_name


@pytest.mark.parametrize(
    ("module_policy", "expected_name"),
    [
        (ModulePolicy.STRICT, None),
        (ModulePolicy.RELAXED, "c"),
    ],
)
def test_module_policy(module_policy: ModulePolicy, expected_name: str | None) -> None:
    loader = Loader[type[BasePlugin]](
        base="tests.subclass.secondary",
        module_policy=module_policy,
    )

    kls = loader.get("d")

    if expected_name is None:
        assert kls is None
    else:
        assert kls is not None
        assert kls().get_name() == expected_name


class T1:
    pass


class T2(T1):
    pass


class T3:
    pass


@pytest.mark.parametrize(
    ("x", "expected"),
    [(T1, True), (T2, True), (T3, False), (True, False)],
)
def test_subclass_validator(x: Any, expected: bool) -> None:  # noqa:ANN401
    validator = Loader._is_subclass_validator(T1)
    r = validator(x)
    assert r is expected
