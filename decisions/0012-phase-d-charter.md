# 0012 — Phase D charter: AI & Reach

**Status**: accepted  
**Date**: 2026-04-30  
**Deciders**: project author  

---

## Context

Phase C shipped all 20 library alias packets (C-001 through C-025), bumped the version to 0.4.0, and brought the test suite to 2,413 passing tests across 3 operating systems and 3 Python versions. The project now covers:

- **The full Python keyword set** (ar-v1 + ar-v2 dictionaries, 187 entries)
- **30+ library aliases** covering HTTP, ML, web frameworks, databases, async, office documents, browser automation, terminal UI, and CLI tools
- **Class-proxy system** for instance-level method translation
- **VS Code extension**, **Jupyter kernel**, **pytest plugin**, **ruff/black formatter support**
- **Web playground** (D-001, shipped at Phase D open)

Three forces shape what Phase D must solve:

1. **The zero-friction gap.** The playground (D-001) removes the installation barrier, but discovery remains low. Phase D must generate traffic through a live, shareable URL; a reverse translator that converts existing Python code; and AI SDK aliases that tap into the current wave of Arabic AI development.

2. **The AI moment.** Arabic developers are building with `anthropic`, `openai`, `langchain`, `transformers`, and `sentence-transformers` right now. If لغة الثعبان does not speak the language of AI, it misses the highest-growth segment of the Arabic developer community. Phase D must add full Arabic aliases for these libraries.

3. **The discoverability gap.** A language learner cannot start writing Arabic Python from scratch — they need to see what's possible, get step-by-step guidance, and have their existing Python code translated. A reverse translator (Python → لغة الثعبان) and an integrated tutorial close this gap.

**Theme**: "AI & Reach" — make the language effortless to discover, use, and share.

---

## Tier definitions

| Tier | Label | Criterion |
|---|---|---|
| **1** | Must Ship | Phase D is not complete without these; they drive the primary value proposition |
| **2** | Should Ship | Significantly raise quality or reach; targeted for Phase D but deferrable to D.1 patch |
| **3** | Future Vision | Require external dependencies, research, or community; explicitly deferred to Phase E or a dedicated sub-project |

---

## Tier 1 — Must Ship (D-001 to D-005)

### D-001 — Web Playground ✓

**Status**: **SHIPPED** (2026-04-30)

A self-contained static HTML page at `docs/playground.html`, deployed to GitHub Pages via `.github/workflows/pages.yml`. Bundles the full arabicpython transpiler (pretokenize + translate + ar-v2 dictionary) inline. Runs via Pyodide 0.27.0 — zero installation, zero backend. Features: 7 built-in examples, RTL code editor, output panel, Ctrl+Enter hotkey.

**Acceptance criteria** (all met):
- [ ] Opens in Chrome/Firefox/Safari without any local server
- [ ] Runs "مرحبا بالعالم" and displays output
- [ ] Handles SyntaxError gracefully (Arabic error text)
- [ ] GitHub Pages workflow deploys on push to `main` under `docs/`

---

### D-002 — AI SDK Arabic aliases

**Packet label**: D-002  
**Scope**: Arabic module aliases for `anthropic`, `openai`, `langchain-core`, `transformers` (HuggingFace), and `sentence-transformers`. Each gets a TOML file under `arabicpython/aliases/`, a test file under `tests/aliases/`, and a demo `.apy` file under `examples/`.

**Why this tier**: The single highest-leverage item after the playground. Arabic developers building AI applications are the fastest-growing segment. Aliasing `anthropic` as `كلود_عربي` and `openai` as `ذكاء_مفتوح` makes لغة الثعبان immediately relevant to this wave.

**Arabic module names**:

| Python package | Arabic module name | Rationale |
|---|---|---|
| `anthropic` | `كلود_عربي` | Brand + language marker |
| `openai` | `ذكاء_مفتوح` | MSA "open intelligence" |
| `langchain` / `langchain_core` | `سلسلة_لغه` | MSA "language chain" |
| `transformers` | `محولات` | MSA "transformers" |
| `sentence_transformers` | `محولات_جمل` | MSA "sentence transformers" |

**Key entries per alias** (examples):

`anthropic.toml`:
```
عميل = Anthropic (class)
رسالة = Message
انشئ = create (method on messages)
محادثه = MessageParam
نموذج = Model
خطا_مهله = APITimeoutError
```

`openai.toml`:
```
عميل = OpenAI (class)
اجلب_اجابه = chat.completions.create
نموذج_توليد = Completion
تضمين = Embedding
خطا_مفتاح = AuthenticationError
```

**pyproject.toml extra**:
```toml
[project.optional-dependencies]
ai = [
    "anthropic>=0.25",
    "openai>=1.30",
    "langchain-core>=0.2",
]
```

**Acceptance criteria**:
- Each TOML has `[meta]`, `[entries]`, `[attributes]` sections
- All keys round-trip through `normalize_identifier()` (caught by existing invariant test)
- Test file covers: module-level entries resolve correctly, `pytest.importorskip` guards
- Demo `.apy` file runs end-to-end if the library is installed
- Collision budget test still passes (no new collisions beyond budget)

---

#### Codex packet prompt — D-002

```
PACKET D-002 — Arabic aliases for AI SDKs (anthropic, openai, langchain-core, transformers, sentence-transformers)

## Goal
Create five Arabic alias modules for the major AI/LLM Python libraries, following
the established Phase C pattern exactly. Each alias consists of:
  1. arabicpython/aliases/<name>.toml
  2. tests/aliases/test_<name>.py
  3. examples/D02_<name>_demo.apy

## Pattern reference
Copy the structure of arabicpython/aliases/requests.toml (for the TOML)
and tests/aliases/test_requests.py (for the test). Look at those files first.

Also read: arabicpython/aliases/_finder.py, _loader.py, _proxy.py to understand
how proxy_classes, [entries], and [attributes] are consumed at runtime.

## Normalization rule (CRITICAL)
Every Arabic key in [entries] and [attributes] MUST equal
normalize_identifier(key) — i.e., no ة (use ه), no أ/إ/آ (use ا),
no ى (use ي), no shadda, no harakat.
The test test_keys_round_trip_through_normalize WILL catch violations.
Run: python -c "from arabicpython.normalize import normalize_identifier; print(normalize_identifier('خطأ'))"
to check any key before committing.

## TOML structure (required sections)

[meta]
python_module = "anthropic"   # exact importable name
arabic_name   = "كلود_عربي"  # must be a valid Python identifier
version       = "0.25"
proxy_classes = ["Anthropic"]  # list classes whose instances get auto-wrapped

[entries]
# Arabic key = "Python.dotted.path"  (use dots for nested: "errors.APITimeoutError")
كلود_عربي = "Anthropic"
...

[attributes]
# Arabic key = "python_method_name"
انشئ = "create"
...

## The five libraries

### 1. anthropic → كلود_عربي
File: arabicpython/aliases/anthropic.toml
Minimum 20 entries. Include:
  - Anthropic client class
  - messages.create, completions.create
  - Message, MessageParam, ContentBlock, TextBlock, Usage
  - All major exception classes (APITimeoutError, AuthenticationError,
    RateLimitError, APIConnectionError, APIStatusError, BadRequestError)
  - Stream / MessageStream if present
  - beta.tools if present

### 2. openai → ذكاء_مفتوح
File: arabicpython/aliases/openai.toml
Minimum 20 entries. Include:
  - OpenAI, AsyncOpenAI client classes
  - chat.completions.create, completions.create, embeddings.create
  - ChatCompletion, Completion, Embedding, Image, Model
  - All major exception classes

### 3. langchain_core → سلسلة_لغه
File: arabicpython/aliases/langchain_core.toml
Minimum 15 entries. Focus on:
  - BaseLanguageModel, BaseChatModel, BaseMessage
  - HumanMessage, AIMessage, SystemMessage
  - PromptTemplate, ChatPromptTemplate
  - BaseOutputParser, StrOutputParser
  - RunnableSequence

### 4. transformers → محولات
File: arabicpython/aliases/transformers.toml
Minimum 20 entries. Include:
  - AutoModel, AutoModelForCausalLM, AutoModelForSequenceClassification
  - AutoTokenizer, PreTrainedTokenizer
  - pipeline (function)
  - Trainer, TrainingArguments
  - BertModel, GPT2LMHeadModel (as entry points)
  - set_seed, logging

### 5. sentence_transformers → محولات_جمل
File: arabicpython/aliases/sentence_transformers.toml
Minimum 15 entries. Include:
  - SentenceTransformer (class, proxy_classes)
  - encode (method, via attributes)
  - util.cos_sim, util.semantic_search
  - CrossEncoder
  - InputExample

## Test file pattern
Each test file must:
  - Use pytest.importorskip("<python_module>")
  - Have a module-scoped fixture that creates a ModuleProxy via AliasFinder
  - TestCore: assert module-level entries resolve to the right Python objects
  - TestTomlMeta: assert [meta] parseable, arabic_name correct, entry count >= N

## Demo .apy file
Show the module alias in use (read-only operations only, no API calls).
Use pytest.importorskip pattern in a comment at top: "# requires: pip install anthropic"
Show: import alias, access class, access an exception class, show __name__/__module__.

## pyproject.toml
Add an [ai] optional-dependencies extra:
  ai = ["anthropic>=0.25", "openai>=1.30", "langchain-core>=0.2",
        "transformers>=4.40", "sentence-transformers>=3.0"]

Update [all] to include lughat-althuban[ai].

## Collision budget
After adding all five files, run:
  pytest tests/test_aliases_toml_invariants.py -v
The cross-file collision test has COLLISION_BUDGET = 70.
If your additions push it over 70, rename the colliding keys by adding
domain-specific suffixes (e.g., خطا_مهله_عميل instead of خطا_مهله).
Do NOT just bump the budget without renaming.

## Quality bar
- ruff check . passes
- black --check . passes
- pytest tests/aliases/test_anthropic.py tests/aliases/test_openai.py ... -v passes
  (with the relevant library installed; test files skip gracefully if not)
- pytest tests/test_aliases_toml_invariants.py passes
```

---

### D-003 — Reverse translator: Python → لغة الثعبان

**Packet label**: D-003  
**Scope**: A CLI tool and library function that takes a `.py` file or string and produces equivalent `.apy` source using Arabic keywords and, optionally, Arabic built-in names and exception names. Integrated into the `ثعبان` CLI as `ثعبان ترجمة-عكسية <file.py>`.

**Why this tier**: The biggest conversion barrier for an existing Python developer is the blank-page problem. If they can paste their Python script and get working لغة الثعبان back, they can immediately learn by reading. This is also the strongest single demo for social media ("look, I pasted my Python and got Arabic back in one command").

**Scope of translation**:
- Level 1 (must): Keywords (`if` → `اذا`, `for` → `لكل`, `def` → `دالة`, etc.)
- Level 2 (should): Built-in names (`print` → `اطبع`, `range` → `نطاق`, `len` → `طول`, etc.)
- Level 3 (optional flag): Exception names (`ValueError` → `خطا_قيمه`, etc.)
- Out of scope: Renaming user-defined variables/functions (too risky; just translate the keywords)

**CLI usage**:
```bash
ثعبان ترجمة-عكسية script.py           # writes to script.apy
ثعبان ترجمة-عكسية script.py --stdout  # prints to stdout
ثعبان ترجمة-عكسية script.py --level=2 # include built-ins (default level=2)
ثعبان ترجمة-عكسية script.py --level=3 # include exceptions too
```

**Implementation approach**: The `Dialect` object already has `reverse_names` and `reverse_attributes` maps (built in `dialect.py` — every `load_dialect()` call populates them). The reverse translator tokenizes the `.py` file with `tokenize`, walks NAME tokens, and replaces Python keywords/builtins with their Arabic canonical form using `reverse_names` / `reverse_attributes`.

**Acceptance criteria**:
- `ثعبان ترجمة-عكسية examples/hello.py` produces valid `.apy` that runs via `ثعبان تشغيل`
- Round-trip test: `translate(reverse_translate(python_src)) == python_src` for a set of 10 reference programs
- The playground page has a "ترجم كود Python" tab that accepts Python and shows Arabic output
- `-h` / `--help` prints Arabic usage text

---

#### Codex packet prompt — D-003

```
PACKET D-003 — Reverse translator: Python source → لغة الثعبان source

## Goal
Implement arabicpython/reverse.py (a new module) plus CLI integration.
The reverse translator takes a Python source string and returns an equivalent
.apy source string by replacing Python keywords and built-in names with their
Arabic canonical forms from the ar-v2 dictionary.

## Inputs you will need to read first
- arabicpython/dialect.py        — Dialect dataclass has reverse_names, reverse_attributes
- arabicpython/translate.py      — study the forward pipeline; reverse is the same in structure
- arabicpython/cli.py            — add the new subcommand here
- dictionaries/ar-v2.md         — source of truth for reverse mappings

## What to implement

### arabicpython/reverse.py

def reverse_translate(
    source: str,
    *,
    dialect: Dialect | None = None,
    dict_version: str | None = None,
    level: int = 2,
) -> str:
    """Translate Python source to لغة الثعبان source.

    Level 1: keywords only (if/for/def/class/...)
    Level 2: keywords + built-in names (print/range/len/...) [default]
    Level 3: level 2 + exception names (ValueError/KeyError/...)
    """

Algorithm:
1. Load dialect (same logic as translate.py).
2. Fast path: source.isascii() does NOT apply here — all Python source is ASCII
   but we are outputting Arabic, so skip the fast path entirely.
3. Tokenize the source with tokenize.tokenize.
4. Walk NAME tokens:
   - If the token is after '.', look up in dialect.reverse_attributes.
     On hit at level 2+, replace.
   - Otherwise, look up in dialect.reverse_names.
     On hit at level 1+, always replace keywords.
     On hit at level 2+, replace built-ins (category == "function" or "type").
     On hit at level 3, also replace exceptions (category == "exception").
5. Apply changes right-to-left (same as translate.py).
6. Return the result.

The dialect.categories map tells you the category of each normalized key.
Categories are: "keyword", "literal", "type", "function", "exception", "method".
Level 1 = replace "keyword" and "literal".
Level 2 = level 1 + "type" + "function".
Level 3 = level 2 + "exception".
Do NOT replace "method" — attribute names on user objects should be left alone
(the user's class methods are not standard library methods).

### CLI integration (arabicpython/cli.py)
Add subcommand: ثعبان ترجمة-عكسية
  - Positional argument: input file (path to .py)
  - --stdout: print to stdout instead of writing .apy file
  - --level: 1, 2, or 3 (default 2)
  - --dict: ar-v1 or ar-v2 (default ar-v2)
  - If no --stdout, write to same directory with .apy extension
  - Print a one-line summary: "ترجمة: <input> → <output> (N استبدال)"

### Tests (tests/test_reverse.py)
- test_keywords_only: reverse_translate("if x:\n    pass\n", level=1) contains "اذا"
- test_builtins: reverse_translate("print(len(x))\n", level=2) contains "اطبع" and "طول"
- test_round_trip: for each of 5 reference programs, translate(reverse_translate(src)) == src
  Reference programs: hello world, fibonacci, list comprehension, exception handling, class def
- test_exceptions_level3: reverse_translate("except ValueError:", level=3) contains "خطا_قيمه"
- test_preserves_user_names: user-defined function names and variable names are NOT translated
- test_cli: subprocess call to `python -m arabicpython.cli ترجمة-عكسية --stdout` works

### Quality bar
- ruff check . passes
- black --check . passes
- pytest tests/test_reverse.py -v passes
```

---

### D-004 — Arabic stdlib module aliases (20+ Python stdlib modules)

**Packet label**: D-004  
**Scope**: Arabic aliases for the Python standard library modules most commonly used by beginners and educators. Unlike Phase C's third-party library aliases, these cover `import` statements for stdlib modules and their top-level functions.

**Why this tier**: A learner writing their first Arabic Python program will quickly need `os`, `math`, `datetime`, `json`, `pathlib`, `random`, `re`, and `collections`. Without stdlib aliases, they are forced into a code-switch: `استورد math` works (they can import by English name), but calling `math.sqrt()` instead of `رياضيات.جذر()` breaks the immersion. Phase D must close this.

**Target stdlib modules** (minimum coverage, one TOML each):

| Python stdlib | Arabic alias | Priority |
|---|---|---|
| `math` | `رياضيات` | P1 |
| `os` | `نظام` | P1 |
| `os.path` | `مسار_نظام` | P1 |
| `pathlib` | `مسار` | P1 |
| `datetime` | `تاريخ_وقت` | P1 |
| `json` | `جيسون` | P1 |
| `random` | `عشوائي` | P1 |
| `re` | `تعابير` | P2 |
| `collections` | `مجموعات` | P2 |
| `itertools` | `ادوات_تكرار` | P2 |
| `functools` | `ادوات_دوال` | P2 |
| `string` | `نصوص` | P2 |
| `time` | `وقت` | P2 |
| `sys` | `نظام_بايثون` | P2 |
| `io` | `ادخال_اخراج` | P3 |
| `csv` | `ملف_csv` | P3 |
| `hashlib` | `تشفير` | P3 |
| `uuid` | `معرف_فريد` | P3 |
| `logging` | `تسجيل` | P3 |
| `threading` | `خيوط` | P3 |

**Special handling**: stdlib modules are already importable (no `pip install` needed), so `pytest.importorskip` is not required. Test files can import directly.

**Acceptance criteria**:
- `استورد رياضيات` works and `رياضيات.جذر(٩)` returns `3.0`
- `استورد تاريخ_وقت` works and `تاريخ_وقت.تاريخ.اليوم()` returns today's date
- All 20 TOML files pass the invariant tests
- A new `tests/aliases/stdlib/` subdirectory contains test files
- A new `examples/stdlib/` directory contains at least 5 demo `.apy` files

---

#### Codex packet prompt — D-004

```
PACKET D-004 — Arabic aliases for Python stdlib modules (math, os, pathlib, datetime, json, random, re, collections, itertools, functools + 10 more)

## Goal
Create Arabic alias TOML files for 20 Python standard library modules.
These follow the exact same pattern as third-party library aliases (Phase C)
but do NOT need pytest.importorskip since stdlib is always available.

## Pattern reference
Read arabicpython/aliases/requests.toml and tests/aliases/test_requests.py first.
Read arabicpython/aliases/_finder.py to understand how AliasFinder resolves modules.

## Key difference from Phase C aliases
stdlib modules don't need pip install, so:
  - No pytest.importorskip in tests
  - No pyproject.toml optional-dependency addition needed
  - Tests can import directly

## Normalization rule (CRITICAL — same as always)
Every key in [entries] and [attributes] MUST equal normalize_identifier(key).
No ة, أ/إ/آ, ى, shadda, harakat. Check with:
  python -c "from arabicpython.normalize import normalize_identifier; print(normalize_identifier('KEY'))"

## Module list and minimum entry counts

P1 — Must implement (≥15 entries each):

1. math → رياضيات
   entries: sqrt جذر, pi باي, e قاعده_لوغ, floor ارضيه, ceil سقف,
            sin جيب, cos جيب_تمام, tan ظل, log لوغاريتم, log2 لوغ_2,
            log10 لوغ_10, pow أس, factorial مضروب, gcd قاسم_مشترك,
            inf لانهايه, nan ليس_عددا, degrees درجات, radians راديان,
            hypot وتر, isnan يكون_ليس_عددا, isinf يكون_لانهايه

2. os → نظام
   entries: getcwd مسار_حالي, listdir اسرد_مجلد, mkdir انشئ_مجلد,
            makedirs انشئ_مجلدات, remove احذف_ملف, rmdir احذف_مجلد,
            rename اعد_تسميه, getenv متغير_بيئه, putenv عين_متغير,
            environ متغيرات_بيئه, sep فاصل_مسار, linesep فاصل_سطر,
            path مسار_نظام, walk تصفح_شجره, stat احصاء_ملف

3. pathlib → مسار
   entries: Path مسار_ملف (proxy_classes = ["Path", "PurePath", "PosixPath", "WindowsPath"])
   attributes on Path: exists يوجد, is_file يكون_ملف, is_dir يكون_مجلد,
            read_text اقرا_نص, write_text اكتب_نص, read_bytes اقرا_بايتات,
            write_bytes اكتب_بايتات, mkdir انشئ, unlink احذف, rename اعد_تسميه,
            glob ابحث_نمط, rglob ابحث_نمط_شامل, stat احصاء, parent الاب,
            name الاسم, stem الجذر, suffix اللاحقه, parts الاجزاء,
            absolute مطلق, resolve حل, joinpath الحق_مسار, open افتح

4. datetime → تاريخ_وقت
   entries: date تاريخ, time وقت, datetime تاريخ_كامل, timedelta فرق_زمني,
            timezone منطقه_زمنيه
   attributes on date: today اليوم, now الان, year سنه, month شهر, day يوم,
            strftime نسق_تاريخ, strptime حلل_تاريخ, isoformat نسق_iso,
            weekday يوم_اسبوع, replace استبدل

5. json → جيسون
   entries: loads حمل_نص, dumps اصدر_نص, load حمل_ملف, dump اصدر_ملف,
            JSONDecodeError خطا_json, JSONEncoder مشفر_json, JSONDecoder فك_مشفر_json

6. random → عشوائي
   entries: random عشوائي_عشري, randint عشوائي_صحيح, choice اختر,
            choices اختيارات, shuffle اخلط, sample عينه, uniform منتظم,
            seed بذره, randrange نطاق_عشوائي, gauss غاوسيان

P2 — Should implement (≥10 entries each):

7. re → تعابير
8. collections → مجموعات  (Counter عداد, deque طابور, defaultdict قاموس_افتراضي, OrderedDict قاموس_مرتب, namedtuple صف_مسمى)
9. itertools → ادوات_تكرار
10. functools → ادوات_دوال (reduce اختزل, partial جزئي, lru_cache ذاكره_تخزين, wraps يلف, cached_property خاصيه_محفوظه)
11. string → نصوص
12. time → وقت_نظام (avoid collision with datetime.time)
13. sys → نظام_بايثون
14. typing → تنميط

P3 — Should implement (≥8 entries each):
15. io → ادخال_اخراج
16. csv → ملف_csv
17. hashlib → تشفير
18. uuid → معرف_فريد
19. logging → تسجيل
20. threading → خيوط

## Test structure
Create tests/aliases/stdlib/ directory.
One test file per P1 module: test_math.py, test_os.py, test_pathlib.py, etc.
Each test:
  - Fixture creates ModuleProxy via AliasFinder
  - TestCore: assert key entries resolve to correct Python objects
  - TestAttributes: assert method-level attributes work (for proxy_classes modules)
  - TestTomlMeta: assert meta section correct

## Demo .apy files
Create examples/stdlib/ directory with at least 5 demos:
  D04_math_demo.apy — compute pi, golden ratio, triangle sides
  D04_pathlib_demo.apy — list files, read/write text
  D04_datetime_demo.apy — today's date, timedelta, formatting
  D04_json_demo.apy — loads/dumps roundtrip
  D04_random_demo.apy — random choice, shuffle, sample

## Collision budget
Run pytest tests/test_aliases_toml_invariants.py after all 20 TOMLs are added.
If collisions exceed 70, rename with _نظام or _رياضيات suffixes.
If needed, bump COLLISION_BUDGET to a new reviewed number and document why.

## Quality bar
- ruff check . passes
- black --check . passes
- pytest tests/aliases/stdlib/ -v passes
- pytest tests/test_aliases_toml_invariants.py passes
```

---

### D-005 — Full Arabic traceback localization

**Packet label**: D-005  
**Scope**: Extend `arabicpython/tracebacks.py` to translate the English text of every built-in Python exception message that appears in a traceback — not just the exception class name, but the descriptive message itself. Add a `--tracebacks=arabic` flag to the CLI and make it the default for `.apy` files.

**Why this tier**: A learner who gets `NameError: name 'x' is not defined` in Arabic context is forced to context-switch back to English to understand the error. The dictionary already translates exception class names (`NameError` → `خطا_اسم`); D-005 completes the work by translating the message text.

**Translation scope** (top 30 most common messages by frequency):

| English message pattern | Arabic translation |
|---|---|
| `name '{name}' is not defined` | `الاسم '{name}' غير معرَّف` |
| `{type} object is not iterable` | `الكائن من نوع {type} غير قابل للتكرار` |
| `'NoneType' object has no attribute '{attr}'` | `الكائن None لا يملك الصفة '{attr}'` |
| `list index out of range` | `الفهرس خارج نطاق القائمة` |
| `division by zero` | `القسمة على صفر` |
| `{type} object cannot be interpreted as an integer` | `لا يمكن تفسير {type} كعدد صحيح` |
| `{func}() takes {n} positional arguments but {m} were given` | `{func}() تأخذ {n} وسيطاً إلا أنها أُعطيت {m}` |
| `{func}() got an unexpected keyword argument '{arg}'` | `{func}() حصلت على وسيط غير متوقع: '{arg}'` |
| `{key}` (KeyError) | `المفتاح '{key}' غير موجود في القاموس` |
| `maximum recursion depth exceeded` | `تجاوزت الحد الأقصى للتكرار الذاتي` |
| `{module} has no attribute '{attr}'` | `الوحدة '{module}' لا تملك الصفة '{attr}'` |
| `expected {n} but got {m}` | `المتوقع {n} لكن تم الحصول على {m}` |
| `{type} and {type} cannot be concatenated` | `لا يمكن دمج {type} و {type}` |
| `unsupported operand type(s) for {op}` | `نوع غير مدعوم للعملية {op}` |
| `'str' object does not support item assignment` | `النصوص لا تقبل التعيين المباشر (غير قابلة للتعديل)` |
| `pop from empty list` | `انتزاع من قائمة فارغة` |
| `too many values to unpack (expected {n})` | `قيم أكثر مما يمكن فك ضمّها (المتوقع {n})` |

**Acceptance criteria**:
- `ثعبان تشغيل script.apy` shows Arabic error messages for all top-30 patterns
- `PYTHONTRACEBACK=arabic ثعبان تشغيل script.apy` is equivalent
- English tracebacks still available via `--tracebacks=english` flag
- Tests in `tests/test_tracebacks_arabic.py` verify 10+ message patterns

---

#### Codex packet prompt — D-005

```
PACKET D-005 — Arabic traceback message translation

## Goal
Extend arabicpython/tracebacks.py to translate the English text of built-in
Python exception messages, not just the class names.

## Read first
- arabicpython/tracebacks.py — current implementation
- arabicpython/cli.py        — where to add --tracebacks flag
- dictionaries/ar-v2.md     — already translates exception class names

## What to implement

### Translation table
Add a module-level dict _MSG_PATTERNS in tracebacks.py.
Each entry is (compiled_regex, arabic_template) where the template uses
\1, \2, etc. for captured groups.

Minimum 20 patterns covering the most common errors. Include all patterns
listed in the D-005 charter spec (NameError, TypeError, IndexError,
KeyError, ZeroDivisionError, RecursionError, AttributeError message texts).

Pattern matching strategy:
  1. Get exc_type name and str(exc_value) from the traceback
  2. For each (pattern, template) pair: try re.sub(pattern, template, str(exc_value))
  3. On match, display the Arabic form; fall back to English if no pattern matches

### tracebacks.py changes
Add: def translate_exception_message(exc_type: type, exc_value: Exception) -> str

Add: def format_arabic_traceback(exc_info, *, level="full") -> str
  - level="full": translate class name + message + frame locations
  - level="message": translate only the message, leave frame paths in English

### CLI changes (cli.py)
Add --tracebacks flag to all subcommands that run user code (run, repl):
  --tracebacks=arabic    (default for .apy files)
  --tracebacks=english   (always English)
  --tracebacks=mixed     (Arabic class name, English message)

### Tests (tests/test_tracebacks_arabic.py)
- test_name_error: raise NameError via translate(); check Arabic message
- test_type_error_not_iterable: int is not iterable → Arabic
- test_zero_division: ZeroDivisionError → Arabic
- test_index_error: list index out of range → Arabic
- test_attribute_none: None has no attribute → Arabic
- test_recursion_error: maximum recursion → Arabic
- test_key_error: key not found → Arabic
- test_fallback: unknown message pattern → returns original English (no crash)
- test_cli_flag: subprocess with --tracebacks=english shows English

## Quality bar
- ruff check . passes
- black --check . passes
- pytest tests/test_tracebacks_arabic.py -v passes
```

---

## Tier 2 — Should Ship (D-006 to D-011)

### D-006 — Integrated web tutorial

**Scope**: Add a `/tutorial` page (or tabbed section in `playground.html`) with 8 progressive lessons that teach لغة الثعبان from scratch. Each lesson has: a short explanation panel (Arabic text), a pre-filled code editor, and a "run" button. Lessons unlock sequentially. Progress is saved in `localStorage`.

**Lessons**:
1. أول برنامج — `اطبع`
2. المتغيرات والأنواع — `نص`, `عدد_صحيح`, `عدد_عشري`, `منطقي`
3. شروط التحكم — `اذا` / `والا` / `والا_اذا`
4. الحلقات — `لكل` و `طالما`
5. الدوال — `دالة` و `ارجع`
6. القوائم والقواميس
7. الأصناف والكائنات
8. معالجة الأخطاء

**Acceptance criteria**: Tutorial page loads standalone; each lesson runs correctly in Pyodide; progress persists across browser refresh.

---

#### Codex packet prompt — D-006

```
PACKET D-006 — Web tutorial page (docs/tutorial.html)

## Goal
Create docs/tutorial.html: a standalone, self-contained Arabic tutorial for
لغة الثعبان with 8 progressive lessons. Reuse the Pyodide + arabicpython
bundle from playground.html.

## Read first
- docs/playground.html — copy the Pyodide init logic verbatim
  (the embedded <script type="text/plain"> source file strategy)
- docs/ar/tutorial-ar.md or docs/tutorial-ar.md — content source

## Architecture
Single HTML file. Two panels: lesson sidebar (left) + lesson content (right).
Lesson content = explanation text (Arabic, RTL) + editable code area + run button + output.

Copy the full embedded Python bundle from playground.html:
  src-init, src-normalize, src-pretokenize, src-fstring311, src-dialect,
  src-translate, src-ar-v2-md
These are identical — do NOT diverge.

## 8 Lessons (content in Arabic)

Lesson 1: أول برنامج
  Explain: اطبع هي الدالة الأساسية للطباعة.
  Code: اطبع("مرحبا بالعالم!")
  Expected output: مرحبا بالعالم!

Lesson 2: المتغيرات والأنواع
  Explain: نص، عدد_صحيح، عدد_عشري، منطقي
  Code: اسم = "محمد"\nعمر = ٢٥\nطول_نص = طول(اسم)\nاطبع(ت"اسمي {اسم}، عمري {عمر}")

Lesson 3: شروط التحكم
  Explain: اذا / والا / والا_اذا
  Code: درجه = ٨٥\nاذا درجه >= ٩٠:\n    اطبع("ممتاز")\nوالا_اذا درجه >= ٧٠:\n    اطبع("جيد")\nوالا:\n    اطبع("يحتاج مراجعة")

Lesson 4: الحلقات
  Explain: لكل / طالما
  Code: lكل عدد في نطاق(١، ٦):\n    اطبع(عدد * عدد)

Lesson 5: الدوال
  Explain: دالة / ارجع
  Code: دالة مرحبا(اسم):\n    ارجع ت"مرحبا يا {اسم}!"\n\naطبع(مرحبا("فاطمة"))

Lesson 6: القوائم والقواميس
  Explain: قائمة، قاموس، العمليات الأساسية
  Code: list and dict operations with Arabic comma

Lesson 7: الأصناف
  Explain: صنف، __init__، دوال الصنف
  Code: class example with animal

Lesson 8: معالجة الأخطاء
  Explain: حاول / استثناء / أخيرا
  Code: try/except example

## localStorage progress
localStorage key: "lughat_tutorial_progress" = JSON array of completed lesson indices.
On load, highlight completed lessons and unlock the next one.
"أكملت هذا الدرس ✓" button marks lesson complete and unlocks next.

## Linking
In playground.html, add a "📖 البرنامج التعليمي" link in the header pointing to tutorial.html.
In tutorial.html, add a "🔗 الملعب" link pointing back to playground.html.

## Quality bar
- Opens from file:// in Chrome (no server needed)
- All 8 lessons run correctly
- Progress survives page refresh
```

---

### D-007 — Mobile-optimized playground (PWA)

**Scope**: Extend `docs/playground.html` to be a Progressive Web App: `manifest.json`, a service worker for offline caching of the Pyodide bundle, and a touch-friendly layout for phones. Add "اضغط للنسخ" (tap to copy) on output.

**Key challenges**: Pyodide is ~10 MB; the service worker must cache it after first load. The RTL code editor must work with iOS/Android soft keyboards.

**Acceptance criteria**:
- Lighthouse PWA score ≥ 70
- "Add to Home Screen" installs correctly on iOS and Android
- Works offline after first visit (Pyodide cached by service worker)
- Code editor usable on a phone screen

---

### D-008 — Arabic Jupyter kernel improvements

**Scope**: Enhance `arabicpython_kernel/` to support:
1. **Arabic cell magic**: `%%عربي` cell magic that runs the cell body through `translate()` before execution, for use in standard `.ipynb` notebooks without the `.apy` extension
2. **Arabic rich display**: When a variable's `__repr__` contains Arabic, display it RTL in the Jupyter output cell
3. **Keyword completion**: The kernel's `do_complete` returns Arabic keyword suggestions, not just English ones

**Acceptance criteria**:
- `%%عربي` magic works in JupyterLab
- Arabic repr displays RTL
- Tab-completion in a Jupyter cell suggests Arabic keywords after partial Arabic typing

---

### D-009 — Arabic `pip` wrapper improvements

**Scope**: Extend `arabicpython/pip_wrapper.py` to:
1. Accept Arabic package names: `ثعبان تثبيت طلبات` → `pip install requests` (using a registry map)
2. Show Arabic install output: intercept pip output and translate status messages
3. Add a `ثعبان مكتبات` command that lists installed alias packages with their Arabic names

**Registry map**: A new `arabicpython/aliases/registry.toml` that maps Arabic package names to PyPI names for all packages covered by alias TOMLs.

**Acceptance criteria**:
- `ثعبان تثبيت طلبات` installs `requests`
- `ثعبان مكتبات` lists `[طلبات] requests 2.31.0` etc.
- Unknown Arabic names fall through to PyPI with a helpful Arabic error

---

### D-010 — Example gallery page

**Scope**: `docs/gallery.html` — a grid of 20+ real-world `.apy` program examples. Each card shows: program title (Arabic), a short description, a syntax-highlighted code preview, and a "شغّل في الملعب" button that opens `playground.html?example=<id>` with the code pre-loaded.

**Programs to include**: One per major domain — web scraping, data analysis, file operations, API calls, game logic, sorting algorithms, math visualizations, text processing, OOP patterns, functional patterns, async patterns, exception patterns, CLI tools, unit tests, regex, date/time manipulation, JSON parsing, CSV processing, recursion, decorators.

**Acceptance criteria**: Gallery loads fast (no Pyodide on the gallery page itself); "شغّل في الملعب" links work; URL parameter correctly pre-loads code in playground.

---

### D-011 — `[ai]` optional-dependency extra (pyproject.toml)

**Scope**: After D-002 ships, add `lughat-althuban[ai]` as a published optional extra. Update the README with an "AI with Arabic" section showing a full Arabic `anthropic` usage example. Add a GitHub Actions workflow job that installs `.[ai]` and runs `pytest tests/aliases/test_anthropic.py` on CI.

**Acceptance criteria**: `pip install lughat-althuban[ai]` installs all AI SDK aliases; CI verifies the aliases on every push.

---

## Tier 3 — Future Vision (D-012 to D-017)

These items are explicitly deferred. No Codex prompt is written for them; they require community input, external dependencies, or research that is out of scope for a single-author project at this stage. They are documented here as a roadmap signal.

---

### D-012 — Multi-dialect Arabic support

**Concept**: Currently ar-v2 is Modern Standard Arabic (MSA / الفصحى). Speakers of Gulf, Levantine, Moroccan, or Egyptian dialects may have different intuitive translations for some keywords. For example:
- `if` → `لو` (Egyptian/colloquial) vs. `اذا` (MSA, current)
- `while` → `ما دام` (Levantine) vs. `طالما` (MSA, current)

A `ar-gulf`, `ar-levantine` dictionary variant could serve these communities. This requires linguistic consultants per dialect, community review, and a dialect-selection mechanism in the CLI (`# apython: dict=ar-gulf`).

**Blocking dependencies**: Community advisory board; native speaker review per dialect; governance ADR.

---

### D-013 — Arabic AI pair programmer (Claude in playground)

**Concept**: Add a chat panel to `playground.html` that accepts natural Arabic questions like "لماذا أحصل على خطأ في السطر ٣؟" (Why do I get an error on line 3?) and calls the Anthropic API with the code + error context. The response appears in Arabic.

**Blocking dependencies**: Anthropic API key (cannot embed in static HTML without a backend); requires a serverless function or Cloudflare Worker backend; privacy considerations for submitted code.

---

### D-014 — School curriculum pack

**Concept**: A structured curriculum for teaching Arabic Python in K-12 or university settings. Includes: 30 graded exercises with auto-graded test cases, a teacher's guide in Arabic, lesson plan templates, and a student progress tracker. Designed to align with Saudi/GCC CS education standards.

**Blocking dependencies**: Collaboration with an Arabic CS education organization; curriculum review by professional educators; translation of exercise sets.

---

### D-015 — Arabic package index (`apy.dev`)

**Concept**: A minimal PyPI-like registry at `apy.dev` (or a subdomain) that maps Arabic package names to PyPI packages and hosts Arabic-first documentation for each wrapped library. The `ثعبان تثبيت` command would check this registry first.

**Blocking dependencies**: Domain registration; Cloudflare Workers or similar serverless backend; community curation; legal/trademark review of Arabic transliterations of package names.

---

### D-016 — Static type checking in Arabic (mypy-ar)

**Concept**: A mypy plugin or wrapper that understands Arabic type annotations: `دالة مرحبا(اسم: نص) -> لاشيء:`. Since `نص` translates to `str` and `لاشيء` translates to `None`, the translated AST is already type-checkable. The plugin would run `translate()` before invoking mypy, then map mypy's English error messages back to Arabic.

**Blocking dependencies**: Understanding of mypy's plugin API; round-trip of position information through translate(); significant engineering effort.

---

### D-017 — Community and governance

**Concept**: As the project grows, single-author governance becomes a bottleneck. Phase E should establish:
- A **dictionary committee** (3–5 native Arabic speakers) that votes on new keyword proposals
- A **GitHub Discussions** forum for Arabic learners to ask questions in Arabic
- A **translation bounty** program for third-party library aliases contributed by the community
- A **`CONTRIBUTING-AR.md`** guide written entirely in Arabic

**Blocking dependencies**: Community interest; time investment in moderation; Arabic-language GitHub issues/PRs workflow.

---

## Phase D completion criterion

Phase D is considered complete when all Tier 1 items are shipped (D-001 through D-005) and the playground URL (GitHub Pages) is publicly accessible and correctly runs all 7 built-in examples.

Tier 2 items are targeted for Phase D but are individually deferrable. A "Phase D.1" patch release may ship Tier 2 items after the Tier 1 gate is met.

---

## Version plan

| Milestone | Version | Contents |
|---|---|---|
| D-001 shipped | 0.4.1 | Playground + Pages workflow |
| D-002 + D-003 | 0.5.0 | AI aliases + reverse translator |
| D-004 + D-005 | 0.5.1 | stdlib aliases + Arabic tracebacks |
| D-006 + D-010 | 0.5.2 | Tutorial + gallery |
| Full Tier 2 | 0.6.0 | All Tier 2 items |
| Phase D complete | 0.6.x | Tier 1 gate fully met |

---

## References

- ADR 0011 — Phase C charter (structural template for this document)
- ADR 0004 — Normalization policy (governs all Arabic identifier choices)
- ADR 0010 — Dictionary versioning (ar-v2 is the default for Phase D)
- Pyodide documentation — https://pyodide.org/en/stable/
- Anthropic Python SDK — https://github.com/anthropics/anthropic-sdk-python
