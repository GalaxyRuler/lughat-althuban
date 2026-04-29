import importlib
import pathlib
import sys

import pytest

rich = pytest.importorskip("rich", reason="rich not installed")

from rich.console import Console, Group  # noqa: E402
from rich.logging import RichHandler  # noqa: E402
from rich.markdown import Markdown  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.progress import Progress, TaskID, track  # noqa: E402
from rich.prompt import Confirm, Prompt  # noqa: E402
from rich.status import Status  # noqa: E402
from rich.table import Column, Table  # noqa: E402
from rich.tree import Tree  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent / "arabicpython" / "aliases"


@pytest.fixture()
def clean_import_state():
    original_meta_path = list(sys.meta_path)
    sys.modules.pop("ريتش", None)
    yield
    sys.modules.pop("ريتش", None)
    sys.meta_path[:] = original_meta_path


@pytest.fixture()
def ريتش_proxy():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ريتش", None, None)
    assert spec is not None, "AliasFinder did not find 'ريتش'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


def test_import_ريتش_works(clean_import_state):
    from arabicpython.aliases import install

    install()
    import ريتش

    assert ريتش.اطبع is rich.print
    assert ريتش.وحده_التحكم is Console


def test_core_symbols_resolve_correctly(ريتش_proxy):
    assert ريتش_proxy.اطبع is rich.print
    assert ريتش_proxy.افحص is rich.inspect
    assert ريتش_proxy.وحده_التحكم is Console
    assert ريتش_proxy.جدول is Table
    assert ريتش_proxy.عمود is Column
    assert ريتش_proxy.صندوق is rich.box
    assert ريتش_proxy.تقدم is Progress
    assert ريتش_proxy.تتبع is track
    assert ريتش_proxy.معرف_مهمه is TaskID
    assert ريتش_proxy.لوحه is Panel
    assert ريتش_proxy.مجموعه is Group
    assert ريتش_proxy.نص_تنسيق is Markdown
    assert ريتش_proxy.شجره is Tree
    assert ريتش_proxy.اضف is Tree.add
    assert ريتش_proxy.معالج_ريتش is RichHandler
    assert ريتش_proxy.مطالبه is Prompt
    assert ريتش_proxy.تاكيد is Confirm
    assert ريتش_proxy.حاله is Status


def test_console_can_be_instantiated_via_arabic_alias(ريتش_proxy):
    console = ريتش_proxy.وحده_التحكم(record=True)

    assert isinstance(console, Console)
    console.print("[bold green]مرحبا[/]")
    assert "مرحبا" in console.export_text(styles=False)


def test_rich_toml_loads_without_error():
    from arabicpython.aliases._loader import load_mapping

    mapping = load_mapping(ALIASES_DIR / "rich.toml")
    assert mapping.arabic_name == "ريتش"
    assert mapping.python_module == "rich"
    assert mapping.entries["وحده_التحكم"] == "console.Console"
    assert len(mapping.entries) >= 30


def test_rich_demo_imports(clean_import_state):
    from arabicpython.aliases import install as install_aliases
    from arabicpython.import_hook import install as install_apy

    install_apy()
    install_aliases()
    examples_dir = ALIASES_DIR.parent.parent / "examples"
    sys.path.insert(0, str(examples_dir))

    try:
        importlib.import_module("C15_rich_demo")
    finally:
        sys.modules.pop("C15_rich_demo", None)
        sys.path.remove(str(examples_dir))
