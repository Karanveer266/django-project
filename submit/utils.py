"""
Helper that compiles / runs source code for C++, Python or Java
without any containerisation.  Returns a dict with:
    status ∈ {"OK", "COMPILATION_ERROR", "RUNTIME_ERROR", "TIMEOUT", "ERROR"}
    stdout – program output
    stderr – compiler / run-time diagnostics
"""

import subprocess
import tempfile
from pathlib import Path

# ─────────────────────────────────────────
# Language configuration table
# ─────────────────────────────────────────
LANGS = {
    # ---------- C++ (g++) ----------
    "cpp": {
        "ext": ".cpp",
        "compile": lambda src, exe: [
            "g++", src, "-O2", "-pipe", "-static", "-s", "-o", exe
        ],
        "run": lambda exe, _src, _tmp: [exe],
    },
    # ---------- Python 3 ----------
    "py": {
        "ext": ".py",
        "compile": None,                                        # nothing to compile
        "run": lambda _exe, src, _tmp: ["python3", "-u", src],  # -u = unbuffered
    },
    # ---------- Java (JDK ≥ 8) ----------
    # Assumes learner’s public class is called `Main`
    "java": {
        "ext": ".java",
        "compile": lambda src, _exe: ["javac", src],                 # javac drops .class next to .java
        "run": lambda _exe, _src, tmp: ["java", "-cp", str(tmp), "Main"],
    },
}

# ─────────────────────────────────────────
# Core execution function
# ─────────────────────────────────────────
def run_code(language: str, code: str, input_data: str, timeout: int = 5):
    """
    Execute `code` written in `language` with `input_data` on stdin.

    Returns:
        dict(status, stdout, stderr)
    """
    lang = LANGS.get(language)
    if lang is None:
        return {
            "status": "ERROR",
            "stdout": "",
            "stderr": f"Unsupported language: {language}",
        }

    # Fresh temp directory per submission; automatically deleted afterwards
    with tempfile.TemporaryDirectory(prefix="run_") as tmpdir:
        tmp_path = Path(tmpdir)
        src      = tmp_path / f"Main{lang['ext']}"
        exe      = tmp_path / "main"                       # used only for C++

        src.write_text(code, encoding="utf-8")

        # -------- compile (if needed) --------
        if lang["compile"]:
            compile_cmd = [
                arg.format(src=str(src), exe=str(exe)) for arg in lang["compile"]
            ]
            comp = subprocess.run(
                compile_cmd, capture_output=True, text=True
            )
            if comp.returncode != 0:
                return {
                    "status": "COMPILATION_ERROR",
                    "stdout": comp.stdout,
                    "stderr": comp.stderr,
                }

        # -------- execute --------
        run_cmd = lang["run"](str(exe), str(src), tmp_path)
        try:
            run = subprocess.run(
                run_cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            status = "OK" if run.returncode == 0 else "RUNTIME_ERROR"
            return {
                "status": status,
                "stdout": run.stdout,
                "stderr": run.stderr,
            }
        except subprocess.TimeoutExpired as e:
            return {
                "status": "TIMEOUT",
                "stdout": e.stdout or "",
                "stderr": e.stderr or "",
            }
