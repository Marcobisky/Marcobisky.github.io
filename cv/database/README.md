## Usage

### Tutorial

- `global/`: All possible CV entries.
- `local/`: Configurations for different CV versions.
- `utils/`: Python scripts to convert JSON to LaTeX or Quarto Markdown.
- `generated/`: Generated standalone LaTeX files.
    - Note the generated Quarto Markdown file is not here but `cv/cv-web.qmd` for easier preview in vscode.

### Workspace

```bash
cd cv/database
```

### Json to Latex

```bash
# With using default template and global json
# generate English CV pdf
./gen.sh <local-config-name> e.g. ./gen.sh cv-lite
# generate Chinese CV pdf
./gen.sh <local-config-name> e.g. ./gen.sh cv-lite-cn
```

### Json to Quarto Markdown

```bash
# HTML default CV
python3 utils/json2md.py global/default.json -s local/cv-web.json -o ../cv-web.qmd
python3 utils/json2qmd.py global/default.json -s local/cv-web.json -o ../cv-web.qmd --heading-level 1  # Use heading level 1 (#) instead of 2 (##), do not use this though!
```