#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# IO
# -----------------------------

def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def index_by_label(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    m: Dict[str, Dict[str, Any]] = {}
    for it in items or []:
        lab = it.get("label")
        if lab:
            m[lab] = it
    return m


def build_cv_index(cv: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    cv.json:
      {
        "template-entry":[{label,...},...],
        "template-2col-mid":[{label,left,middle},...],
        "template-2col-right":[{label,left,right},...]
      }
    -> idx[template][label] = item
    """
    idx: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for tmpl, arr in (cv or {}).items():
        if isinstance(arr, list):
            idx[tmpl] = index_by_label(arr)
    return idx


# -----------------------------
# Quarto formatting helpers
# -----------------------------

def norm_newlines(s: str) -> str:
    return (s or "").replace("\r\n", "\n").replace("\r", "\n")


def render_heading(level: int, title: str) -> str:
    return f"{'#' * level} {title}\n"


def render_date(date: str) -> str:
    # match your format: [(*Sept ...*)]{.cvdate}
    date = norm_newlines(date).strip()
    return f"[(*{date}*)]{{.cvdate}}"


def render_margin_image(caption: str, image_path: str) -> str:
    """
    Quarto HTML-only margin content block.
    """
    caption = norm_newlines(caption).strip()
    image_path = norm_newlines(image_path).strip()
    if not caption or not image_path:
        return ""
    return (
        "::: {.content-visible when-format=\"html\"}\n"
        f"![{caption}]({image_path}){{.column-margin}}\n"
        ":::\n"
    )


def render_bullets(lines: List[str], indent: int = 2) -> str:
    """
    Render as:
      - ...
      - ...
    with leading spaces (indent) to match your sample.
    """
    if not lines:
        return ""
    pad = " " * indent
    out = []
    for line in lines:
        line = norm_newlines(line).strip()
        if not line:
            continue
        out.append(f"{pad}- {line}")
    return "\n".join(out) + "\n"


# -----------------------------
# Template renderers -> QMD
# -----------------------------

def qmd_entry(item: Dict[str, Any], enabled: List[str]) -> str:
    """
    template-entry -> Quarto:
      **TITLE** [(*DATE*)]{.cvdate}

      *EXTRA*   (if enabled + present)

        - desc...
    Also emits margin image block if image+caption exist.
    """
    en = set(enabled or [])
    title = norm_newlines(item.get("title", "")).strip()
    date = norm_newlines(item.get("date", "")).strip()
    extra = norm_newlines(item.get("extra", "")).strip()
    desc = item.get("description") or []

    image = norm_newlines(item.get("image", "")).strip()
    caption = norm_newlines(item.get("caption", "")).strip()

    out: List[str] = []

    # headline line
    headline_parts = []
    if "title" in en and title:
        headline_parts.append(f"**{title}**")
    if "date" in en and date:
        headline_parts.append(render_date(date))
    if headline_parts:
        out.append(" ".join(headline_parts))
        out.append("")

    # optional margin image
    if image and caption:
        out.append(render_margin_image(caption, image).rstrip())
        out.append("")

    # extra line
    if "extra" in en and extra:
        out.append(f"*{extra}*")
        out.append("")

    # bullets
    if "description" in en and desc:
        out.append(render_bullets(desc, indent=2).rstrip())
        out.append("")

    return "\n".join([x for x in out if x is not None]).rstrip() + "\n"


def qmd_2col_mid(items: List[Dict[str, Any]], enabled: List[str]) -> str:
    """
    template-2col-mid:
      **LEFT**: MIDDLE
    """
    en = set(enabled or [])
    out: List[str] = []
    for it in items:
        left = norm_newlines(it.get("left", "")).strip() if "left" in en else ""
        mid = norm_newlines(it.get("middle", "")).strip() if "middle" in en else ""
        if not (left or mid):
            continue
        # keep markdown in mid (links/code) as-is
        out.append(f"**{left}**: {mid}".rstrip())
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def qmd_2col_right(items: List[Dict[str, Any]], enabled: List[str]) -> str:
    """
    template-2col-right:
      **LEFT** [(*RIGHT*)]{.cvdate}
    (keeps the same date styling)
    """
    en = set(enabled or [])
    out: List[str] = []
    for it in items:
        left = norm_newlines(it.get("left", "")).strip() if "left" in en else ""
        right = norm_newlines(it.get("right", "")).strip() if "right" in en else ""
        if not (left or right):
            continue
        line_parts = []
        if left:
            # keep links in left as-is; still bold the whole left span like your style
            line_parts.append(f"**{left}**")
        if right:
            line_parts.append(render_date(right))
        out.append(" ".join(line_parts).rstrip())
    out.append("")
    return "\n\n".join(out).rstrip() + "\n"


TEMPLATE_QMD = {
    "template-entry": qmd_entry,
    "template-2col-mid": None,    # handled as section-level list
    "template-2col-right": None,  # handled as section-level list
}


# -----------------------------
# Generation by spec (general.json)
# -----------------------------

def generate_qmd(cv: Dict[str, Any], spec: Dict[str, Any], heading_level: int = 2) -> str:
    """
    spec.json:
      {
        "Education": {"template":"template-entry","items":[...],"enabled":[...]},
        ...
      }
    """
    idx = build_cv_index(cv)

    pieces: List[str] = []
    for section_name, cfg in (spec or {}).items():
        if not isinstance(cfg, dict):
            continue
        template = cfg.get("template")
        labels = cfg.get("items", [])
        enabled = cfg.get("enabled", [])

        if template not in idx:
            print(f"[warn] template '{template}' not found in cv.json for section '{section_name}'", file=sys.stderr)
            continue
        if not isinstance(labels, list) or not isinstance(enabled, list):
            print(f"[warn] bad spec in section '{section_name}': items/enabled must be lists", file=sys.stderr)
            continue

        pieces.append(render_heading(heading_level, section_name).rstrip())
        pieces.append("")

        pool = idx[template]
        picked = []
        for lab in labels:
            it = pool.get(lab)
            if it is None:
                print(f"[warn] missing label '{lab}' in template '{template}' for section '{section_name}'", file=sys.stderr)
                continue
            picked.append(it)

        if template == "template-entry":
            for it in picked:
                pieces.append(qmd_entry(it, enabled).rstrip())
                pieces.append("")
        elif template == "template-2col-mid":
            pieces.append(qmd_2col_mid(picked, enabled).rstrip())
            pieces.append("")
        elif template == "template-2col-right":
            pieces.append(qmd_2col_right(picked, enabled).rstrip())
            pieces.append("")
        else:
            print(f"[warn] unsupported template '{template}' (add renderer) for section '{section_name}'", file=sys.stderr)

    # ensure trailing blank lines (helps Quarto render spacing consistently)
    return "\n".join(pieces).strip() + "\n\n"


# -----------------------------
# CLI
# -----------------------------

def main():
    ap = argparse.ArgumentParser(description="Generate Quarto Markdown (.qmd) from cv.json + general.json")
    ap.add_argument("cv_json", type=str, help="Path to cv.json")
    ap.add_argument("-s", "--spec", required=True, type=str, help="Path to general.json (section ordering & selection)")
    ap.add_argument("-o", "--output", default="generated.qmd", type=str, help="Output qmd file")
    ap.add_argument("--heading-level", default=2, type=int, help="Heading level for sections (default: 2 -> ##)")
    args = ap.parse_args()

    cv = load_json(Path(args.cv_json))
    spec = load_json(Path(args.spec))

    qmd = generate_qmd(cv, spec, heading_level=args.heading_level)
    Path(args.output).write_text(qmd, encoding="utf-8")
    print(f"[ok] wrote {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()