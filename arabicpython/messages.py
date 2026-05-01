"""Arabic user-facing messages shared by CLI tools."""

from __future__ import annotations

import argparse

MESSAGES: dict[str, str] = {
    "cli.description": "لغة الثعبان، مشغّل بايثون العربي.",
    "cli.dict_help": "اختر نسخة القاموس.",
    "cli.stdin_read_error": "تعذر قراءة الإدخال القياسي",
    "cli.open_file_error": "تعذر فتح الملف",
    "cli.is_directory": "المسار مجلد وليس ملفا",
    "cli.missing_file": "الملف غير موجود",
    "cli.invalid_utf8": "ترميز الملف ليس UTF-8 صالحا",
    "cli.dictionary_conflict": "تعارض في نسخة القاموس",
    "cli.unknown_dictionary": "نسخة القاموس غير معروفة",
    "cli.keyboard_interrupt": "مقاطعة_لوحة_المفاتيح",
    "formatter.description": "نسّق ملفات .apy.",
    "formatter.check_help": "لا تكتب التغييرات، واخرج برمز 1 إذا احتاج أي ملف إلى تنسيق.",
    "formatter.file_not_found": "الملف غير موجود",
    "formatter.would_reformat": "سيعاد تنسيقه",
    "formatter.reformatted": "أعيد تنسيقه",
    "formatter.already_formatted": "منسق مسبقا",
    "linter.description": "راجع ملفات .apy.",
    "linter.no_info_help": "أخف تشخيصات المعلومات.",
    "linter.select_help": "قائمة رموز التشخيص المراد تفعيلها، مفصولة بفواصل.",
    "linter.file_not_found": "الملف غير موجود",
    "linter.missing_intro": "لا يحتوي الملف على تعليق أو توثيق علوي",
    "linter.line_too_long": "السطر طويل",
    "linter.trailing_whitespace": "مسافة زائدة في نهاية السطر",
    "linter.tab_indentation": "إزاحة بعلامة جدولة؛ استخدم 4 مسافات",
    "linter.mixed_identifier": "معرّف يمزج العربية واللاتينية",
    "pretokenize.bidi_control": "حرف تحكم باتجاه النص غير مسموح خارج النصوص الحرفية",
    "pretokenize.bidi_reason": "راجع https://trojansource.codes لمعرفة السبب",
    "pretokenize.mixed_digits": "مزج أنظمة الأرقام داخل العدد غير مسموح",
    "pretokenize.one_digit_system": "استخدم نظام أرقام واحدا في العدد",
    "aliases.unmapped_module_warning": "الاسم العربي غير موجود في خريطة الوحدة المنسقة",
    "aliases.unmapped_module_attribute": "لا تملك الوحدة العربية هذه الصفة",
    "aliases.unmapped_instance_warning": "الاسم العربي غير موجود في خريطة الكائن المنسقة",
    "aliases.unmapped_instance_attribute": "لا يملك الكائن هذه الصفة العربية",
    "kernel.missing_jupyter_client": (
        "الحزمة jupyter_client غير مثبتة. ثبّتها بالأمر: pip install jupyter_client"
    ),
    "kernel.installed_kernel": "ثُبّتت مواصفة النواة",
    "kernel.install_help": "ثبّت مواصفة النواة في Jupyter.",
    "kernel.translation_error": "خطأ في الترجمة",
}


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
