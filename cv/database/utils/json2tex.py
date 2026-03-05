#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Callable, Optional, Tuple


# -----------------------------
# Text utils: smart quotes + math-preserve + minimal markdown
# -----------------------------

_LATEX_ESC = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",      # not applied inside $...$
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

_LINK_RE  = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE  = re.compile(r"\*\*([^*]+)\*\*")
_CODE_RE  = re.compile(r"`([^`]+)`")
_ITAL_RE  = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_MATH_RE  = re.compile(r"\$[^$]*\$")


def smart_quotes(s: str) -> str:
    if not s or '"' not in s:
        return s
    out = []
    for i, ch in enumerate(s):
        if ch != '"':
            out.append(ch)
            continue
        prev = s[i - 1] if i > 0 else ""
        if i == 0 or prev.isspace() or prev in "([{<\n\r\t":
            out.append("``")
        else:
            out.append("''")
    return "".join(out)


def escape_text(s: str) -> str:
    return "".join(_LATEX_ESC.get(ch, ch) for ch in (s or ""))


def split_math(s: str) -> List[Tuple[bool, str]]:
    if not s:
        return [(False, "")]
    out: List[Tuple[bool, str]] = []
    last = 0
    for m in _MATH_RE.finditer(s):
        if m.start() > last:
            out.append((False, s[last:m.start()]))
        out.append((True, m.group(0)))
        last = m.end()
    if last < len(s):
        out.append((False, s[last:]))
    return out


def md_text_to_latex(text: str) -> str:
    """Markdown-ish transform on a TEXT segment (non-math)."""
    text = smart_quotes(text or "")
    parts: List[str] = []
    i = 0

    while i < len(text):
        m_link = _LINK_RE.search(text, i)
        m_bold = _BOLD_RE.search(text, i)
        m_code = _CODE_RE.search(text, i)
        m_ital = _ITAL_RE.search(text, i)

        matches = [m for m in (m_link, m_bold, m_code, m_ital) if m]
        if not matches:
            parts.append(escape_text(text[i:]))
            break

        m = min(matches, key=lambda x: x.start())
        if m.start() > i:
            parts.append(escape_text(text[i:m.start()]))

        if m is m_link:
            t, url = m.group(1), (m.group(2) or "").strip()
            parts.append(rf"\MYhref{{{url}}}{{{md_inline_to_latex(t)}}}")
        elif m is m_bold:
            parts.append(rf"\textbf{{{md_inline_to_latex(m.group(1))}}}")
        elif m is m_code:
            parts.append(rf"\texttt{{{escape_text(m.group(1))}}}")
        else:
            parts.append(rf"\textit{{{md_inline_to_latex(m.group(1))}}}")

        i = m.end()

    return "".join(parts)


def md_inline_to_latex(s: str) -> str:
    """Inline transform with math-preserve: keep $...$ literal."""
    segs = split_math(s or "")
    out: List[str] = []
    for is_math, seg in segs:
        out.append(seg if is_math else md_text_to_latex(seg))
    return "".join(out)


def section_title_to_latex(title: str) -> str:
    # For \section{...} keep it plain escaped (no markdown expected)
    return escape_text(smart_quotes(title or ""))


def title_field_to_latex(title: str) -> str:
    """
    Title field: if it's a *full* markdown link [text](url),
    render as \MYhref{url}{\textbf{text}}; else \textbf{...}
    """
    t = smart_quotes((title or "").strip())
    m = _LINK_RE.fullmatch(t)
    if m:
        text, url = m.group(1), (m.group(2) or "").strip()
        return rf"\MYhref{{{url}}}{{\textbf{{{md_inline_to_latex(text)}}}}}"
    return rf"\textbf{{{md_inline_to_latex(t)}}}"


# -----------------------------
# IO + indexing
# -----------------------------

def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def index_template_items(cv: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Build index: template_name -> {label -> item_dict}
    cv.json shape: {"template-entry":[{label:...},...], "template-2col-mid":[...], ...}
    """
    idx: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for tmpl, items in (cv or {}).items():
        if not isinstance(items, list):
            continue
        m: Dict[str, Dict[str, Any]] = {}
        for it in items:
            lab = it.get("label")
            if lab:
                m[lab] = it
        idx[tmpl] = m
    return idx


def pick_items(
    idx: Dict[str, Dict[str, Dict[str, Any]]],
    template: str,
    labels: List[str],
    section_name: str,
) -> List[Dict[str, Any]]:
    pool = idx.get(template, {})
    out: List[Dict[str, Any]] = []
    for lab in labels:
        it = pool.get(lab)
        if it is None:
            print(f"[warn] missing label '{lab}' in template '{template}' for section '{section_name}'", file=sys.stderr)
            continue
        out.append(it)
    return out


# -----------------------------
# Templates
# -----------------------------

def render_template_entry(items: List[Dict[str, Any]], enabled: List[str]) -> str:
    """
    template-entry:
      - title (bold, link-aware) \hfill date
      - optional extra italic small line
      - optional description itemize
    enabled subset controls which fields appear: title/date/extra/description
    """
    en = set(enabled or [])
    out: List[str] = []

    for it in items:
        title = title_field_to_latex(it.get("title", ""))
        date  = md_inline_to_latex(it.get("date", ""))

        # line 1
        if "title" in en and "date" in en:
            out.append(rf"{title} \hfill {date}")
        elif "title" in en:
            out.append(rf"{title}")
        elif "date" in en:
            out.append(rf"{date}")
        else:
            # if neither enabled, nothing sensible to print; skip entry
            continue
        out.append("")

        # extra line
        if "extra" in en:
            extra = (it.get("extra") or "").strip()
            if extra:
                out.append(r"\vspace{-0.5em} \begin{small} \textit{" + md_inline_to_latex(extra) + r"} \end{small} \vspace{-0.5em}")
                out.append("")

        # description bullet list
        if "description" in en:
            desc = it.get("description") or []
            if desc:
                out.append(r"\begin{itemize}")
                out.append(r"    \setlength\itemsep{-0.5em}")
                for line in desc:
                    out.append("    " + r"\item " + md_inline_to_latex(line))
                out.append(r"\end{itemize}")
                out.append("")

    return "\n".join(out).rstrip() + "\n"


def render_template_2col_mid(items: List[Dict[str, Any]], enabled: List[str]) -> str:
    """
    template-2col-mid:
      tabularx 2 columns: left | middle
    enabled controls which fields used (usually left,middle)
    """
    en = set(enabled or [])
    if not {"left", "middle"} & en:
        return ""

    out: List[str] = []
    out.append(r"\begin{tabularx}{\linewidth}{@{}l X@{}}")
    for it in items:
        left   = md_inline_to_latex(it.get("left", ""))   if "left" in en   else ""
        middle = md_inline_to_latex(it.get("middle", "")) if "middle" in en else ""
        out.append(rf"\textbf{{{left}}} &  \normalsize{{{middle}}}\\")
    out.append(r"\end{tabularx}")
    out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_template_2col_right(items: List[Dict[str, Any]], enabled: List[str]) -> str:
    """
    template-2col-right:
      Each row: \textbf{left} \hfill right \\ (except last optional)
    enabled controls (left,right)
    """
    en = set(enabled or [])
    if not {"left", "right"} & en:
        return ""

    out: List[str] = []
    for i, it in enumerate(items):
        left  = md_inline_to_latex(it.get("left", ""))  if "left" in en  else ""
        right = md_inline_to_latex(it.get("right", "")) if "right" in en else ""
        line = rf"\textbf{{{left}}} \hfill {right}"
        if i != len(items) - 1:
            line += r" \\"
        out.append(line)
    out.append("")
    return "\n".join(out).rstrip() + "\n"


TEMPLATES: Dict[str, Callable[[List[Dict[str, Any]], List[str]], str]] = {
    "template-entry": render_template_entry,
    "template-2col-mid": render_template_2col_mid,
    "template-2col-right": render_template_2col_right,
}


# -----------------------------
# Generator
# -----------------------------

def generate(cv: Dict[str, Any], spec: Dict[str, Any]) -> str:
    idx = index_template_items(cv)
    pieces: List[str] = []

    # spec order = section output order (json preserves insertion order)
    for section_name, cfg in (spec or {}).items():
        if not isinstance(cfg, dict):
            continue

        template = cfg.get("template")
        items = cfg.get("items", [])
        enabled = cfg.get("enabled", [])

        if template not in TEMPLATES:
            print(f"[warn] unknown template '{template}' in section '{section_name}'", file=sys.stderr)
            continue
        if not isinstance(items, list) or not isinstance(enabled, list):
            print(f"[warn] bad spec in section '{section_name}': items/enabled must be lists", file=sys.stderr)
            continue

        picked = pick_items(idx, template, items, section_name)
        if not picked:
            continue

        pieces.append(rf"\section{{{section_title_to_latex(section_name)}}}")
        pieces.append("")
        pieces.append(TEMPLATES[template](picked, enabled))
        pieces.append("")

    return "\n".join(pieces).strip() + "\n\n"


# -----------------------------
# CLI
# -----------------------------

def main():
    ap = argparse.ArgumentParser(description="Generate generated.tex from cv.json + general.json (template-based)")
    ap.add_argument("cv_json", type=str, help="Path to cv.json")
    ap.add_argument("-s", "--spec", required=True, type=str, help="Path to general.json")
    ap.add_argument("-o", "--output", default="generated.tex", type=str, help="Output .tex file")
    args = ap.parse_args()

    cv = load_json(Path(args.cv_json))
    spec = load_json(Path(args.spec))

    tex = generate(cv, spec)
    Path(args.output).write_text(tex, encoding="utf-8")
    print(f"[ok] wrote {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()