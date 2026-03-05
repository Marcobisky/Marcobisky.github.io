## Usage

### Tutorial

- `global/`: All possible CV entries.
- `local/`: Configurations for different CV versions.
- `utils/`: Python scripts to convert JSON to LaTeX or Quarto Markdown.
- `generated/`: Generated LaTeX files (but partial, should be included in `cv-lite.tex` and `cv-lite-cn.tex`).
    - Note the generated Quarto Markdown file is not here but `cv/web.qmd` since it's easier for preview in vscode.

### Workspace

```bash
cd cv/database
```

### Json to Latex

```bash
# English default CV
python3 utils/json2tex.py global/cv.json -s local/lite.json -o generated/lite.tex
# Chinese default CV
python3 utils/json2tex.py global/cv-cn.json -s local/lite-cn.json -o generated/lite-cn.tex
```

### Json to Quarto Markdown

```bash
# HTML default CV
python3 utils/json2md.py global/cv.json -s local/web.json -o ../web.qmd
python3 utils/json2qmd.py global/cv.json -s local/web.json -o ../web.qmd --heading-level 1  # Use heading level 1 (#) instead of 2 (##), do not use this though!
```