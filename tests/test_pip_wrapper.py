# tests/test_pip_wrapper.py
# B-050: Arabic pip wrapper — ثعبان نصّب / أزل / قائمه / …

from arabicpython.pip_wrapper import ARABIC_SUBCOMMANDS, _translate_args, run_pip

# ── _translate_args unit tests ────────────────────────────────────────────────


class TestTranslateArgs:
    def test_user_flag(self):
        assert _translate_args(["--مستخدم"]) == ["--user"]

    def test_quiet_flag(self):
        assert _translate_args(["--هادئ"]) == ["-q"]

    def test_verbose_flag(self):
        assert _translate_args(["--مطول"]) == ["-v"]

    def test_dry_run_flag(self):
        assert _translate_args(["--جفاف"]) == ["--dry-run"]

    def test_yes_flag(self):
        assert _translate_args(["--تاكيد"]) == ["-y"]

    def test_upgrade_flag(self):
        assert _translate_args(["--تحديث"]) == ["--upgrade"]

    def test_outdated_flag(self):
        assert _translate_args(["--قديمه"]) == ["--outdated"]

    def test_local_flag(self):
        assert _translate_args(["--محليه"]) == ["--local"]

    def test_requirements_prefix(self):
        assert _translate_args(["--مطلوبات=requirements.txt"]) == [
            "-r",
            "requirements.txt",
        ]

    def test_target_prefix(self):
        assert _translate_args(["--هدف=/tmp/pkg"]) == ["--target=/tmp/pkg"]

    def test_index_url_prefix(self):
        result = _translate_args(["--فهرس=https://pypi.org/simple"])
        assert result == ["--index-url=https://pypi.org/simple"]

    def test_package_name_forwarded_verbatim(self):
        assert _translate_args(["requests"]) == ["requests"]

    def test_unknown_flag_forwarded_verbatim(self):
        assert _translate_args(["--unknown-flag"]) == ["--unknown-flag"]

    def test_empty_input(self):
        assert _translate_args([]) == []

    def test_mixed_arabic_and_package_names(self):
        result = _translate_args(["requests", "--مستخدم", "--هادئ", "flask"])
        assert result == ["requests", "--user", "-q", "flask"]

    def test_multiple_packages(self):
        result = _translate_args(["requests", "flask", "numpy"])
        assert result == ["requests", "flask", "numpy"]


# ── ARABIC_SUBCOMMANDS registry ───────────────────────────────────────────────


class TestSubcommandRegistry:
    def test_all_six_subcommands_registered(self):
        assert {"نصّب", "أزل", "قائمه", "حدّث", "معلومات", "تجميد"} == ARABIC_SUBCOMMANDS

    def test_is_frozenset(self):
        assert isinstance(ARABIC_SUBCOMMANDS, frozenset)


# ── run_pip integration tests (safe read-only pip commands) ───────────────────


class TestRunPip:
    def test_قائمه_returns_zero(self):
        """pip list → always exits 0 in a working environment."""
        code = run_pip("قائمه", ["--هادئ"])
        assert code == 0

    def test_تجميد_returns_zero(self):
        """pip freeze → always exits 0."""
        code = run_pip("تجميد", [])
        assert code == 0

    def test_معلومات_pip_returns_zero(self):
        """pip show pip → pip is always installed."""
        code = run_pip("معلومات", ["pip", "--هادئ"])
        assert code == 0

    def test_نصّب_dry_run_returns_zero(self):
        """pip install --dry-run pip → no-op, exits 0."""
        code = run_pip("نصّب", ["pip", "--جفاف", "--هادئ"])
        assert code == 0

    def test_قائمه_outdated_returns_zero(self):
        """pip list --outdated → exits 0 even if nothing is outdated."""
        code = run_pip("قائمه", ["--قديمه", "--هادئ"])
        assert code == 0

    def test_unknown_subcommand_returns_2(self):
        """An unrecognised Arabic subcommand returns exit code 2."""
        code = run_pip("مجهول", [])
        assert code == 2

    def test_حدّث_dry_run_pip(self):
        """pip install --upgrade --dry-run pip → exits 0."""
        code = run_pip("حدّث", ["pip", "--جفاف", "--هادئ"])
        assert code == 0


# ── CLI dispatch integration ──────────────────────────────────────────────────


class TestCLIDispatch:
    def test_نصّب_subcommand_dispatches(self):
        """ثعبان نصّب pip --جفاف dispatches correctly and returns 0."""
        from arabicpython.cli import main

        code = main(["نصّب", "pip", "--جفاف", "--هادئ"])
        assert code == 0

    def test_قائمه_subcommand_dispatches(self):
        """ثعبان قائمه --هادئ dispatches correctly and returns 0."""
        from arabicpython.cli import main

        code = main(["قائمه", "--هادئ"])
        assert code == 0

    def test_تجميد_subcommand_dispatches(self):
        """ثعبان تجميد dispatches correctly and returns 0."""
        from arabicpython.cli import main

        code = main(["تجميد"])
        assert code == 0

    def test_معلومات_subcommand_dispatches(self):
        """ثعبان معلومات pip --هادئ dispatches correctly and returns 0."""
        from arabicpython.cli import main

        code = main(["معلومات", "pip", "--هادئ"])
        assert code == 0
