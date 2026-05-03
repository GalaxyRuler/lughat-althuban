from __future__ import annotations

import contextlib
import io
import os
import re
from pathlib import Path

import pytest

from arabicpython.translate import translate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYGROUND = PROJECT_ROOT / "docs" / "playground.html"
BRAND_CSS = PROJECT_ROOT / "docs" / "brand.css"
GITHUB_PAGES = [
    PROJECT_ROOT / "docs" / "index.html",
    PROJECT_ROOT / "docs" / "gallery.html",
    PLAYGROUND,
]
EXAMPLE_RE = re.compile(
    r'^  \{\s*\n\s*id:\s*"(?P<id>[^"]+)"(?P<body>.*?)(?=^  \},?\s*$)',
    re.M | re.S,
)
CODE_RE = re.compile(r"code:\s*`(?P<code>.*?)`", re.S)
SOURCE_RE = re.compile(r'source:\s*"(?P<source>[^"]+)"')
LIBRARIES_RE = re.compile(r"libraries:\s*\[(?P<libraries>.*?)\]", re.S)
STRING_RE = re.compile(r'"(?P<path>[^"]+)"')
LATIN_LETTER_RE = re.compile(r"[A-Za-z]")
EXAMPLE_INPUTS = {
    "desert-treasure": ["شرق", "شرق", "شمال", "بحث"],
}


def _library_paths(body: str) -> list[Path]:
    libraries_match = LIBRARIES_RE.search(body)
    if not libraries_match:
        return []
    return [
        PLAYGROUND.parent / match.group("path")
        for match in STRING_RE.finditer(libraries_match.group("libraries"))
    ]


def _playground_examples() -> list[tuple[str, str]]:
    html = PLAYGROUND.read_text(encoding="utf-8")
    examples = []
    for match in EXAMPLE_RE.finditer(html):
        example_id = match.group("id")
        body = match.group("body")
        code_match = CODE_RE.search(body)
        if code_match:
            examples.append((example_id, code_match.group("code")))
            continue

        source_match = SOURCE_RE.search(body)
        if source_match:
            parts = [
                source_path.read_text(encoding="utf-8") for source_path in _library_paths(body)
            ]
            source_path = PLAYGROUND.parent / source_match.group("source")
            parts.append(source_path.read_text(encoding="utf-8"))
            examples.append((example_id, "\n\n".join(parts)))
            continue

        raise AssertionError(f"playground example {example_id!r} has no code or source")

    assert examples
    return examples


def _external_example_sources() -> list[Path]:
    html = PLAYGROUND.read_text(encoding="utf-8")
    sources = []
    for match in EXAMPLE_RE.finditer(html):
        body = match.group("body")
        sources.extend(_library_paths(body))
        source_match = SOURCE_RE.search(body)
        if source_match:
            sources.append(PLAYGROUND.parent / source_match.group("source"))

    unique_sources = list(dict.fromkeys(sources))
    assert unique_sources
    return unique_sources


PLAYGROUND_EXAMPLES = _playground_examples()
EXTERNAL_EXAMPLE_SOURCES = _external_example_sources()


def _assert_no_latin_in_text_values(value: object) -> None:
    if isinstance(value, str):
        assert not LATIN_LETTER_RE.search(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            _assert_no_latin_in_text_values(key)
            _assert_no_latin_in_text_values(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _assert_no_latin_in_text_values(item)


@pytest.mark.parametrize(
    ("example_id", "source"),
    PLAYGROUND_EXAMPLES,
    ids=[example_id for example_id, _ in PLAYGROUND_EXAMPLES],
)
def test_playground_example_output_stays_arabic_first(
    monkeypatch: pytest.MonkeyPatch,
    example_id: str,
    source: str,
) -> None:
    if example_id in {"city-jump", "asteroid-guard"}:
        pytest.importorskip("pygame", reason="pygame-ce required for the Pygame platformer")
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        from arabicpython import install_aliases

        install_aliases()

    stdout = io.StringIO()
    stderr = io.StringIO()
    translated = translate(source)
    compiled = compile(translated, f"<playground:{example_id}>", "exec")
    answers = iter(EXAMPLE_INPUTS.get(example_id, []))

    def fake_input(prompt: object = "") -> str:
        with contextlib.suppress(StopIteration):
            return next(answers)
        return ""

    monkeypatch.setattr("builtins.input", fake_input)
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(compiled, {"__name__": "__main__"})  # noqa: S102

    output = stdout.getvalue() + stderr.getvalue()
    assert not LATIN_LETTER_RE.search(output), (
        f"{example_id} printed Latin letters; playground examples must keep "
        f"runtime output Arabic-first.\n{output}"
    )


@pytest.mark.parametrize(
    "source_path",
    EXTERNAL_EXAMPLE_SOURCES,
    ids=[source_path.stem for source_path in EXTERNAL_EXAMPLE_SOURCES],
)
def test_external_playground_sources_use_no_latin_letters(source_path: Path) -> None:
    source = source_path.read_text(encoding="utf-8")
    assert not LATIN_LETTER_RE.search(source)


def test_smart_city_showcase_runs_as_complex_arabic_program() -> None:
    source = (PROJECT_ROOT / "docs" / "showcases" / "مدينة_ذكية.apy").read_text(encoding="utf-8")
    namespace: dict[str, object] = {}

    exec(compile(translate(source), "<smart-city>", "exec"), namespace)  # noqa: S102

    state = namespace["ابدا"]()
    assert len(state["الأحياء"]) == 4
    assert len(state["العقد"]) == 9
    assert len(state["الروابط"]) >= 16
    assert state["المحدد"] == "النخيل"
    assert state["مدة_الجولة"] == 7
    assert state["هدف_الاستقرار"] == 60
    assert state["إنذار"]["اسم"] == "انقطاع كهرباء"
    assert state["إنذار"]["نوع"] == "كهرباء"
    assert state["المسار"] == ["المركز", "السوق", "المستشفى", "الشمال"]

    state = namespace["اختر_حي"]("الميناء")
    assert state["المحدد"] == "الميناء"
    assert state["المسار"] == ["المركز", "الميناء", "البحر"]

    state = namespace["نفذ_قرار"]("كهرباء")
    assert state["ميزانية"] == 10
    assert state["اليوم"] == 2
    assert state["إنذار"]["اسم"] == "تسرب ماء"
    assert "تنبؤ" in state
    assert state["نتيجة"] == "قيد اللعب"

    state = namespace["نفذ_قرار"]("كهرباء")
    assert state["ميزانية"] == 5
    assert state["اليوم"] == 3
    assert state["إنذار"]["اسم"] == "اختناق مروري"

    _assert_no_latin_in_text_values(state)


def test_smart_city_showcase_has_visual_playground_surface() -> None:
    html = PLAYGROUND.read_text(encoding="utf-8")
    assert 'class="city-map-wrap"' in html
    assert 'data-city-action="كهرباء"' in html
    assert 'data-city-action="مرور"' in html
    assert '_smart_city_ns["نفذ_قرار"]' in html


def test_city_jump_platformer_runs_with_arabic_pygame_api() -> None:
    pytest.importorskip("pygame", reason="pygame-ce required for the Pygame platformer")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    from arabicpython import install_aliases

    install_aliases()
    game_source = (PROJECT_ROOT / "docs" / "games" / "قفزة_المدينة.apy").read_text(encoding="utf-8")
    source = game_source
    namespace: dict[str, object] = {}

    exec(compile(translate(source), "<city-jump>", "exec"), namespace)  # noqa: S102

    state = namespace["ابدا"]()
    assert state["بطل"]["قلوب"] == 3
    assert state["المطلوب"] == 5
    assert len(state["منصات"]) >= 7
    assert len(state["أخطار"]) == 3

    start_x = state["بطل"]["س"]
    for command in ["يمين", "يمين قفز", "يمين", "يمين"]:
        state = namespace["نفذ_امر"](command)

    assert state["بطل"]["س"] > start_x
    assert "بطل" in state
    assert "باب" in state
    _assert_no_latin_in_text_values(state)


def test_city_jump_platformer_has_visual_playground_surface() -> None:
    html = PLAYGROUND.read_text(encoding="utf-8")
    assert 'id="platform-panel"' in html
    assert 'id="platform-stage" tabindex="0"' in html
    assert 'class="platform-canvas"' in html
    assert 'pyodide.loadPackage("pygame-ce")' in html
    assert 'sys.modules["لعبه"] = لعبه' in html
    assert 'data-platform-command="قفز"' in html
    assert 'id="platform-control-hint"' in html
    assert "← → ↑ / مسافة" in html
    assert 'aria-keyshortcuts="ArrowLeft KeyA"' in html
    assert 'aria-keyshortcuts="ArrowUp Space KeyW"' in html
    assert 'aria-keyshortcuts="ArrowRight KeyD"' in html
    assert "let platformerJumpQueued = false;" in html
    assert 'command === "قفز" && isPressed' in html
    assert 'event.code === "KeyA"' in html
    assert 'event.code === "KeyD"' in html
    assert 'event.code === "KeyW"' in html
    assert '_platformer_ns["نفذ_امر"]' in html
    assert ".platform-controls {\n      direction: ltr;" in html
    assert html.index('data-platform-command="يسار"') < html.index('data-platform-command="قفز"')
    assert html.index('data-platform-command="قفز"') < html.index('data-platform-command="يمين"')


def test_asteroid_guard_runs_with_arabic_pygame_api() -> None:
    pytest.importorskip("pygame", reason="pygame-ce required for the Pygame arcade game")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    from arabicpython import install_aliases

    install_aliases()
    game_source = (PROJECT_ROOT / "docs" / "games" / "حارس_الكويكبات.apy").read_text(
        encoding="utf-8"
    )
    namespace: dict[str, object] = {}

    exec(compile(translate(game_source), "<asteroid-guard>", "exec"), namespace)  # noqa: S102

    state = namespace["ابدا"]()
    assert state["دروع"] == 3
    assert state["موجة"] == 1
    assert state["كويكبات"] >= 4
    assert state["نقاط"] == 0

    for command in ["اندفاع", "يمين", "إطلاق", "إطلاق", "يسار درع"]:
        state = namespace["نفذ_امر"](command)

    assert state["طلقات"] >= 1
    assert state["طاقة_درع"] <= 100
    assert "بطل" in state
    assert "كويكبات" in state
    _assert_no_latin_in_text_values(state)


def test_asteroid_guard_thrust_releases_into_controlled_drift() -> None:
    pytest.importorskip("pygame", reason="pygame-ce required for the Pygame arcade game")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    from arabicpython import install_aliases

    install_aliases()
    game_source = (PROJECT_ROOT / "docs" / "games" / "حارس_الكويكبات.apy").read_text(
        encoding="utf-8"
    )
    namespace: dict[str, object] = {}

    exec(compile(translate(game_source), "<asteroid-guard>", "exec"), namespace)  # noqa: S102
    namespace["ابدا"]()

    def ship_speed() -> float:
        ship = namespace["السفينه"]
        return (ship["سع"] ** 2 + ship["صع"] ** 2) ** 0.5

    for _ in range(30):
        namespace["نفذ_امر"]("اندفاع")

    speed_after_thrust = ship_speed()

    for _ in range(30):
        namespace["نفذ_امر"]("")

    speed_after_release = ship_speed()

    for _ in range(90):
        namespace["نفذ_امر"]("")

    assert speed_after_thrust <= 4.0
    assert speed_after_release < speed_after_thrust * 0.35
    assert ship_speed() <= 0.1


def test_asteroid_guard_has_visual_playground_surface() -> None:
    html = PLAYGROUND.read_text(encoding="utf-8")
    game_source = (PROJECT_ROOT / "docs" / "games" / "حارس_الكويكبات.apy").read_text(
        encoding="utf-8"
    )
    assert 'id: "asteroid-guard"' in html
    assert 'source: "games/حارس_الكويكبات.apy"' in html
    assert 'const ASTEROID_ID = "asteroid-guard";' in html
    assert 'data-platform-command="اندفاع"' in html
    assert 'data-platform-command="إطلاق"' in html
    assert 'data-platform-command="درع"' in html
    assert "رياضيات.جيب_تمام = math.cos" in html
    assert "if (activeExample?.id === ASTEROID_ID)" in html
    assert "let platformerFireQueued = false;" in html
    assert 'command === "إطلاق" && platformerFireQueued' in html
    assert "keyboardOnly: true" in html
    assert "tickMs: 1000 / 60" in html
    assert "platformControls.hidden = Boolean(meta.keyboardOnly)" in html
    assert "#platform-panel.keyboard-only .platform-controls" in html
    assert "body.game-mode #examples-panel { display: none; }" in html
    assert "function focusPlatformerStage()" in html
    assert 'window.addEventListener("keydown", handlePlatformerKeyDown, { capture: true });' in html
    assert 'window.addEventListener("keyup", handlePlatformerKeyUp, { capture: true });' in html
    assert 'platformPanel.addEventListener("pointerdown"' in html
    assert "rgba(255, 247, 207" not in html
    assert "(٢٥٥، ٢٤٧، ٢٠٧)" not in game_source
    assert "لون_طلقة = (٩٤، ٢٣٤، ٢١٢)" in game_source
    assert "لون_طلقة_توهج = (٢٣٤، ١٠٣، ٨٣)" in game_source


def test_github_pages_brand_theme_uses_dark_surfaces_holistically() -> None:
    css = BRAND_CSS.read_text(encoding="utf-8")

    assert "--bg: #030712" in css
    assert "--panel: #111921" in css
    assert "--soft: #17212c" in css
    assert '.brand-mark path[fill="#111921"]' in css
    assert ".platform-canvas {\n  background: #030712;" in css

    forbidden_surface_defaults = (
        "background: #ffffff",
        "background: #FFFFFF",
        "background: #f5f6fc",
        "--bg: #f5f6fc",
        "--panel: #ffffff",
        "--panel: #FFFFFF",
        "--soft: #f5f6fc",
        "--shadow: #ffffff",
        "--shadow: #FFFFFF",
    )
    for path in [BRAND_CSS, *GITHUB_PAGES]:
        page_css = path.read_text(encoding="utf-8")
        assert 'rel="stylesheet" href="brand.css' in page_css or path == BRAND_CSS
        for forbidden in forbidden_surface_defaults:
            assert forbidden not in page_css


def test_desert_treasure_visual_api_moves_and_wins() -> None:
    source = (PROJECT_ROOT / "docs" / "games" / "كنز_الصحراء.apy").read_text(encoding="utf-8")
    namespace: dict[str, object] = {}
    exec(compile(translate(source), "<desert-treasure>", "exec"), namespace)  # noqa: S102

    state = namespace["ابدا"]()
    assert state["اللاعب"] == {"س": 3, "ص": 3}
    for command in ["شرق", "شرق", "شمال", "بحث"]:
        state = namespace["نفذ_امر"](command)

    assert state["وجد"] is True
    assert state["انتهت"] is True
    assert "الكنز" in state["رسالة"]


def test_desert_treasure_controls_keep_physical_compass_direction() -> None:
    html = PLAYGROUND.read_text(encoding="utf-8")
    assert re.search(r"\.game-controls\s*\{[^}]*direction:\s*ltr;", html, re.S)
    assert re.search(r"\.game-controls button\s*\{[^}]*direction:\s*rtl;", html, re.S)


def test_playground_does_not_use_blocked_browser_prompt() -> None:
    html = PLAYGROUND.read_text(encoding="utf-8")
    assert "window.prompt" not in html
