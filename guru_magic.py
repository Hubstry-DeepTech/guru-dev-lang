"""
Jupyter/Colab magic extension for GuruDev.
Usage inside a notebook:
    %load_ext guru_magic
    %%guru
    [bloco]
      ¡codigo!
        VOC.console write("Hello from GuruDev!");
      !/codigo!
    [/bloco]
"""

from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.display import display, Markdown, HTML
import tempfile, subprocess, os, sys

@magics_class
class GuruMagic(Magics):
    @cell_magic
    def guru(self, line, cell):
        # Escreve código temporário
        with tempfile.NamedTemporaryFile(mode="w", suffix=".guru", delete=False) as f:
            f.write(cell)
            guru_path = f.name
        gurub_path = guru_path.replace(".guru", ".gurub")

        # Compila
        cmd_compile = [sys.executable, "-m", "gurudev.compiler", guru_path, "--out", gurub_path]
        result = subprocess.run(cmd_compile, capture_output=True, text=True)
        if result.returncode != 0 or not os.path.exists(gurub_path):
            display(Markdown(f"❌ **Compile error**:\n```\n{result.stderr}\n```"))
            return

        # Executa
        cmd_run = [sys.executable, "-m", "gurudev.vm", gurub_path]
        exec_result = subprocess.run(cmd_run, capture_output=True, text=True)
        display(HTML(f"<pre style='color:#00ff00'>{exec_result.stdout}</pre>"))
        if exec_result.stderr:
            display(Markdown("⚠️ **stderr**:\n```\n" + exec_result.stderr + "\n```"))

def load_ipython_extension(ipython):
    ipython.register_magic_function(GuruMagic, magic_kind="class")
