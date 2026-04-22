# Spec Packet 0013: search-engine-v1

**Phase**: A (showcase app)
**Depends on**: 0001–0011 all merged
**Estimated size**: medium (2–3 sessions)

## Goal

Build a fully-functional Arabic full-text search engine written entirely in
apython (`.apy` files). The engine indexes a corpus of Arabic text documents,
computes TF-IDF relevance scores, and returns ranked results with highlighted
snippets. Every variable name, function name, class name, and comment in the
source code is in Arabic. This app exists to demonstrate that apython can
implement a non-trivial computer science algorithm in readable Arabic code.

## Non-goals

- Does not use any third-party library. stdlib only.
- Does not build a web interface — terminal only.
- Does not index non-Arabic documents (the corpus is Arabic; queries are Arabic).
- Does not implement stemming or morphological analysis — normalization only
  (same rules as apython's own `arabicpython/normalize.py`).
- Does not modify any existing project file outside `apps/search_engine/` and
  `tests/test_search_engine.py`.

## Files

### Files to create

```
apps/
└── search_engine/
    ├── docs/
    │   ├── الخوارزمي.txt
    │   ├── بيت_الحكمة.txt
    │   ├── اللغة_العربية.txt
    │   ├── علم_الفلك.txt
    │   ├── ابن_سينا.txt
    │   └── ابن_بطوطة.txt
    ├── normalizer.apy
    ├── indexer.apy
    ├── ranker.apy
    └── cli.apy

tests/
└── test_search_engine.py
```

### Files to read (do not modify)

- `arabicpython/normalize.py` — reference for the Arabic normalization rules
  to reimplement in `normalizer.apy`
- `dictionaries/ar-v1.md` — reference for apython syntax

---

## Sample documents (`apps/search_engine/docs/`)

Write 6 UTF-8 Arabic text files. Each 200–300 words of flowing MSA prose.
No headers, no bullet points — paragraphs only. Topics:

| File | Topic | Key searchable terms to include |
|------|-------|-------------------------------|
| `الخوارزمي.txt` | محمد بن موسى الخوارزمي، مخترع الجبر والخوارزميات | الجبر، الخوارزمية، الأرقام، الرياضيات، بغداد |
| `بيت_الحكمة.txt` | بيت الحكمة في بغداد، مركز الترجمة والعلوم | الترجمة، العلوم، الكتب، المعرفة، الخلافة |
| `اللغة_العربية.txt` | اللغة العربية، نشأتها، انتشارها، خصائصها | الحروف، القواعد، الشعر، الفصحى، العالم |
| `علم_الفلك.txt` | الفلكيون العرب، الأرصاد، تسمية النجوم | النجوم، الكواكب، المنازل، الأرصاد، الليل |
| `ابن_سينا.txt` | ابن سينا، القانون في الطب، الفلسفة | الطب، الجسم، العلاج، الفلسفة، الروح |
| `ابن_بطوطة.txt` | ابن بطوطة، رحلاته، تسجيل الجغرافيا | الرحلة، البلدان، البحر، المدن، السفر |

---

## Module specifications

### `normalizer.apy`

Reimplements the normalization rules from `arabicpython/normalize.py` in
apython. Exports one function: `طبّع(نص)`.

Rules (apply in order):
1. Strip harakat: remove chars in Unicode ranges `\u064B`–`\u065F` and `\u0670`
2. Strip tatweel: remove `\u0640`
3. Fold hamza variants: `أإآٱ` → `ا`
4. Fold alef-maksura: `ى` → `ي`
5. Fold ta-marbuta: `ة` → `ه`
6. Strip punctuation: remove `،؛؟.,!؟:()[]{}«»`
7. Lowercase (for any Latin characters that might appear)

```python
# expected behaviour
طبّع("الكِتَابُ")   # → "الكتاب"
طبّع("قيمة")        # → "قيمه"
طبّع("إذا")         # → "اذا"
طبّع("مُحَمَّد")    # → "محمد"
```

### `indexer.apy`

Class `فهرس`:

```python
صنف فهرس:
    دالة __init__(الذات, مسار_المجلد):
        # يحمّل كل ملفات .txt من المجلد
        # يبني: الذات.الوثائق = {معرف: {"الاسم": ..., "النص": ..., "الكلمات": [...]}}
        # يبني: الذات.الفهرس_المعكوس = {كلمة_مطبّعة: {معرف: [مواضع]}}
        # يبني: الذات.تكرار_الوثيقة = {كلمة: عدد_الوثائق_التي_تحتوي_عليها}

    دالة _رمّز(الذات, نص):
        # يقسم النص بالمسافات ويطبّع كل كلمة
        # يرجع قائمة الكلمات المطبّعة (يبقي الكلمات الفارغة خارجاً)

    دالة _أنشئ_الفهرس(الذات):
        # يملأ الفهرس_المعكوس وتكرار_الوثيقة

    دالة احفظ(الذات, مسار_الملف):
        # يحفظ الفهرس إلى JSON (الفهرس_المعكوس + metadata الوثائق)

    دالة __len__(الذات):
        ارجع طول(الذات.الوثائق)
```

The inverted index structure stored as JSON:
```json
{
  "وثائق": {"0": {"اسم": "الخوارزمي.txt", "طول": 312}, ...},
  "فهرس": {"الجبر": {"0": [5, 23, 87], "2": [14]}, ...},
  "تكرار_وثيقة": {"الجبر": 3, ...}
}
```

### `ranker.apy`

Class `مُرتِّب`:

```python
صنف مُرتِّب:
    دالة __init__(الذات, فهرس_البحث):
        الذات.الفهرس = فهرس_البحث

    دالة ابحث(الذات, استعلام, عدد_النتائج=5):
        # 1. يطبّع كلمات الاستعلام
        # 2. لكل كلمة في الاستعلام، يجمع وثائق المرشحة من الفهرس_المعكوس
        # 3. يحسب TF-IDF لكل وثيقة مرشحة
        # 4. يرجع قائمة من (معرف_الوثيقة, الدرجة, مقتطف) مرتبة تنازلياً
        # يرجع [] إذا لم توجد نتائج
```

**TF-IDF formula:**

For query term `t` in document `d`:
- `TF(t,d)` = count of `t` in `d` / total words in `d`
- `IDF(t)` = `log(N / (1 + DF(t)))` where N = total documents, DF = docs containing t
- Score for doc `d` = `sum(TF(t,d) × IDF(t))` for all query terms

**Snippet extraction:**

Find the position of the first query term match in the original (non-normalized) document text. Extract 120 characters around it. Mark matched terms with `【` and `】` brackets in the snippet (no color library needed — pure Unicode).

### `cli.apy`

Entry point. Two modes:

**Interactive mode** (no arguments):
```
محرك البحث العربي
══════════════════
الوثائق المفهرسة: ٦

أدخل استعلامك (أو "خروج" للإنهاء):
> الجبر والرياضيات

النتائج (٣ وثائق):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
١. الخوارزمي.txt  [الدرجة: ٠.٨٧]
   ...وضع الخوارزمي أسس 【الجبر】 في كتابه الشهير وأحدث ثورة في 【الرياضيات】...

٢. بيت_الحكمة.txt  [الدرجة: ٠.٤٢]
   ...ترجمت في بيت الحكمة أمهات الكتب في 【الرياضيات】 والفلسفة...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Single-query mode** (argument provided):
```bash
apython apps/search_engine/cli.apy "ابن سينا والطب"
```
Prints results then exits.

**Output formatting rules:**
- Numbers in output use Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩). Convert with:
  `''.join(chr(ord('٠') + int(d)) for d in str(n))`
- Scores rounded to 2 decimal places (also Arabic-Indic)
- Separator lines use `━` (U+2501)
- Header uses `═` (U+2550)

---

## Implementation constraints

- **Python version**: 3.11+
- **Dependencies**: stdlib only (`os`, `json`, `math`, `re`, `sys`)
- **All apython source files**: every identifier (variables, functions, classes,
  parameters) must be in Arabic. Comments in Arabic. The only English allowed is
  inside string literals for file paths/JSON keys that are technically required,
  and the stdlib module names in `استورد` statements.
- **Style**: run `python -m black .` on all Python files before committing.
  `.apy` files are not checked by Black — no formatter needed.
- **Encoding**: all `.apy` and `.txt` files UTF-8.
- **Error handling**: if the docs directory is empty or missing, print an Arabic
  error message and exit with code 1. If a query matches nothing, say so in
  Arabic.

---

## Test requirements (`tests/test_search_engine.py`)

All tests use the real sample documents in `apps/search_engine/docs/`.

1. `test_normalizer_strips_harakat`:
   - Input: `"الكِتَابُ"`
   - Expected: `"الكتاب"`

2. `test_normalizer_folds_hamza`:
   - Input: `"إذا"`
   - Expected: `"اذا"`

3. `test_normalizer_folds_ta_marbuta`:
   - Input: `"قيمة"`
   - Expected: `"قيمه"`

4. `test_index_loads_six_documents`:
   - Build index from `apps/search_engine/docs/`
   - `assert len(فهرس_instance) == 6`

5. `test_index_contains_expected_term`:
   - Build index
   - Assert normalized `"الجبر"` is in `الفهرس_المعكوس`

6. `test_search_returns_results`:
   - Query: `"الجبر"`
   - Assert result list is non-empty
   - Assert first result is `"الخوارزمي.txt"`

7. `test_search_ranking_order`:
   - Query: `"الطب"`
   - Assert `"ابن_سينا.txt"` ranks first

8. `test_search_no_results`:
   - Query: `"بيتزا برغر كولا"` (words guaranteed absent)
   - Assert result list is empty

9. `test_snippet_contains_brackets`:
   - Query any term known to be present
   - Assert `"【"` in the returned snippet

10. `test_arabic_indic_in_output` (subprocess test):
    - Run `apython apps/search_engine/cli.apy "الجبر"` via subprocess
    - Assert `"١"` (Arabic-Indic 1) in stdout

---

## Acceptance checklist

- [ ] All 6 sample documents created with genuine Arabic prose (~200–300 words each).
- [ ] `normalizer.apy` passes all normalizer tests.
- [ ] `indexer.apy` builds inverted index from docs directory.
- [ ] `ranker.apy` returns results ranked by TF-IDF score.
- [ ] `cli.apy` works in both interactive and single-query mode.
- [ ] Numbers in output are Arabic-Indic digits.
- [ ] All `.apy` source identifiers are Arabic words.
- [ ] All 10 tests pass: `pytest tests/test_search_engine.py`
- [ ] Full test suite still passes: `pytest` (no regressions).
- [ ] `python -m black .` passes.
- [ ] Committed and pushed. Delivery note written at
  `specs/0013-search-engine-v1.delivery.md`.
