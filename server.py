import os
import subprocess
import tempfile
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.post("/compile")
def compile_latex():
    data = request.get_json(silent=True) or {}
    tex = data.get("tex", "")

    if not tex or "\\documentclass" not in tex or "\\begin{document}" not in tex or "\\end{document}" not in tex:
        return jsonify({"error": "Invalid LaTeX: expected a full document."}), 400

    with tempfile.TemporaryDirectory() as tmp:
        tex_path = os.path.join(tmp, "main.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex)

        try:
            subprocess.run(
                ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                cwd=tmp,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=60,
            )
        except subprocess.CalledProcessError as e:
            log = e.stdout.decode("utf-8", errors="ignore")
            return jsonify({"error": "Compilation failed", "log": log[:8000]}), 400
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Compilation timed out"}), 408

        pdf_path = os.path.join(tmp, "main.pdf")
        return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="resume.pdf")

@app.get("/health")
def health():
    return {"status": "ok"}
