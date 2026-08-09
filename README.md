# momarci13.github.io

Static personal portfolio for quantitative finance, model validation, statistics, and
machine-learning research.

## Local preview

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`.

## Rebuild the CV

The deployed PDF is generated from the editable ReportLab source:

```powershell
python scripts/build_cv.py
```

The script writes `marcell_molnar_cv.pdf`, which is the file linked from the site.
