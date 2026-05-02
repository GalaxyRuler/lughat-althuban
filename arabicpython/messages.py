"""Arabic user-facing messages shared by CLI tools."""

from __future__ import annotations

import argparse

from arabicpython._generated_messages import MESSAGES


def msg(key: str) -> str:
    """Return a shared Arabic message."""
    return MESSAGES[key]


class ArabicArgumentParser(argparse.ArgumentParser):
    """ArgumentParser with Arabic headings in generated help output."""

    _REPLACEMENTS = {
        "usage:": "الاستخدام:",
        "positional arguments:": "المعاملات الموضعية:",
        "optional arguments:": "الخيارات:",
        "options:": "الخيارات:",
        "show this help message and exit": "اعرض هذه المساعدة ثم اخرج",
    }

    def format_usage(self) -> str:
        return self._arabicize(super().format_usage())

    def format_help(self) -> str:
        return self._arabicize(super().format_help())

    @classmethod
    def _arabicize(cls, text: str) -> str:
        for old, new in cls._REPLACEMENTS.items():
            text = text.replace(old, new)
        return text
