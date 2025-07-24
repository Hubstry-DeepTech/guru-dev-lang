"""
gurudev/compiler.py
Compiles GuruDev source (.guru) → GuruByte (.gurub).
Preserves 5-D semantic coordinates and produces JSON-based bytecode.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, List

# -------------------------
# Constants
# -------------------------
GURU_SIGNATURE = "GURU"
VERSION = "0.1.0"
ENCODING = "UTF-8"

# -------------------------
# Helper: SHA-256 checksum
# -------------------------
def checksum(content: str) -> str:
    return hashlib.sha256(content.encode(ENCODING)).hexdigest()

# -------------------------
# Main compiler entry
# -------------------------
def compile_ast(ast: List[Dict[str, Any]], out_path: Path) -> Path:
    """
    Converts an AST (from parser.py) into a .gurub file.
    Each block becomes a CODEBLOCK entry with embedded 5-D context.
    """
    header = {
        "Signature": GURU_SIGNATURE,
        "Version": VERSION,
        "Encoding": ENCODING,
    }

    context = {}
    constants = {}
    codeblocks = []

    for block in ast:
        # Extract 5-D metadata from sobrescrita
        for attr in block.get("sobrescrita", []):
            context[attr["key"]] = attr["value"]

        # Embed GuruDev code
        guru_code = block["codigo"]["source"]
        codeblocks.append({
            "id": f"block_{len(codeblocks)}",
            "COORD": context,  # 5-D coordinates
            "INSTR": ["LOAD", "EVALUATE", "DISPLAY"],
            "SOURCE": guru_code
        })

        # Embed foreign variants as constants for now
        for foreign in block.get("subescritas", []):
            constants[f"foreign_{foreign['language']}_{len(constants)}"] = foreign["source"]

    gurub = {
        "HEADER": header,
        "CONTEXT": context,
        "CONSTANTS": constants,
        "CODEBLOCKS": codeblocks,
        "FOOTER": {
            "Checksum": checksum(json.dumps(gurub, sort_keys=True))
        }
    }

    with open(out_path, "w", encoding=ENCODING) as f:
        json.dump(gurub, f, indent=2)
    return out_path
