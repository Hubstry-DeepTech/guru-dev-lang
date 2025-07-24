"""
gurudev/lexer.py
Tokenizador PLY para a linguagem GuruDev.
Reconhece blocos tríplices, sub-escritas multilíngue, atributos 5-D,
casos gramaticais, tipos multimodais e literais.
"""

import re
from enum import Enum
from typing import List, Tuple

class TokenType(Enum):
    # Estruturas de bloco
    BLOCO_START = "BLOCO_START"
    BLOCO_END = "BLOCO_END"
    SOBRESCRITA_START = "SOBRESCRITA_START"
    SOBRESCRITA_END = "SOBRESCRITA_END"
    SUBESCRITAS_START = "SUBESCRITAS_START"
    SUBESCRITAS_END = "SUBESCRITAS_END"
    CODIGO_START = "CODIGO_START"
    CODIGO_END = "CODIGO_END"

    # Linguagens de sub-escrita
    LANG_START = "LANG_START"
    LANG_END = "LANG_END"

    # Atributos 5-D
    CLAVE_ATTR = "CLAVE_ATTR"
    NIVEL_ATTR = "NIVEL_ATTR"
    RAIZ_ATTR = "RAIZ_ATTR"
    ONT_ATTR = "ONT_ATTR"

    # Casos gramaticais
    VOC = "VOC"
    NOM = "NOM"
    ACU = "ACU"
    DAT = "DAT"
    GEN = "GEN"
    INS = "INS"
    LOC = "LOC"
    ABL = "ABL"

    # Tipos de dados
    INT_TYPE = "INT_TYPE"
    FLOAT_TYPE = "FLOAT_TYPE"
    BOOL_TYPE = "BOOL_TYPE"
    STRING_TYPE = "STRING_TYPE"
    FORMULA_TYPE = "FORMULA_TYPE"
    AUDIO_TYPE = "AUDIO_TYPE"
    IMAGE_TYPE = "IMAGE_TYPE"
    VIDEO_TYPE = "VIDEO_TYPE"
    TABLE_TYPE = "TABLE_TYPE"
    GRAPH_TYPE = "GRAPH_TYPE"

    # Palavras-chave de controle
    SERIE_KEYWORD = "SERIE_KEYWORD"
    PARALELO_KEYWORD = "PARALELO_KEYWORD"
    EM_KEYWORD = "EM_KEYWORD"
    FOR_KEYWORD = "FOR_KEYWORD"
    WHILE_KEYWORD = "WHILE_KEYWORD"
    IF_KEYWORD = "IF_KEYWORD"
    ELSE_KEYWORD = "ELSE_KEYWORD"
    RETURN_KEYWORD = "RETURN_KEYWORD"

    # Literais e identificadores
    STRING_LITERAL = "STRING_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    INT_LITERAL = "INT_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"
    ID = "ID"

    # Delimitadores
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    DOT = "DOT"
    ASSIGN = "ASSIGN"

    # Comentários e espaços
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"

# Mapeamento de palavras-chave
KEYWORDS = {
    "serie": TokenType.SERIE_KEYWORD,
    "paralelo": TokenType.PARALELO_KEYWORD,
    "em": TokenType.EM_KEYWORD,
    "for": TokenType.FOR_KEYWORD,
    "while": TokenType.WHILE_KEYWORD,
    "if": TokenType.IF_KEYWORD,
    "else": TokenType.ELSE_KEYWORD,
    "return": TokenType.RETURN_KEYWORD,
    "Int": TokenType.INT_TYPE,
    "Float": TokenType.FLOAT_TYPE,
    "Bool": TokenType.BOOL_TYPE,
    "String": TokenType.STRING_TYPE,
    "Formula": TokenType.FORMULA_TYPE,
    "Audio": TokenType.AUDIO_TYPE,
    "Image": TokenType.IMAGE_TYPE,
    "Video": TokenType.VIDEO_TYPE,
    "Table": TokenType.TABLE_TYPE,
    "Graph": TokenType.GRAPH_TYPE,
    "true": TokenType.BOOL_LITERAL,
    "false": TokenType.BOOL_LITERAL,
}

BLOCK_OPEN = {
    "[bloco]": TokenType.BLOCO_START,
    "[/bloco]": TokenType.BLOCO_END,
    "[sobrescrita]": TokenType.SOBRESCRITA_START,
    "[/sobrescrita]": TokenType.SOBRESCRITA_END,
    "[subescritas]": TokenType.SUBESCRITAS_START,
    "[/subescritas]": TokenType.SUBESCRITAS_END,
    "¡codigo!": TokenType.CODIGO_START,
    "!/codigo!": TokenType.CODIGO_END,
}

LANG_OPEN = {
    "¿python?": "python",
    "¿rust?": "rust",
    "¿javascript?": "javascript",
    "¿java?": "java",
    "¿csharp?": "csharp",
    "¿c++?": "cpp",
    "¿sql?": "sql",
    "¿r?": "r",
}

ATTR_OPEN = {
    "clave": TokenType.CLAVE_ATTR,
    "nivel": TokenType.NIVEL_ATTR,
    "raiz": TokenType.RAIZ_ATTR,
    "ont": TokenType.ONT_ATTR,
}

CASE_OPEN = {
    "VOC": TokenType.VOC,
    "NOM": TokenType.NOM,
    "ACU": TokenType.ACU,
    "DAT": TokenType.DAT,
    "GEN": TokenType.GEN,
    "INS": TokenType.INS,
    "LOC": TokenType.LOC,
    "ABL": TokenType.ABL,
}

TOKEN_REGEX = [
    (r"\[bloco\]", TokenType.BLOCO_START),
    (r"\[/bloco\]", TokenType.BLOCO_END),
    (r"\[sobrescrita\]", TokenType.SOBRESCRITA_START),
    (r"\[/sobrescrita\]", TokenType.SOBRESCRITA_END),
    (r"\[subescritas\]", TokenType.SUBESCRITAS_START),
    (r"\[/subescritas\]", TokenType.SUBESCRITAS_END),
    (r"¡codigo!", TokenType.CODIGO_START),
    (r"!/codigo!", TokenType.CODIGO_END),
    (r"\¿[a-z]+\?", TokenType.LANG_START),
    (r"\?[a-z]+\?", TokenType.LANG_END),
    (r"\[clave=\"[^\"]*\"\]", TokenType.CLAVE_ATTR),
    (r"\[nivel=\"[^\"]*\"\]", TokenType.NIVEL_ATTR),
    (r"\[raiz=\"[^\"]*\"\]", TokenType.RAIZ_ATTR),
    (r"\[ont=\"[^\"]*\"\]", TokenType.ONT_ATTR),
    (r"VOC|NOM|ACU|DAT|GEN|INS|LOC|ABL", TokenType.VOC),
    (r"Int|Float|Bool|String|Formula|Audio|Image|Video|Table|Graph", TokenType.INT_TYPE),
    (r"serie|paralelo|em|for|while|if|else|return", lambda m: KEYWORDS[m.group()]),
    (r"true|false", TokenType.BOOL_LITERAL),
    (r'"([^"\\]|\\.)*"', TokenType.STRING_LITERAL),
    (r"\d+\.\d+f?", TokenType.FLOAT_LITERAL),
    (r"\d+", TokenType.INT_LITERAL),
    (r"[a-zA-Z_][a-zA-Z0-9_]*", TokenType.ID),
    (r"\{|\}|\(|\)|;|\.|=", lambda m: {
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        ";": TokenType.SEMICOLON,
        ".": TokenType.DOT,
        "=": TokenType.ASSIGN,
    }[m.group()]),
    (r"//.*|/\*[\s\S]*?\*/", TokenType.COMMENT),
    (r"\s+", TokenType.WHITESPACE),
    (r"\n", TokenType.NEWLINE),
]

def tokenize_gurudev_code(code: str) -> List[Tuple[TokenType, str]]:
    tokens = []
    line = 1
    for pattern, token_type in TOKEN_REGEX:
        for match in re.finditer(pattern, code):
            value = match.group()
            if token_type == TokenType.WHITESPACE or token_type == TokenType.COMMENT:
                continue
            tokens.append((token_type, value))
    return tokens
