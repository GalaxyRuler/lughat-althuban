"""Placeholder test so CI has something to run in Phase 0."""

import arabicpython


def test_version_defined():
    assert isinstance(arabicpython.__version__, str)
    assert arabicpython.__version__ != ""
