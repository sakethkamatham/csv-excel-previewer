# Python CLI CSV Reader

A lightweight Python tool for previewing the first 5 rows of CSV and Excel files. Runs as a **command-line tool** or a **desktop GUI** — no arguments launches the GUI automatically.

## Features

- Supports `.csv`, `.xlsx`, and `.xls` files
- **CLI mode** — prints the first 5 rows as a formatted table directly in the terminal
- **GUI mode** — opens a desktop window with a file browser and scrollable table view
- Clear error messages for unsupported formats and read errors

## Requirements

- Python 3.x
- `pandas`
- `openpyxl`
- `tkinter` (included with most Python installations)

## Installation

```bash
git clone <repository-url>
cd python-cli-csv-reader
pip install -r requirements.txt
```

## Usage

### GUI Mode

Run with no arguments to open the desktop file previewer:

```bash
python reader.py
```

A window will open where you can browse for a file and view the first 5 rows in a scrollable table.

### CLI Mode

Pass a file path directly to print the preview in the terminal:

```bash
python reader.py <file>
```

**Examples:**

```bash
python reader.py data.csv
python reader.py report.xlsx
python reader.py spreadsheet.xls
```

**Sample output:**

```
   name  age       city
0  Alice   30   New York
1    Bob   25    Chicago
2  Carol   35    Houston
```

## How It Works

- If a file argument is provided, the script reads the file and prints `df.head()` to stdout.
- If no argument is provided, a `tkinter` GUI window launches with a Browse button, a Load button, and a `ttk.Treeview` table that displays the first 5 rows with column headers and row indices.
- Both modes share the same `read_file()` function, which uses `pandas` to parse CSV or Excel files.

## License

MIT
