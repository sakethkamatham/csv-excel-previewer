import argparse
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd


def read_file(path: str):
    ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    if ext == "csv":
        return pd.read_csv(path)
    elif ext in ("xlsx", "xls"):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format '.{ext}'. Use a .csv or .xlsx/.xls file.")


def main():
    parser = argparse.ArgumentParser(description="Print the first 5 rows of a CSV or Excel file.")
    parser.add_argument("file", help="Path to the CSV or Excel file")
    args = parser.parse_args()

    try:
        df = read_file(args.file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(df.head().to_string(index=True))


def launch_gui():
    root = tk.Tk()
    root.title("CSV / Excel Previewer")
    root.minsize(700, 450)

    # Instruction label
    tk.Label(root, text="Select a CSV or Excel file to preview the first 5 rows.",
             font=("", 12)).pack(pady=(12, 6))

    # File selection row
    file_var = tk.StringVar()
    frame = tk.Frame(root)
    frame.pack(fill="x", padx=12, pady=4)

    entry = tk.Entry(frame, textvariable=file_var, state="readonly", width=60)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

    def browse():
        path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("CSV / Excel files", "*.csv *.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            file_var.set(path)
            status_var.set("")

    tk.Button(frame, text="Browse...", command=browse).pack(side="left")

    # Load button
    def load_file():
        path = file_var.get().strip()
        if not path:
            messagebox.showwarning("No file selected", "Please browse for a file first.")
            return
        try:
            df = read_file(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            populate_treeview(None)
            status_var.set("")
            return
        populate_treeview(df)
        status_var.set(f"Loaded {min(5, len(df))} row(s) — {len(df.columns)} column(s)  |  {path.split('/')[-1]}")

    tk.Button(root, text="Load File", command=load_file, font=("", 11), width=14).pack(pady=6)

    # Treeview with scrollbars
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=12, pady=(0, 4))

    tree = ttk.Treeview(tree_frame, show="headings")
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    hsb.pack(side="bottom", fill="x")
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def populate_treeview(df):
        tree.delete(*tree.get_children())
        tree["columns"] = []
        if df is None:
            return
        cols = ["#"] + list(df.columns.astype(str))
        tree["columns"] = cols
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=max(80, len(col) * 10), anchor="w")
        for row in df.head().itertuples():
            tree.insert("", "end", values=list(row))

    # Status label
    status_var = tk.StringVar()
    tk.Label(root, textvariable=status_var, anchor="w", fg="gray").pack(
        fill="x", padx=12, pady=(0, 8))

    root.lift()
    root.focus_force()
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        launch_gui()
