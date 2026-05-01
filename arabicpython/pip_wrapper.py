"""B-050: Arabic pip wrapper — `ثعبان نصّب / أزل / قائمه / …`.

Maps Arabic subcommands and flags to their pip equivalents and delegates
execution to ``sys.executable -m pip`` so the correct environment is always
used regardless of how Python was invoked.

Arabic subcommand reference
---------------------------
نصّب   <package …>   pip install <package …>
أزل    <package …>   pip uninstall <package …>
قائمه               pip list
حدّث   <package …>   pip install --upgrade <package …>
معلومات <package …>  pip show <package …>
تجميد               pip freeze

Arabic flag reference (apply to whichever subcommand accepts them)
-------------------------------------------------------------------
--مستخدم            --user
--هادئ              -q
--مطول              -v
--جفاف              --dry-run          (install / uninstall)
--تاكيد             -y                 (uninstall: skip confirmation)
--تحديث             --upgrade          (install)
--قديمه             --outdated         (list)
--محليه             --local            (list / freeze)
--مطلوبات=<ملف>     -r <file>          (install from requirements file)
--هدف=<مجلد>        --target=<dir>     (install)
--فهرس=<رابط>       --index-url=<url>  (install)

All unrecognised arguments are forwarded verbatim to pip.
"""

from __future__ import annotations

import subprocess
import sys

# ── Subcommand map ────────────────────────────────────────────────────────────

# Maps Arabic subcommand token → (pip subcommand, list of extra pip args)
_SUBCOMMAND_MAP: dict[str, tuple[str, list[str]]] = {
    "نصّب": ("install", []),
    "أزل": ("uninstall", []),
    "قائمه": ("list", []),
    "حدّث": ("install", ["--upgrade"]),
    "معلومات": ("show", []),
    "تجميد": ("freeze", []),
}

# ── Flag map ──────────────────────────────────────────────────────────────────

_FLAG_MAP: dict[str, str] = {
    "--مستخدم": "--user",
    "--هادئ": "-q",
    "--مطول": "-v",
    "--جفاف": "--dry-run",
    "--تاكيد": "-y",
    "--تحديث": "--upgrade",
    "--قديمه": "--outdated",
    "--محليه": "--local",
}

_PREFIX_MAP: list[tuple[str, str]] = [
    ("--مطلوبات=", "-r"),
    ("--هدف=", "--target="),
    ("--فهرس=", "--index-url="),
]


def _translate_args(args: list[str]) -> list[str]:
    """Translate Arabic flags in *args* to their pip equivalents.

    Unknown arguments (package names, URLs, paths) are forwarded verbatim.
    Returns a flat list of strings suitable for appending to a pip command.
    """
    pip_args: list[str] = []
    for arg in args:
        if arg in _FLAG_MAP:
            pip_args.append(_FLAG_MAP[arg])
            continue

        matched = False
        for arabic_prefix, pip_replacement in _PREFIX_MAP:
            if arg.startswith(arabic_prefix):
                value = arg[len(arabic_prefix) :]
                if pip_replacement.endswith("="):
                    # e.g. "--target=" → "--target=<value>"
                    pip_args.append(pip_replacement + value)
                else:
                    # e.g. "-r" → ["-r", "<value>"]
                    pip_args.extend([pip_replacement, value])
                matched = True
                break

        if not matched:
            pip_args.append(arg)

    return pip_args


def run_pip(arabic_subcommand: str, args: list[str]) -> int:
    """Run a pip subcommand expressed in Arabic.

    *arabic_subcommand* is one of the keys in ``_SUBCOMMAND_MAP``.
    *args* is everything after the subcommand token; Arabic flags are
    translated, everything else is forwarded verbatim.

    Returns the pip process exit code.
    """
    if arabic_subcommand not in _SUBCOMMAND_MAP:
        sys.stderr.write(
            f"ثعبان: أمر غير معروف '{arabic_subcommand}'. "
            f"الأوامر المتاحة: {', '.join(_SUBCOMMAND_MAP)}\n"
        )
        return 2
    if any(arg in {"-h", "--help", "مساعدة"} for arg in args):
        _print_help()
        return 0

    pip_sub, extra_args = _SUBCOMMAND_MAP[arabic_subcommand]
    translated = _translate_args(args)
    cmd = [sys.executable, "-m", "pip", pip_sub, *extra_args, *translated]

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        sys.stderr.write("ثعبان: تعذّر تشغيل pip — تأكد من تثبيته.\n")
        return 1


# ── Public registry of Arabic subcommand tokens (used by cli.py) ─────────────

ARABIC_SUBCOMMANDS: frozenset[str] = frozenset(_SUBCOMMAND_MAP)


def _print_help() -> None:
    sys.stdout.write(
        "الاستخدام: ثعبان <أمر إدارة الحزم> [خيارات]\n\n"
        "الأوامر:\n"
        "  نصّب <حزمة>        ثبّت حزمة\n"
        "  أزل <حزمة>         أزل حزمة\n"
        "  قائمه              اعرض الحزم المثبتة\n"
        "  حدّث <حزمة>        حدّث حزمة\n"
        "  معلومات <حزمة>     اعرض معلومات حزمة\n"
        "  تجميد              اطبع قائمة التجميد\n\n"
        "خيارات عربية شائعة: --مستخدم، --هادئ، --مطول، --جفاف، --تاكيد، --تحديث، --قديمه، --محليه\n"
    )
