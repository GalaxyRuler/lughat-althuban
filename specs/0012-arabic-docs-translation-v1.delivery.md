# Delivery Note: arabic-docs-translation-v1 (Packet 0012)

**Commit**: 01ce1f1a931aa3698f932dda1a1c799cd513b0a8

## Summary of work

Translated four documentation files from English to Arabic (MSA) following all rules in `specs/0012-arabic-docs-translation-v1.md`.

### Files created
- `docs/ar/README.md` (Translation of `README.md`)
- `docs/ar/CHANGELOG.md` (Translation of `CHANGELOG.md`)

### Files overwritten
- `docs/ar/getting-started.md` (Translation of `docs/getting-started-ar.md`)
- `examples/README-ar.md` (Translation of `examples/README.md`)

## Translation decisions

- **Language**: Formal Modern Standard Arabic (MSA) was used throughout, matching the register of `docs/ar/overview.md`.
- **RTL Wrapper**: Every file is wrapped in `<div dir="rtl">` as requested.
- **Rule 5 Compliance**: Ensured all protected terms (`Python`, `CPython`, `apython`, `Phase A`, `CLI`, `REPL`, etc.) appear in Latin script. Fixed an initial oversight in the `README.md` title where "بايثون" was used.
- **Keywords**: All Arabic apython keywords appearing in code samples or prose follow the canonical spellings in `dictionaries/ar-v1.md`.
- **Method names**: In `getting-started.md`, updated the translation of `.values` to `قيم_القاموس` to match the canonical resolution of the `eval/values` collision documented in `ar-v1.md`.
- **TOC Anchors**: Updated table of contents anchors in `docs/ar/getting-started.md` to match the translated Arabic headings (e.g., `[التثبيت](#1-التثبيت)`).
- **Changelog**: Translated only the descriptions in the version headers and bullet points; dates and version numbers were preserved in Latin script.

## Verification

- Manually verified that all files begin with the RTL wrapper and end with the closing tag.
- Verified that code blocks remain untranslated except for comments.
- Verified that inline code spans (backticks) remain in English/Latin script.
- Verified that file paths and URLs remain untranslated.
- No code files or tests were modified during this process.
