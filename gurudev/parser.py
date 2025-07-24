"""
gurudev/parser.py
Constrói a AST a partir dos tokens gerados pelo lexer.
Usa Lark para facilitar manutenção e expansão futura.
"""

from pathlib import Path
from lark import Lark, Transformer, v_args
from lark.indenter import Indenter

# Caminho para a gramática
GRAMMAR_PATH = Path(__file__).with_suffix('').parent / "grammar" / "gurudev.lark"

# -------------------------------------------------
# PARSER (Lark)
# -------------------------------------------------
parser = Lark.open(
    str(GRAMMAR_PATH),
    parser="lalr",
    transformer=None  # usaremos o transformer abaixo
)

# -------------------------------------------------
# TRANSFORMER (AST simplificada)
# -------------------------------------------------
@v_args(inline=True)
class GuruTransformer(Transformer):
    def blocks(self, *blocks):
        return list(blocks)

    def block(self, sobrescrita_opt, codigo, subescritas_opt):
        return {
            "type": "Block",
            "sobrescrita": sobrescrita_opt or [],
            "codigo": codigo,
            "subescritas": subescritas_opt or []
        }

    def sobrescrita_opt(self, *attrs):
        return [{"type": "Attr", "key": k, "value": v.strip('"')}
                for attr in attrs
                for k, v in [attr]]

    def codigo(self, code):
        return {"type": "Code", "language": "GuruDev", "source": str(code)}

    def subescritas_opt(self, *foreign_blocks):
        return foreign_blocks

    def foreign_block(self, lang_start, code, lang_end):
        lang = str(lang_start)[1:-1]  # retira ¿ ?
        return {
            "type": "ForeignBlock",
            "language": lang,
            "source": str(code)
        }

    def attr(self, key, val):
        return (str(key), str(val))

    def STRING(self, s):
        return s[1:-1]  # remove aspas

    def GURU_CODE(self, s):
        return s.strip()

    def FOREIGN_CODE(self, s):
        return s.strip()

# -------------------------------------------------
# FUNÇÃO PÚBLICA
# -------------------------------------------------
def parse_gurudev(code: str):
    """Retorna a AST simplificada de um código-fonte .guru"""
    tree = parser.parse(code)
    return GuruTransformer().transform(tree)
