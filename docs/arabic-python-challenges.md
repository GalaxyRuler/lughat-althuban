# تحديات العربية في بايثون
# Challenges of Arabic in Python

**A technical presentation on the gap between Arabic language and Python's tooling — and how to close it.**

---

## Slide 1 — Why This Matters

Arabic is spoken by **420 million people** as a first language and by over **1.8 billion** who use it liturgically. It is the official language of 26 countries. Yet when an Arabic-speaking student opens Python, they face a wall of English — not because Python cannot handle Arabic, but because Arabic support is fragmented, inconsistent, and poorly documented.

This presentation catalogs every known friction point between Arabic and Python, the specific libraries that address each one, and the concrete steps to resolve them.

---

## Slide 2 — The Arabic Script: What Makes It Different

Before addressing Python-specific problems, it is worth stating the properties of Arabic that create the most friction with software designed for Latin scripts:

| Property | Description |
|---|---|
| Direction | Right-to-left (RTL). Numerals and embedded Latin text flow left-to-right within an RTL paragraph — this bidirectionality is the single largest source of rendering bugs. |
| Letter forms | Each letter has 2–4 contextual shapes: isolated, initial, medial, final. Software that does not reshape Arabic renders it as a string of disconnected isolated letters. |
| Diacritics (تشكيل) | Harakat — fatha (َ), damma (ُ), kasra (ِ), sukun (ْ), shadda (ّ), tanwin — are separate combining Unicode codepoints layered over base letters. Most informal Arabic text omits them entirely. |
| Hamza variants | The hamza appears on six carrier forms: أ (U+0623), إ (U+0625), آ (U+0622), ؤ (U+0624), ئ (U+0626), ء (U+0621). The same phoneme, six different codepoints. |
| Ligatures | Certain letter combinations, especially Lam-Alef, are mandatory ligatures that must be rendered as a single glyph. |
| Morphology | Arabic is a root-pattern morphological system. The root ك-ت-ب (k-t-b) yields كَتَبَ (kataba: he wrote), كِتَاب (kitāb: book), مَكْتَبَة (maktaba: library), كَاتِب (kātib: writer). A single base word can generate hundreds of inflected forms through prefixes, suffixes, and vowel patterns. |
| Two numeral systems | Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩, U+0660–U+0669) are standard in most Arab countries. Western Arabic digits (0–9) are also widely used. Eastern Arabic-Indic digits (۰۱۲۳۴۵۶۷۸۹, U+06F0–U+06F9) are used in Persian/Urdu contexts. |
| Calendar | The Islamic Hijri calendar is a lunar calendar approximately 11 days shorter than the Gregorian year. Dates differ by ~622 years and cannot be converted with a simple offset. |

---

## Slide 3 — Challenge 1: Unicode Blocks and Encoding

### The Problem

Arabic Unicode spans **six separate blocks**, not one:

| Block | Range | Contents |
|---|---|---|
| Arabic | U+0600–U+06FF | Main block: base letters, diacritics, digits, punctuation |
| Arabic Supplement | U+0750–U+077F | Extended letters for non-MSA scripts (Maghrebi, etc.) |
| Arabic Extended-A | U+08A0–U+08FF | Additional letters for African Arabic scripts |
| Arabic Presentation Forms-A | U+FB50–U+FDFF | Positional letter forms and ligatures |
| Arabic Presentation Forms-B | U+FE70–U+FEFF | Additional positional forms |
| Arabic Mathematical Alphabetical Symbols | U+1EE00–U+1EEFF | Math symbols only |

Code written for `[\u0600-\u06FF]` misses five of six blocks. Windows historically defaulted to **Windows-1256 (CP1256)** for Arabic, not UTF-8 — reading legacy files without specifying encoding corrupts Arabic text silently.

### Translation of Key Terms

| English | Arabic |
|---|---|
| Encoding | ترميز |
| Unicode block | كتلة يونيكود |
| Code point | نقطة رمزية |
| UTF-8 | UTF-8 |
| Byte Order Mark (BOM) | علامة ترتيب البايت |

### Steps 1–5

**Step 1 — Always specify UTF-8 explicitly.**
Never rely on the default encoding. Every file open in Python must declare:
```python
with open("file.txt", encoding="utf-8") as f:
    text = f.read()
```
On Windows, `open()` defaults to CP1252 or CP1256 depending on locale. The `-X utf8` command-line flag (`python -X utf8 script.py`) forces UTF-8 globally in Python 3.7+.

**Step 2 — Add `# -*- coding: utf-8 -*-` to source files.**
Although UTF-8 is Python 3's default source encoding (PEP 3120), making it explicit prevents misidentification by editors and CI tools.

**Step 3 — Use `unicodedata.category()` to classify characters, not character ranges.**
```python
import unicodedata
def is_arabic_letter(ch):
    return unicodedata.bidirectional(ch) == 'AL'  # Arabic Letter bidi class

def is_arabic_diacritic(ch):
    return unicodedata.category(ch) == 'Mn' and '\u064B' <= ch <= '\u065F'
```

**Step 4 — Use the `regex` library (PyPI: `regex`, v2026.4.4) for proper Unicode property matching.**
```python
import regex
# Matches ALL Arabic script characters across all six blocks:
arabic_chars = regex.findall(r'\p{Script=Arabic}', text)
# Matches all Arabic diacritics (Mn category):
diacritics = regex.findall(r'\p{Mn}', text)
# Standard re would require: [\u064B-\u065F\u0610-\u061A\u06D6-\u06DC...]
```

**Step 5 — Detect and handle Windows-1256 legacy files.**
```python
def read_arabic_file(path):
    for encoding in ('utf-8-sig', 'utf-8', 'windows-1256', 'iso-8859-6'):
        try:
            with open(path, encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {path} with any known Arabic encoding")
```
`utf-8-sig` handles UTF-8 files that begin with a BOM (common from Windows Notepad).

---

## Slide 4 — Challenge 2: Bidirectional Text (BiDi)

### The Problem

Arabic and English coexist in the same text constantly: URLs, code snippets, brand names, technical terms, and numbers all appear inside Arabic prose. The Unicode Bidirectional Algorithm (UAX #9) governs which direction each character flows, but it is a *display-layer* algorithm. Python strings are stored in logical order (the order characters were typed), but terminals, word processors, browsers, and image renderers must convert to visual order. When the rendering engine is BiDi-unaware, Arabic text appears reversed, left-to-right, or scrambled.

The **Trojan Source attack** (CVE-2021-42574, disclosed November 2021, Boucher & Anderson, University of Cambridge) exploited invisible BiDi override characters embedded in source code comments and string literals. A reviewer sees one thing; the compiler executes another. Affected characters:

| Codepoint | Name | Effect |
|---|---|---|
| U+202A | Left-to-Right Embedding (LRE) | Forces LTR rendering in a bubble |
| U+202B | Right-to-Left Embedding (RLE) | Forces RTL rendering in a bubble |
| U+202C | Pop Directional Formatting (PDF) | Ends an embedding |
| U+202D | Left-to-Right Override (LRO) | Forces LTR, overriding character properties |
| U+202E | Right-to-Left Override (RLO) | Forces RTL, overriding character properties |
| U+2066–U+2069 | LRI / RLI / FSI / PDI | Isolate-based equivalents of the above |
| U+200E | Left-to-Right Mark (LRM) | Invisible LTR directional mark |
| U+200F | Right-to-Left Mark (RLM) | Invisible RTL directional mark |

Python 3.12 added `SyntaxWarning` for BiDi override characters in source files.

### Translation of Key Terms

| English | Arabic |
|---|---|
| Bidirectional | ثنائي الاتجاه |
| Right-to-left | من اليمين إلى اليسار |
| Logical order | الترتيب المنطقي |
| Visual order | الترتيب المرئي |
| Paragraph direction | اتجاه الفقرة |

### Steps 1–5

**Step 1 — Install python-bidi (v0.6.7) for display-layer BiDi resolution.**
```bash
pip install python-bidi
```
```python
from bidi.algorithm import get_display
visual_text = get_display("مرحبا Python 3.12 يا صديقي")
# Converts logical-order mixed Arabic/Latin to visual order for LTR renderers
```

**Step 2 — Install arabic-reshaper (v3.0.0) for correct letter forms before BiDi reordering.**
```bash
pip install arabic-reshaper
```
```python
import arabic_reshaper
from bidi.algorithm import get_display

text = "مرحبا بالعالم"
reshaped = arabic_reshaper.reshape(text)   # correct contextual letter forms
display  = get_display(reshaped)           # correct RTL visual order
# Now safe to pass to matplotlib, PIL, reportlab, fpdf2
```

**Step 3 — For terminal output, use Right-to-Left Mark (U+200F) to set paragraph direction.**
Modern terminals (Windows Terminal, iTerm2, GNOME Terminal) handle Arabic natively. Add `\u200f` (RLM) at the start of any mixed-direction line:
```python
RLM = '\u200f'
print(f"{RLM}الدالة: {function_name}")
```

**Step 4 — Reject BiDi control characters from untrusted source files.**
```python
BIDI_CONTROLS = frozenset('\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069')
def check_source_for_bidi(source: str, filename: str) -> None:
    for i, ch in enumerate(source):
        if ch in BIDI_CONTROLS:
            raise SyntaxError(
                f"BiDi control character U+{ord(ch):04X} in {filename} at position {i}. "
                "See CVE-2021-42574 (Trojan Source)."
            )
```

**Step 5 — Use `unicodedata.bidirectional()` to detect and classify characters rather than guessing.**
```python
import unicodedata
def text_base_direction(text: str) -> str:
    """Returns 'RTL', 'LTR', or 'NEUTRAL' based on first strong directional character."""
    for ch in text:
        bidi = unicodedata.bidirectional(ch)
        if bidi in ('AL', 'R', 'RLE', 'RLO'):   # Arabic Letter, Right-to-Left
            return 'RTL'
        if bidi in ('L', 'LRE', 'LRO'):          # Left-to-Left
            return 'LTR'
    return 'NEUTRAL'
```

---

## Slide 5 — Challenge 3: Text Normalization

### The Problem

The same Arabic word can be encoded dozens of ways. The word for "إذا" (if) can appear as:
- `إذا` — U+0625 U+0630 U+0627 (Alef with hamza below)
- `اذا` — U+0627 U+0630 U+0627 (plain Alef, no hamza)
- `إِذَا` — with full diacritics

A naïve string comparison between these three forms returns False despite them being the same word. Database lookups, search engines, and dictionary lookups fail silently if normalization is not applied uniformly.

Unicode itself has four normalization forms (NFC, NFD, NFKC, NFKD) that handle composed vs. decomposed characters, but they do not handle Arabic-specific semantic equivalences like hamza folding.

### Libraries

- **`unicodedata`** (stdlib): `normalize('NFKC', text)` — canonical decomposition then composition; covers Alef variants that are precomposed
- **`camel-tools` v1.5.7** (PyPI: `camel-tools`): `normalize_alef_ar()`, `normalize_alef_maksura_ar()`, `normalize_teh_marbuta_ar()`, `normalize_unicode()`
- **`PyArabic` v0.6.15** (PyPI: `PyArabic`): `strip_tashkeel()`, `strip_tatweel()`, `normalize_hamza()`, `normalize_lamalef()`, `normalize_spellerrors()`, `normalize_searchtext()`

### Translation of Key Terms

| English | Arabic |
|---|---|
| Normalization | تطبيع |
| Diacritics / Harakat | التشكيل / الحركات |
| Hamza | الهمزة |
| Alef | الألف |
| Tatweel / Kashida | التطويل / الكشيدة |
| Teh Marbuta | التاء المربوطة |
| Alef Maksura | الألف المقصورة |

### Steps 1–5

**Step 1 — Apply NFKC normalization as the baseline for all Arabic text.**
```python
import unicodedata
text = unicodedata.normalize('NFKC', raw_text)
```
NFKC decomposes compatibility characters (e.g., Lam-Alef ligatures in Presentation Forms) then recomposes. It is the correct form for any text processing pipeline.

**Step 2 — Strip harakat (diacritics) when comparing or indexing words.**
```python
# Using PyArabic:
from pyarabic import normalize as arab_normalize
stripped = arab_normalize.strip_tashkeel(text)   # removes all 8 harakat categories
stripped = arab_normalize.strip_tatweel(stripped) # removes U+0640

# Using camel-tools:
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.charsets import AR_DIAC_CHARSET
stripped = ''.join(ch for ch in text if ch not in AR_DIAC_CHARSET)
```

**Step 3 — Fold hamza variants for search and lookup.**
The six hamza-bearing Alef forms (U+0621, U+0622, U+0623, U+0624, U+0625, U+0626) must collapse to a canonical form before any dictionary or database lookup:
```python
from camel_tools.utils.normalize import normalize_alef_ar, normalize_alef_maksura_ar, normalize_teh_marbuta_ar

def normalize_for_search(text: str) -> str:
    text = unicodedata.normalize('NFKC', text)
    text = normalize_alef_ar(text)           # أإآٱ → ا
    text = normalize_alef_maksura_ar(text)   # ى → ي
    text = normalize_teh_marbuta_ar(text)    # ة → ه
    return text
```

**Step 4 — Build a normalization pipeline that is idempotent and composable.**
```python
from pyarabic import normalize as arab_norm
import unicodedata

def arabic_normalize_pipeline(text: str, *, strip_diacritics=True, fold_hamza=True) -> str:
    text = unicodedata.normalize('NFKC', text)
    text = arab_norm.strip_tatweel(text)
    if strip_diacritics:
        text = arab_norm.strip_tashkeel(text)
    if fold_hamza:
        text = arab_norm.normalize_hamza(text)
        text = arab_norm.normalize_spellerrors(text)  # ة→ه, ى→ي
    return text

# Idempotent: normalize(normalize(x)) == normalize(x)
assert arabic_normalize_pipeline(arabic_normalize_pipeline("إذا")) == arabic_normalize_pipeline("إذا")
```

**Step 5 — Store normalized forms alongside original forms in databases.**
Never discard the original. Store both:
```python
import sqlite3
db = sqlite3.connect(':memory:')
db.execute('''CREATE TABLE words (
    original TEXT,
    normalized TEXT,
    PRIMARY KEY (normalized)
)''')
word = "إِذَا"
db.execute("INSERT OR IGNORE INTO words VALUES (?, ?)",
           (word, arabic_normalize_pipeline(word)))
# Search by normalized form, display original form
```

---

## Slide 6 — Challenge 4: Python Identifier Support

### The Problem

Python has supported Unicode identifiers since PEP 3131 (Python 3.0). The rules follow Unicode TR#31:
- **ID_Start**: categories Lu, Ll, Lt, Lm, Lo, Nl, plus `_`
- **ID_Continue**: ID_Start + categories Mn, Mc, Nd, Pc

Arabic letters (category `Lo`) are valid ID_Start. Arabic diacritics (category `Mn`) are valid ID_Continue. So `مُحَمَّد` is a theoretically valid Python identifier.

**However**: Python 3.11's `tokenize` module generates `ERRORTOKEN` for certain Arabic combining marks (specifically shadda U+0651 and damma U+064F) in identifier positions, even though `str.isidentifier()` returns True for them. Python 3.12 fixed this via the PEP 701 tokenizer rewrite — but introduced new column-offset bugs for non-ASCII content (CPython issue #112943). The practical rule for Python 3.11 compatibility: **do not use harakat (U+064B–U+065F) in identifiers**. The tatweel (U+0640) works on all versions.

Additionally: Python's `compile()` applies NFKC normalization to identifiers (PEP 3131 §Normalization). Two identifiers that are NFKC-equivalent refer to the same variable — which is generally correct for Arabic but can surprise developers working with Alef variants.

### Translation of Key Terms

| English | Arabic |
|---|---|
| Identifier | معرّف |
| Keyword | كلمة مفتاحية |
| Token | رمز معجمي |
| Combining mark | علامة تشكيلية |
| Normalization (identifier) | تطبيع المعرّف |

### Steps 1–5

**Step 1 — Test identifier validity before using it in source.**
```python
def is_safe_arabic_identifier(name: str) -> bool:
    """Returns True if name is valid across Python 3.11, 3.12, and 3.13."""
    if not name.isidentifier():
        return False
    # Exclude harakat: U+064B–U+065F (fail on Python 3.11 tokenize)
    harakat = set(chr(cp) for cp in range(0x064B, 0x0660))
    harakat.add('\u0670')  # superscript alef
    return not any(ch in harakat for ch in name)
```

**Step 2 — Strip harakat from identifiers before writing .apy / .py source files.**
```python
HARAKAT = frozenset(chr(cp) for cp in range(0x064B, 0x0660)) | {'\u0670'}
TATWEEL  = '\u0640'

def to_safe_identifier(name: str) -> str:
    """Remove harakat; keep tatweel (it is safe on all Python versions)."""
    return ''.join(ch for ch in name if ch not in HARAKAT)
```

**Step 3 — Be aware of NFKC normalization collisions.**
```python
import unicodedata
a = "أسد"   # Alef with hamza above (U+0623)
b = "اسد"   # Plain alef (U+0627)
# These are DIFFERENT identifiers; Python does NOT normalize hamza for identifiers
# (NFKC preserves hamza differences). But camel-tools normalize_alef_ar() maps both to اسد.
# Do not use camel-tools normalization on Python identifiers — use Python's own NFKC only.
print(unicodedata.normalize('NFKC', a) == unicodedata.normalize('NFKC', b))  # False
```

**Step 4 — Build a translation dictionary that maps normalized forms for lookup.**
If you are building a transpiler or Arabic-keyword Python dialect, normalize identifiers at lookup time, not at storage time:
```python
def normalize_identifier_key(name: str) -> str:
    """Canonical key for dictionary lookup: NFKC + strip harakat + fold alef + fold alef-maksura + fold teh-marbuta."""
    import unicodedata
    name = unicodedata.normalize('NFKC', name)
    name = ''.join(ch for ch in name if ch not in HARAKAT and ch != TATWEEL)
    # Fold hamza variants
    ALEF_VARIANTS = str.maketrans({'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا'})
    name = name.translate(ALEF_VARIANTS)
    # Fold alef-maksura and teh-marbuta only at word-final position
    if name.endswith('ى'):
        name = name[:-1] + 'ي'
    if name.endswith('ة'):
        name = name[:-1] + 'ه'
    return name
```

**Step 5 — Set `PYTHONIOENCODING=utf-8` in deployment environments.**
Python's stdout/stderr on Windows defaults to CP1252, which cannot encode Arabic identifiers in error messages. Set:
```bash
set PYTHONIOENCODING=utf-8        # Windows CMD
export PYTHONIOENCODING=utf-8     # Linux/macOS
```
Or in code: `sys.stdout.reconfigure(encoding='utf-8')`.

---

## Slide 7 — Challenge 5: Tokenization (NLP)

### The Problem

Arabic has no spaces between words in classical text (spaces are modern). More critically, Arabic **clitics** — prefixes and suffixes that attach to words — make tokenization non-trivial:

- وَالكِتَابُ = و (and) + ال (the) + كتاب (book) + ُ (nominative marker)
- كَتَبْتُهَا = كتب (wrote) + ت (1st person) + ها (it, fem.)

A whitespace tokenizer produces one token where the correct analysis produces four. This breaks every downstream NLP task: POS tagging, NER, parsing, search indexing.

### Libraries

| Library | PyPI | Key Arabic Tokenization Feature |
|---|---|---|
| CAMeL Tools | `camel-tools` v1.5.7 | `MorphAnalyzer` with full clitic segmentation for MSA and Egyptian Arabic |
| Farasa | `farasapy` v0.1.1 | `FarasaSegmenter` — rule-based + statistical segmenter, fastest for large-scale |
| Stanza | `stanza` | Neural tokenizer with MWT (multi-word token) expansion for clitics |
| NLTK | `nltk` | `ISRIStemmer` for stemming; `stopwords.words('arabic')` for 168 Arabic stopwords |
| regex | `regex` v2026.4.4 | `\p{Arabic}+` for script-aware tokenization without explicit ranges |

### Translation of Key Terms

| English | Arabic |
|---|---|
| Tokenization | التجزئة / تقسيم النص |
| Token | وحدة نصية |
| Clitic | الكليتيك (الضمائر المتصلة والحروف المتصلة) |
| Stemming | التجذير |
| Lemmatization | الترميز المعجمي / إرجاع الكلمة لجذرها |
| Stop words | الكلمات الوقفية |

### Steps 1–5

**Step 1 — Install Stanza and download the Arabic model for neural tokenization.**
```bash
pip install stanza
python -c "import stanza; stanza.download('ar')"
```
```python
import stanza
nlp = stanza.Pipeline('ar', processors='tokenize,mwt')
doc = nlp("والكتاب جميل")
for sentence in doc.sentences:
    for token in sentence.tokens:
        print(token.text, [word.text for word in token.words])
# والكتاب → ['و', 'ال', 'كتاب']  (MWT expansion)
```

**Step 2 — Use CAMeL Tools MorphAnalyzer for MSA clitic segmentation.**
```bash
pip install camel-tools
camel_data -i morphology-db-msa-r13
```
```python
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

db = MorphologyDB.builtin_db(flags='gid')
analyzer = Analyzer(db)
analyses = analyzer.analyze('والكتاب')
for a in analyses[:3]:
    print(a['diac'], a['pos'], a['prc1'], a['enc0'])
```

**Step 3 — For large-scale fast segmentation, use Farasa.**
```bash
pip install farasapy
# Requires Java 1.7+ on the system PATH
```
```python
from farasa.segmenter import FarasaSegmenter
segmenter = FarasaSegmenter(interactive=True)   # keep Java process alive
result = segmenter.segment("والكتاب")
print(result)  # "و+ ال+ كتاب"
segmenter.terminate()
```

**Step 4 — Build a simple regex tokenizer for Arabic-specific use cases without NLP overhead.**
```python
import regex

ARABIC_WORD  = r'\p{Arabic}+'
LATIN_WORD   = r'[A-Za-z]+'
NUMBER       = r'[\d٠-٩]+'
PUNCTUATION  = r'[،؛؟\.\!\,\:\;\?\-]'
TOKEN_PATTERN = regex.compile(f'(?:{ARABIC_WORD}|{LATIN_WORD}|{NUMBER}|{PUNCTUATION})')

def tokenize_arabic(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text)

print(tokenize_arabic("أطلقت مشروع لغة الثعبان في 2026!"))
# ['أطلقت', 'مشروع', 'لغة', 'الثعبان', 'في', '2026', '!']
```

**Step 5 — Remove NLTK Arabic stopwords before indexing.**
```python
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
arabic_stops = set(stopwords.words('arabic'))
# 168 words: في, من, إلى, على, أن, كان, لا, ما, هذا, ...

def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in arabic_stops]
```

---

## Slide 8 — Challenge 6: Morphological Analysis

### The Problem

Arabic morphology is the deepest challenge. The root ك-ت-ب generates:
كَتَبَ، يَكْتُبُ، كِتَابَة، مَكَاتِب، كَاتِب، مَكْتُوب، اِكْتَتَبَ، اِسْتَكْتَبَ — and hundreds more forms. A search for "كتابة" must also return documents containing "الكتابة", "كتاباتهم", "المكتوب", etc. This requires morphological analysis, not just stemming.

### Libraries

| Library | PyPI | Capability |
|---|---|---|
| CAMeL Tools | `camel-tools` v1.5.7 | Full morphological analysis (lemma, root, POS, gender, number, case, state, person, aspect, voice, mood, all affixes) |
| Farasa | `farasapy` v0.1.1 | POS tagging, lemmatization, NER; faster than CAMeL Tools |
| MADAMIRA | Not on PyPI (Java jar) | Research-grade: full morphological disambiguation for MSA; requires license |
| Stanza | `stanza` | UPOS + morphological features via UD framework |
| PyArabic | `PyArabic` v0.6.15 | Root extraction, letter classification, moon/sun letters |

### Translation of Key Terms

| English | Arabic |
|---|---|
| Morphological analysis | التحليل الصرفي |
| Root | الجذر |
| Pattern (وزن) | الوزن / الميزان الصرفي |
| Lemma | اللمة / الصورة القاموسية |
| Part of speech | الجزء من الكلام |
| Inflection | الصرف / التصريف |
| Diacritization | التشكيل الآلي |
| Named entity recognition | التعرف على الكيانات المسماة |

### Steps 1–5

**Step 1 — Use CAMeL Tools MorphDisambiguator for context-aware analysis.**
```python
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.disambig.mle import MLEDisambiguator

db = MorphologyDB.builtin_db(flags='gid')
analyzer = Analyzer(db)
mle = MLEDisambiguator.pretrained('calima-msa-r13')

sentence = ['كتب', 'الطالب', 'رسالته']
disambiguated = mle.disambiguate(sentence)
for word, analysis in zip(sentence, disambiguated):
    top = analysis.analyses[0].analysis
    print(f"{word}: lemma={top['lex']}, pos={top['pos']}, root={top.get('root','?')}")
```

**Step 2 — Use Farasa POS tagger for production-scale tagging.**
```python
from farasa.pos import FarasaPOSTagger
pos = FarasaPOSTagger(interactive=True)
tags = pos.tag("كتب الطالب رسالته")
print(tags)  # "كتب/VBD الطالب/NN رسالته/NN+POSS"
pos.terminate()
```

**Step 3 — Use Farasa diacritizer to restore harakat (for TTS or formal documents).**
```python
from farasa.diacritizer import FarasaDiacritizer
diac = FarasaDiacritizer(interactive=True)
result = diac.diacritize("كتب الطالب")
print(result)  # "كَتَبَ الطَّالِبُ"
diac.terminate()
```

**Step 4 — Use PyArabic for root extraction without Java dependencies.**
```python
from pyarabic.root import RootExtractor
extractor = RootExtractor()
# Note: rule-based, lower accuracy than CAMeL Tools or Farasa
roots = extractor.extract("مكتوب")
print(roots)  # ['كتب']
```

**Step 5 — Build an Arabic search index using lemma forms, not surface forms.**
```python
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

db  = MorphologyDB.builtin_db(flags='gid')
ana = Analyzer(db)

def get_lemmas(word: str) -> set[str]:
    analyses = ana.analyze(word)
    return {a['lex'] for a in analyses if 'lex' in a}

# Index all lemma forms; search query also converted to lemmas
def index_document(text: str) -> dict[str, list[int]]:
    index = {}
    for pos, word in enumerate(text.split()):
        for lemma in get_lemmas(word):
            index.setdefault(lemma, []).append(pos)
    return index
```

---

## Slide 9 — Challenge 7: Numeral Systems

### The Problem

Three digit systems coexist in Arabic software:
- **Western Arabic**: 0 1 2 3 4 5 6 7 8 9 (U+0030–U+0039) — used in most tech contexts
- **Arabic-Indic**: ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ (U+0660–U+0669) — standard in Saudi Arabia, Egypt, Gulf
- **Eastern Arabic-Indic**: ۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹ (U+06F0–U+06F9) — Persian, Urdu, Pashto

Python's `int()`, `float()`, and arithmetic operators do NOT accept Arabic-Indic digits directly:
```python
int("٣")   # ValueError: invalid literal for int() with base 10: '٣'
```
`str.maketrans()` is the canonical solution. Python's `pretokenize` phase in any Arabic-keyword extension must convert digits before passing to the tokenizer.

### Translation of Key Terms

| English | Arabic |
|---|---|
| Digit | رقم |
| Arabic-Indic numerals | الأرقام العربية الهندية |
| Number system | نظام الترقيم |
| Decimal point | الفاصلة العشرية |

### Steps 1–5

**Step 1 — Convert Arabic-Indic to Western Arabic before any arithmetic.**
```python
ARABIC_INDIC_TABLE = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
EASTERN_ARABIC_TABLE = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')

def to_western_digits(text: str) -> str:
    return text.translate(ARABIC_INDIC_TABLE).translate(EASTERN_ARABIC_TABLE)

print(int(to_western_digits("١٩٨٤")))  # 1984
```

**Step 2 — Convert Western Arabic to Arabic-Indic for display.**
```python
TO_ARABIC_INDIC = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')

def to_arabic_indic(text: str) -> str:
    return text.translate(TO_ARABIC_INDIC)

print(to_arabic_indic("2026-04-22"))  # ٢٠٢٦-٠٤-٢٢
```

**Step 3 — Handle mixed-digit strings defensively.**
A string like "١2٣" (mixing systems) is malformed and should be rejected:
```python
import regex
ARABIC_INDIC_RE  = regex.compile(r'^[٠-٩]+$')
EASTERN_ARABIC_RE = regex.compile(r'^[۰-۹]+$')
WESTERN_RE       = regex.compile(r'^[0-9]+$')

def parse_arabic_number(text: str) -> int:
    if WESTERN_RE.match(text):
        return int(text)
    if ARABIC_INDIC_RE.match(text):
        return int(text.translate(ARABIC_INDIC_TABLE))
    if EASTERN_ARABIC_RE.match(text):
        return int(text.translate(EASTERN_ARABIC_TABLE))
    raise ValueError(f"Mixed or unrecognized digit system: {text!r}")
```

**Step 4 — Use `locale` for locale-aware number formatting.**
```python
import locale
locale.setlocale(locale.LC_NUMERIC, 'ar_SA.UTF-8')  # Linux/macOS
formatted = locale.format_string("%.2f", 3.14159)
print(formatted)  # "3٫14" (Arabic decimal separator U+066B in some locales)
```

**Step 5 — Use Arabic-Indic digits in user-facing output consistently.**
Build a formatting utility:
```python
def arabic_format_number(n: int | float, *, decimal_places: int = 0) -> str:
    if decimal_places:
        formatted = f"{n:.{decimal_places}f}"
    else:
        formatted = str(int(n))
    return formatted.translate(TO_ARABIC_INDIC)

print(arabic_format_number(1984))      # ١٩٨٤
print(arabic_format_number(3.14, decimal_places=2))  # ٣.١٤
```

---

## Slide 10 — Challenge 8: Sorting and Collation

### The Problem

Python's default `sorted()` sorts strings by Unicode code point value. For Arabic:
- Arabic letters start at U+0627 (Alef) — after all ASCII and Latin characters (U+0041–U+007A)
- The alphabetical order of Arabic letters (أبجد) does not match Unicode code point order
- Alef variants (أ U+0623, إ U+0625, آ U+0622) sort differently from plain Alef (ا U+0627) by code point but should be equivalent for alphabetical ordering
- Diacritics affect code point comparison but should be secondary or irrelevant for alphabetical sorting

Python's `locale.strcoll()` provides OS-dependent Arabic sorting but is not thread-safe and requires the Arabic locale to be installed on the system.

### Libraries

- **PyICU v2.16.2** (PyPI: `pyicu`): wraps ICU 77 (March 2025); implements Unicode Collation Algorithm (UCA, Unicode Technical Standard #10) with CLDR Arabic locale tailoring
- **`locale`** (stdlib): OS-dependent; not thread-safe; requires Arabic locale installed

### Translation of Key Terms

| English | Arabic |
|---|---|
| Collation / Sorting | الترتيب / الفرز |
| Alphabetical order | الترتيب الأبجدي |
| Sort key | مفتاح الترتيب |
| Unicode Collation Algorithm | خوارزمية الترتيب يونيكود |

### Steps 1–5

**Step 1 — Install PyICU.**
```bash
# Linux (Ubuntu):
sudo apt-get install libicu-dev
pip install pyicu

# macOS (Homebrew):
brew install icu4c
pip install pyicu

# Windows: use the pre-built wheel from Christoph Gohlke's site or conda-forge
```

**Step 2 — Create an Arabic-locale collator and use it for sorting.**
```python
import icu
ar_collator = icu.Collator.createInstance(icu.Locale('ar'))
words = ['زبد', 'أسد', 'إبل', 'بدء', 'آكل', 'ارض']
sorted_arabic = sorted(words, key=ar_collator.getSortKey)
print(sorted_arabic)
# Correct Arabic alphabetical order: أ/إ/آ (all Alef variants together), then ب, then ز, ...
```

**Step 3 — Control collation strength for different use cases.**
```python
import icu

# Primary strength: ignore diacritics and case (for search)
search_collator = icu.RuleBasedCollator(
    icu.Collator.createInstance(icu.Locale('ar')).getRules()
)
search_collator.setStrength(icu.Collator.PRIMARY)

# Secondary strength: distinguish diacritics but not case (for dictionary)
dict_collator = icu.Collator.createInstance(icu.Locale('ar'))
dict_collator.setStrength(icu.Collator.SECONDARY)

# Tertiary strength: full discrimination (for formal alphabetical lists)
formal_collator = icu.Collator.createInstance(icu.Locale('ar'))
formal_collator.setStrength(icu.Collator.TERTIARY)
```

**Step 4 — Use `locale.strcoll()` as a fallback when PyICU is not available.**
```python
import locale
import functools

try:
    import icu
    ar_collator = icu.Collator.createInstance(icu.Locale('ar'))
    sort_key = ar_collator.getSortKey
except ImportError:
    locale.setlocale(locale.LC_COLLATE, 'ar_SA.UTF-8')
    sort_key = locale.strxfrm  # WARNING: not thread-safe

words = ['زبد', 'أسد', 'بدء']
print(sorted(words, key=sort_key))
```

**Step 5 — Sort Arabic directory listings or file names correctly.**
```python
import os
import icu

ar_collator = icu.Collator.createInstance(icu.Locale('ar'))

def list_arabic_files(directory: str) -> list[str]:
    files = os.listdir(directory)
    return sorted(files, key=ar_collator.getSortKey)
```

---

## Slide 11 — Challenge 9: Date and Calendar Systems

### The Problem

The Islamic (Hijri) calendar is a **purely lunar calendar** of 12 months of 29 or 30 days each, totaling 354 or 355 days per year — approximately 11 days shorter than the Gregorian year. There is no simple offset formula. The conversion requires a lookup table or astronomical calculation. Furthermore, **two versions** of the Hijri calendar coexist:

1. **Tabular/Arithmetical**: an algorithmic calendar used in historical and legal contexts; leap years follow a fixed 30-year cycle
2. **Umm al-Qura**: the official calendar of Saudi Arabia, based on astronomical calculations of moon visibility; can differ from the tabular calendar by 1–2 days

Python's standard `datetime` module has no Hijri calendar support.

### Libraries

| Library | PyPI | Version | Calendar Type | Range |
|---|---|---|---|---|
| hijridate | `hijridate` | 2.6.0 (Jan 2026) | Umm al-Qura | 1343–1500 AH |
| convertdate | `convertdate` | 2.4.1 (Feb 2026) | Tabular | Full Hijri range |
| ummalqura | `ummalqura` | 2.0.1 (2017, unmaintained) | Umm al-Qura | Limited |

### Translation of Key Terms

| English | Arabic |
|---|---|
| Hijri calendar | التقويم الهجري |
| Gregorian calendar | التقويم الميلادي |
| Lunar month | الشهر القمري |
| Umm al-Qura | أم القرى |
| Tabular calendar | التقويم الحسابي |

### Steps 1–5

**Step 1 — Install hijridate (the maintained replacement for the deprecated hijri-converter).**
```bash
pip install hijridate
```
```python
from hijridate import Hijri, Gregorian

# Gregorian to Hijri:
today = Gregorian(2026, 4, 22)
hijri = today.to_hijri()
print(hijri)                         # Hijri(1447, 10, 24)
print(hijri.month_name('ar'))        # "شوال"

# Hijri to Gregorian:
h = Hijri(1447, 9, 1)               # 1st of Ramadan 1447
g = h.to_gregorian()
print(g)                             # Gregorian(2026, 3, 20)
```

**Step 2 — Display dates in full Arabic with correct month names.**
```python
from hijridate import Hijri
from datetime import date

HIJRI_MONTHS_AR = [
    'محرم', 'صفر', 'ربيع الأول', 'ربيع الثاني',
    'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان',
    'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
]
WEEKDAYS_AR = ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']

def format_hijri_date(gregorian_date: date) -> str:
    from hijridate import Gregorian
    h = Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day).to_hijri()
    day_name = WEEKDAYS_AR[gregorian_date.weekday()]
    month_name = HIJRI_MONTHS_AR[h.month - 1]
    return f"{day_name}، {h.day} {month_name} {h.year} هـ"

print(format_hijri_date(date(2026, 4, 22)))  # الأربعاء، ٢٤ شوال ١٤٤٧ هـ
```

**Step 3 — Use convertdate for tabular Hijri (non-Saudi contexts).**
```python
from convertdate import islamic
from datetime import date

today = date.today()
hijri_year, hijri_month, hijri_day = islamic.from_gregorian(
    today.year, today.month, today.day
)
# Note: tabular result may differ by 1-2 days from Umm al-Qura
```

**Step 4 — Handle the two-calendar ambiguity in data input.**
```python
import re
from hijridate import Hijri

HIJRI_PATTERN = re.compile(r'(\d{1,4})[/\-](\d{1,2})[/\-](\d{1,2})\s*هـ?$')

def parse_arabic_date(date_str: str) -> 'Gregorian':
    m = HIJRI_PATTERN.match(date_str.strip())
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return Hijri(y, mo, d).to_gregorian()
    raise ValueError(f"Cannot parse date: {date_str!r}")
```

**Step 5 — Compute prayer times relative to the Hijri calendar for Ramadan detection.**
```python
from hijridate import Gregorian
from datetime import date

def is_ramadan(d: date = None) -> bool:
    if d is None:
        d = date.today()
    h = Gregorian(d.year, d.month, d.day).to_hijri()
    return h.month == 9  # Ramadan is the 9th Hijri month
```

---

## Slide 12 — Challenge 10: Natural Language Processing at Scale

### The Problem

Most mature NLP libraries — spaCy, NLTK, Gensim, AllenNLP — were built primarily for English, with Arabic added as an afterthought or through community extensions. Arabic-specific challenges that general NLP libraries do not handle correctly:

1. **No word boundaries**: unlike Chinese (no spaces) but unlike English (spaces are sufficient), Arabic uses spaces but clitics attach to words without spaces
2. **High OOV rate**: Arabic's morphological richness means any fixed vocabulary misses many legal inflected forms
3. **Dialect diversity**: MSA (Modern Standard Arabic) differs significantly from Egyptian, Gulf, Levantine, Maghrebi, and Sudanese dialects — a model trained on MSA often fails on dialects
4. **Script ambiguity**: the same spelling can refer to completely different words depending on context and diacritics (e.g., كتب = he wrote / books / offices)

### Libraries and Models

**Transformer models on Hugging Face:**

| Model ID | Architecture | Parameters | Training Data | Best For |
|---|---|---|---|---|
| `aubmindlab/bert-base-arabertv02` | BERT-Base | 136M | 8.6B words (MSA + Wikipedia + news) | Classification, NER, QA |
| `aubmindlab/bert-large-arabertv02` | BERT-Large | 371M | 8.6B words | Same, higher accuracy |
| `aubmindlab/bert-base-arabertv02-twitter` | BERT-Base | 136M | 8.6B + 60M tweets | Social media, dialects |
| `CAMeL-Lab/bert-base-arabic-camelbert-msa` | BERT-Base | 110M | MSA only | Formal Arabic tasks |
| `CAMeL-Lab/bert-base-arabic-camelbert-ca` | BERT-Base | 110M | Classical Arabic | Quranic, literary |
| `CAMeL-Lab/bert-base-arabic-camelbert-da` | BERT-Base | 110M | Dialectal Arabic | Social media, dialects |
| `CAMeL-Lab/bert-base-arabic-camelbert-mix` | BERT-Base | 110M | MSA + CA + DA | General purpose |
| `CAMeL-Lab/bert-base-arabic-camelbert-mix-ner` | BERT-Base (fine-tuned) | 110M | — | NER (persons, locations, orgs) |
| `aubmindlab/aragpt2-base` | GPT-2 | 135M | 8.6B words | Text generation |
| `aubmindlab/aragpt2-mega` | GPT-2 | 1.46B | 8.6B words | Large-scale text generation |
| `aubmindlab/araelectra-base-discriminator` | ELECTRA | 135M | 8.6B words | Language understanding |

### Translation of Key Terms

| English | Arabic |
|---|---|
| Natural language processing | معالجة اللغة الطبيعية |
| Named entity recognition | التعرف على الكيانات المسماة |
| Sentiment analysis | تحليل المشاعر |
| Question answering | الإجابة على الأسئلة |
| Dialect | اللهجة |
| Out-of-vocabulary | خارج المفردات |

### Steps 1–5

**Step 1 — Use AraBERT for Arabic text classification.**
```bash
pip install transformers torch
```
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained('aubmindlab/bert-base-arabertv02')
model = AutoModelForSequenceClassification.from_pretrained(
    'aubmindlab/bert-base-arabertv02',
    num_labels=2
)
inputs = tokenizer("هذا المشروع رائع", return_tensors='pt')
outputs = model(**inputs)
```

**Step 2 — Use CAMeL Tools NER for entity extraction.**
```python
from camel_tools.ner import NERecognizer

ner = NERecognizer.pretrained()
tokens = ['زار', 'محمد', 'الرياض', 'في', 'أبريل']
entities = ner.predict_sentence(tokens)
for token, entity in zip(tokens, entities):
    print(f"{token}: {entity}")
# محمد: B-PERS, الرياض: B-LOC
```

**Step 3 — Use CAMeL Tools dialect identifier for preprocessing branching.**
```python
from camel_tools.dialectid import DialectIdentifier

did = DialectIdentifier.pretrained()
result = did.predict("شو بتحكي؟")  # Levantine
print(result.top)  # 'Levantine' or 'LEV'
# Route to dialect-specific model or transliterate to MSA first
```

**Step 4 — Use AraGPT2 for Arabic text generation.**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('aubmindlab/aragpt2-base')
model     = AutoModelForCausalLM.from_pretrained('aubmindlab/aragpt2-base')

prompt = "البرمجة بالعربية تعني"
input_ids = tokenizer.encode(prompt, return_tensors='pt')
output = model.generate(input_ids, max_length=100, do_sample=True, top_k=50)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

**Step 5 — Use Stanza for dependency parsing (Arabic treebank-trained).**
```python
import stanza

nlp = stanza.Pipeline('ar', processors='tokenize,mwt,pos,lemma,depparse')
doc = nlp("كتب الطالب رسالة جميلة")
for sentence in doc.sentences:
    for word in sentence.words:
        print(f"{word.text:15s} pos={word.upos:6s} head={sentence.words[word.head-1].text if word.head > 0 else 'ROOT'} dep={word.deprel}")
```

---

## Slide 13 — Challenge 11: Terminal and Display Rendering

### The Problem

Arabic text in terminals, log files, and graphical outputs has three distinct problems:
1. **Direction**: terminals must be configured for RTL or mixed-direction content
2. **Letter forms**: letters must be reshaped to their contextual forms (initial/medial/final/isolated)
3. **Ligatures**: Lam-Alef and other mandatory ligatures must be collapsed

Modern terminal emulators (Windows Terminal ≥1.0, iTerm2, GNOME Terminal, Alacritty) handle Arabic natively when the font supports it. However, Python libraries that render to **images** (matplotlib, PIL/Pillow), **PDFs** (reportlab, fpdf2, weasyprint), or **HTML with text rendering** all require explicit reshaping.

### Libraries

- **`arabic-reshaper` v3.0.0**: reshapes letters to contextual forms
- **`python-bidi` v0.6.7**: reorders to visual (display) order
- **Font requirements**: a font with full Arabic coverage — Amiri, Cairo, Noto Naskh Arabic, Scheherazade New, or IBM Plex Arabic

### Steps 1–5

**Step 1 — Set up the standard reshaping pipeline for image/PDF output.**
```bash
pip install arabic-reshaper python-bidi matplotlib
```
```python
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Use an Arabic-capable font (download Amiri or Noto Naskh Arabic)
font_path = "/usr/share/fonts/truetype/amiri/Amiri-Regular.ttf"  # Linux
arabic_font = fm.FontProperties(fname=font_path)

fig, ax = plt.subplots()
text = "لغة الثعبان — بايثون بالعربية"
display_text = get_display(arabic_reshaper.reshape(text))
ax.text(0.5, 0.5, display_text, fontproperties=arabic_font,
        ha='center', va='center', fontsize=18)
plt.savefig("arabic_plot.png", bbox_inches='tight')
```

**Step 2 — Configure arabic-reshaper for the specific font's supported ligatures.**
```python
import arabic_reshaper

# Auto-configure based on font's GSUB table
config = arabic_reshaper.config_for_true_type_font('/path/to/font.ttf')
reshaper = arabic_reshaper.ArabicReshaper(configuration=config)
reshaped = reshaper.reshape("لغة الثعبان")
```

**Step 3 — Use RTL marks for terminal output to enforce paragraph direction.**
```python
RLM = '\u200f'  # Right-to-Left Mark

def print_arabic(text: str) -> None:
    """Print Arabic text with RTL paragraph direction hint."""
    print(f"{RLM}{text}")

print_arabic("مرحبا يا عالم")
```

**Step 4 — Generate Arabic PDFs with reportlab.**
```bash
pip install reportlab arabic-reshaper python-bidi
```
```python
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

pdfmetrics.registerFont(TTFont('Amiri', '/path/to/Amiri-Regular.ttf'))

c = canvas.Canvas("arabic_doc.pdf")
c.setFont('Amiri', 14)

text = "هذا مستند عربي مكتوب بالبايثون"
shaped = get_display(arabic_reshaper.reshape(text))
# reportlab: x=500 with right-aligned text for RTL
c.drawRightString(500, 750, shaped)
c.save()
```

**Step 5 — Handle mixed Arabic/Latin in terminal output with explicit directional marks.**
```python
LRM = '\u200e'  # Left-to-Right Mark
RLM = '\u200f'  # Right-to-Left Mark

def format_mixed(arabic_label: str, value: str) -> str:
    """Format: Arabic label [RTL], then colon, then value [could be LTR number/path]."""
    return f"{RLM}{arabic_label}: {LRM}{value}"

print(format_mixed("الإصدار", "3.12.0"))
print(format_mixed("المسار", "/usr/local/bin/ثعبان"))
```

---

## Slide 14 — Challenge 12: Regular Expressions

### The Problem

Python's `re` module has two problems with Arabic:

1. **No Unicode property escapes**: `\p{Arabic}` does not work in `re`. You must enumerate code point ranges manually, and you will miss blocks.
2. **`re.UNICODE` flag behavior**: while `\w` with UNICODE matches Arabic letters, `\b` (word boundary) does not work reliably for Arabic because Arabic does not use spaces to delimit all morphological units.

### Libraries

- **`regex` v2026.4.4** (PyPI: `regex`): drop-in `re` replacement with full Unicode 17.0.0 property support

### Steps 1–5

**Step 1 — Replace `re` with `regex` for any Arabic text processing.**
```bash
pip install regex
```
```python
import regex  # drop-in replacement for re

# Match all Arabic words across all 6 Unicode blocks:
arabic_words = regex.findall(r'\p{Script=Arabic}+', text)

# Match Arabic letters only (not punctuation or digits from Arabic block):
arabic_letters = regex.findall(r'\p{Lo&&\p{Script=Arabic}}+', text)

# Match Arabic diacritics (tashkeel):
diacritics = regex.findall(r'\p{Mn&&\p{Script=Arabic}}', text)
```

**Step 2 — Use Unicode property intersections for precise character classes.**
```python
import regex

# Arabic letters excluding hamza (for search normalization):
AR_LETTER_NO_HAMZA = regex.compile(r'[\p{Arabic}&&\p{Lo}&&[^ءأإآؤئ]]')

# Arabic punctuation:
AR_PUNCT = regex.compile(r'[\u060C\u061B\u061F\u0640]')  # ،؛؟ and tatweel

# Arabic numerals (all three systems):
AR_NUMERALS = regex.compile(r'[\p{Nd&&\p{Arabic}}۰-۹0-9]')
```

**Step 3 — Implement Arabic-aware sentence splitting.**
```python
import regex

# Arabic sentence terminators: period (.), question mark (؟), exclamation (!),
# Arabic question mark (U+061F), Arabic semicolon (U+061B)
SENTENCE_END = regex.compile(r'(?<=[.؟!؟؛\u061F\u061B])\s+')

def split_arabic_sentences(text: str) -> list[str]:
    return SENTENCE_END.split(text.strip())
```

**Step 4 — Build a robust Arabic word tokenizer with regex.**
```python
import regex

TOKEN = regex.compile(
    r'(?:'
    r'\p{Script=Arabic}+'       # Arabic word (all scripts/blocks)
    r'|[A-Za-z]+'               # Latin word
    r'|[\d٠-٩۰-۹]+'            # Any digit system
    r'|[^\s\w]'                 # Single punctuation
    r')',
    regex.UNICODE
)

def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text)
```

**Step 5 — Use named groups for Arabic entity extraction.**
```python
import regex

# Match Arabic names (simplified pattern for demonstration)
NAME_PATTERN = regex.compile(
    r'(?P<prefix>(?:محمد|عبد|أبو|أم|بنت|بن)\s+)?'
    r'(?P<name>\p{Script=Arabic}{2,})'
    r'(?:\s+(?P<surname>\p{Script=Arabic}{2,}))?'
)

for m in NAME_PATTERN.finditer("تحدث محمد بن سلمان في الاجتماع"):
    print(m.groupdict())
```

---

## Slide 15 — Challenge 13: The Documentation Gap

### The Problem

This is arguably the most impactful challenge. The Python documentation — tutorial, library reference, language reference — is English-first. While translation projects exist (python.org provides 19 languages), the **Arabic translation is incomplete and unmaintained**. As of 2026:

- Python official docs: partial Arabic translation at docs.python.org/ar — far behind current versions
- PyPI package documentation: almost entirely English
- Stack Overflow Arabic content: minimal for Python-specific questions
- Educational resources in Arabic: fragmented, often outdated

A student who only reads Arabic has almost no path to learning Python in their language.

### What Exists

| Resource | URL | Status |
|---|---|---|
| Python docs (Arabic) | docs.python.org/ar | Partial, unmaintained |
| Arabic Python community (Facebook) | — | Active but informal |
| لغة الثعبان | github.com/GalaxyRuler/lughat-althuban | Active |

### Steps 1–5

**Step 1 — Contribute to the official Python Arabic translation on Transifex.**
The Python documentation is coordinated at `python.org/dev/peps` and translated via Transifex (translate.python.org). Arabic translators are needed for all three of: the tutorial, the library reference, and the language reference.

**Step 2 — Write Arabic docstrings in your own libraries.**
Python supports any Unicode in docstrings. There is no technical barrier:
```python
def normalize_arabic(text: str) -> str:
    """
    تُطبّع النص العربي بإزالة الحركات وطيّ صور الهمزة.

    المعاملات:
        text (str): النص العربي المُدخَل.

    القيم المُرجَعة:
        str: النص بعد التطبيع.

    مثال:
        >>> normalize_arabic("إِذَا")
        'اذا'
    """
```

**Step 3 — Use Arabic variable names and comments in educational code.**
The entire premise of لغة الثعبان — that Python can be written with Arabic keywords, identifiers, and comments — demonstrates that the language itself is not the barrier. Educational materials can use Arabic-identifier Python to teach programming concepts without requiring English:
```python
# حساب مساحة الدائرة
import math as رياضيات

def مساحة_دائرة(نصف_القطر: float) -> float:
    """تُحسب مساحة الدائرة من نصف قطرها."""
    return رياضيات.pi * نصف_القطر ** 2
```

**Step 4 — Build Arabic error messages for your libraries.**
```python
ARABIC_ERRORS = {
    'file_not_found': "الملف '{path}' غير موجود.",
    'invalid_encoding': "ترميز الملف '{path}' غير صالح. استخدم UTF-8.",
    'permission_denied': "لا يوجد إذن للوصول إلى '{path}'.",
    'empty_input': "المدخل فارغ. يُرجى إدخال نص عربي.",
}

def arabic_error(key: str, **kwargs) -> str:
    return ARABIC_ERRORS[key].format(**kwargs)

raise ValueError(arabic_error('file_not_found', path='ملف.apy'))
```

**Step 5 — Publish Arabic-language tutorials and examples as part of your package.**
Structure your package with an `examples/ar/` directory containing `.apy` or `.py` files with Arabic comments. Add a bilingual README where Arabic comes first.

---

## Slide 16 — Full Library Reference

| Challenge | Library | PyPI Name | Version | Key Function / Class |
|---|---|---|---|---|
| Unicode normalization | unicodedata | stdlib | — | `normalize('NFKC', text)`, `category()`, `bidirectional()` |
| Arabic normalization | camel-tools | `camel-tools` | 1.5.7 | `normalize_alef_ar()`, `normalize_unicode()` |
| Arabic text tools | PyArabic | `PyArabic` | 0.6.15 | `strip_tashkeel()`, `normalize_hamza()`, `normalize_lamalef()` |
| BiDi rendering | python-bidi | `python-bidi` | 0.6.7 | `bidi.algorithm.get_display()` |
| Letter reshaping | arabic-reshaper | `arabic-reshaper` | 3.0.0 | `ArabicReshaper.reshape()` |
| Full Arabic NLP | CAMeL Tools | `camel-tools` | 1.5.7 | `MorphAnalyzer`, `MorphDisambiguator`, `NERecognizer`, `DialectIdentifier` |
| Fast NLP (Java) | Farasa | `farasapy` | 0.1.1 | `FarasaSegmenter`, `FarasaPOSTagger`, `FarasaDiacritizer` |
| Neural NLP | Stanza | `stanza` | latest | `Pipeline('ar')`, MWT expansion, depparse |
| BERT (MSA+news) | AraBERT | `transformers` | — | `aubmindlab/bert-base-arabertv02` |
| BERT (dialectal) | CAMeLBERT | `transformers` | — | `CAMeL-Lab/bert-base-arabic-camelbert-mix` |
| BERT (Twitter) | AraBERT Twitter | `transformers` | — | `aubmindlab/bert-base-arabertv02-twitter` |
| Text generation | AraGPT2 | `transformers` | — | `aubmindlab/aragpt2-base` (135M) to `aragpt2-mega` (1.46B) |
| Discrimination | AraELECTRA | `transformers` | — | `aubmindlab/araelectra-base-discriminator` |
| Hijri calendar | hijridate | `hijridate` | 2.6.0 | `Hijri().to_gregorian()`, `Gregorian().to_hijri()` |
| Multi-calendar | convertdate | `convertdate` | 2.4.1 | `islamic.from_gregorian()` |
| Arabic collation | PyICU | `pyicu` | 2.16.2 | `Collator.createInstance(Locale('ar')).getSortKey()` |
| Unicode regex | regex | `regex` | 2026.4.4 | `\p{Script=Arabic}`, `\p{Mn}`, `\p{Lo}` |
| Stop words | NLTK | `nltk` | latest | `stopwords.words('arabic')` (168 words) |
| Stemming | NLTK | `nltk` | latest | `ISRIStemmer().stem(word)` |

---

## Slide 17 — The Minimum Viable Arabic Python Stack

For a project that processes Arabic text correctly from end to end, the minimum set of dependencies is:

```
arabic-reshaper==3.0.0
camel-tools==1.5.7
hijridate==2.6.0
pyicu==2.16.2
python-bidi==0.6.7
PyArabic==0.6.15
regex==2026.4.4
```

Install:
```bash
pip install arabic-reshaper camel-tools hijridate pyicu python-bidi PyArabic regex
```

This covers: encoding safety, normalization, reshaping, BiDi, collation, calendar conversion, Unicode property regex, and morphological analysis.

---

## Slide 18 — Summary: The Gap and the Path Forward

Arabic is not an afterthought in Unicode — it was a first-class consideration from the beginning. The gap is not in Python's core language (PEP 3131 covers Arabic identifiers; `tokenize` covers Arabic source files well in 3.12+). The gap is in:

1. **Documentation**: the official Python docs have almost no Arabic translation
2. **Tooling defaults**: `open()` does not default to UTF-8 on Windows; `re` does not support Unicode property escapes; `sorted()` does not know Arabic collation; `datetime` does not know the Hijri calendar
3. **NLP depth**: most production-grade Arabic NLP requires Java (Farasa) or heavyweight dependencies (CAMeL Tools with Rust); there is no pure-Python equivalent of spaCy's Arabic pipeline
4. **Terminal support**: the standard pipeline (reshape → get_display) is not automatic for plotting or PDF libraries
5. **Education**: there are almost no Arabic-language Python tutorials, books, or courses at the depth that exists in English, French, or Spanish

Projects like **لغة الثعبان** are one step in closing this gap — by demonstrating that Python programs can be written in Arabic, by providing a CLI that Arabic speakers can invoke without typing a single Latin character, and by building in Arabic the very tools (prayer time calculators, search engines) that Arabic-speaking users would recognise as practically useful.

The libraries are there. The Unicode standard supports it. The path forward is execution.

---

*Prepared for the لغة الثعبان project — github.com/GalaxyRuler/lughat-althuban*
