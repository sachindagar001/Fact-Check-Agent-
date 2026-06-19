import re
import json
import hashlib
from datetime import datetime
from pypdf import PdfReader
import config

_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)

def extract_json_object(text: str) -> dict:
    if not text: raise ValueError("Empty LLM response.")
    c = text.strip()
    c = re.sub(r"^```(?:json)?\s*", "", c)
    c = re.sub(r"\s*```$", "", c)
    try: 
        return json.loads(c)
    except json.JSONDecodeError: 
        pass
    m = _JSON_RE.search(c)
    if m:
        try: 
            return json.loads(m.group(0))
        except json.JSONDecodeError: 
            pass
    raise ValueError(f"Could not extract JSON: {c[:300]}...")

def extract_text_from_pdf(f) -> str:
    reader = PdfReader(f)
    return "\n".join((p.extract_text() or "") for p in reader.pages)

def file_hash(f) -> str:
    f.seek(0)
    h = hashlib.sha256()
    while True:
        chunk = f.read(8192)
        if not chunk: break
        h.update(chunk)
    f.seek(0)
    return h.hexdigest()

def render_markdown_report(results: list, pdf_name: str, model_name: str) -> str:
    lines = [
        f"# Fact-Check Report",
        f"**Source PDF:** `{pdf_name}`  ",
        f"**Generated:** {datetime.utcnow().isoformat(timespec='seconds')}Z  ",
        f"**Model:** `{model_name}`  ",
        f"**Claims checked:** {len(results)}",
        "", "---", ""
    ]
    for i, r in enumerate(results, 1):
        v = r.get("verdict", "Error")
        badge = config.VERDICT_BADGE.get(v, "❓")
        lines += [f"## {i}. {badge} {v}", "", f"**Original claim:** {r.get('original_claim', '')}", ""]
        if v == "Inaccurate" and r.get("correct_fact"): 
            lines += [f"**Correct fact:** {r.get('correct_fact')}", ""]
        if r.get("evidence"): 
            lines += [f"**Evidence:** {r.get('evidence')}", ""]
        srcs = [s for s in r.get("sources", []) if s]
        if srcs: 
            lines += ["**Sources:**"] + [f"- {s}" for s in srcs] + [""]
        lines += ["---", ""]
    return "\n".join(lines)