# ---------------------------------------------------------------------
# Gufo Labs Loader:
# Examples tests
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
import sys
import os
import subprocess

# Third-party modules
import pytest


@pytest.mark.parametrize(
    ["example", "args", "expected"],
    [
        ("protocol", ["add", "1", "2"], "3"),
        ("protocol", ["sub", "2", "1"], "1"),
        ("singleton", ["add", "1", "2"], "3"),
        ("singleton", ["sub", "2", "1"], "1"),
        ("subclass", ["add", "1", "2"], "3"),
        ("subclass", ["sub", "2", "1"], "1"),
    ],
)
def test_example(example, args, expected):
    python = sys.executable
    r = subprocess.run(
        [python, "-m", "myapp"] + args,
        cwd=os.path.join("examples", example),
        env={"PYTHONPATH": os.path.join(os.getcwd(), "src")},
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    data = r.stdout.strip()
    assert data == expected
