# guru-dev-lang
GuruDev – a multi-paradigm, semantically-rich programming language that fuses grammatical cases, literate computing and 5-D symbolic coordinates for seamless cross-language interoperability and next-generation AI storytelling.
GuruDev is an experimental general-purpose language designed to transcend traditional paradigms.
Grammatical-case syntax (VOC, NOM, ACU, DAT…) brings classical rhetoric into code.
5-D GuruMatrix embeds ontology, hermeneutics and runtime context into every token.
Triplex blocks couple code, context and cross-language variants for literate programming.
Native interoperability lets you switch between Python, Rust, JS, SQL, R… at runtime.
Educational & AGI-ready – built for EdTech, cybersecurity and symbolic AI pipelines.
This MVP repo ships a lexer, parser, compiler (→ GuruByte), interpreter and Colab/Jupyter magic in under 2 k lines.
# GuruDev Language – MVP for Global Pre-Seed

A **multi-paradigm, interoperable programming language** inspired by grammatical cases, semiotics and literate computing.

> “Code that transcends paradigms, syntax that honours tradition.”

---

## 🚀 MVP Status

| Component        | Status | File |
|------------------|--------|------|
| Lexer            | ✅     | `gurudev/lexer.py` |
| Parser (Lark)    | ✅     | `gurudev/parser.py` |
| Compiler → `.gurub` | ✅ | `gurudev/compiler.py` |
| GuruDVM          | ✅     | `gurudev/vm.py` |
| Colab/Jupyter Magic | ✅ | `guru_magic.py` |
| CLI              | ✅     | `gurudev/__main__.py` |
| Examples         | ✅     | `examples/*.guru` |

---

## 📦 Quick Install

```bash
git clone https://github.com/Hubstry/guru-dev-mvp.git
cd guru-dev-mvp
pip install -e .
🎮 Usage
1. Compile .guru → .gurub
bash
Copy
guruc compile examples/01_hello_world.guru
2. Run .gurub
bash
Copy
gurudvm run examples/01_hello_world.gurub --verbose
3. Inside Jupyter / Colab
Python
Copy
%load_ext guru_magic
%%guru
[bloco]
  ¡codigo!
    VOC.console write("Hello GuruDev!");
  !/codigo!
[/bloco]
🗂 Repo Tree
Copy
guru-dev-mvp/
├── README.md
├── pyproject.toml
├── guru_magic.py
├── gurudev/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── compiler.py
│   ├── vm.py
│   └── __main__.py
├── grammar/
│   └── gurudev.lark
├── examples/
│   ├── 01_hello_world.guru
│   ├── 02_weighted_average.guru
│   └── 03_dynamic_security.guru
├── docs/
│   └── pitch_deck.pdf
└── .github/
    ├── workflows/ci.yml
    └── ISSUE_TEMPLATE.md
🤝 Contribute or Invest
Open issues, PRs, or reach out: contact@hubstry.ai
© 2025 Guilherme Machado & Hubstry
