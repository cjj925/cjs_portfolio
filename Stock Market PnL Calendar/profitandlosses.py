import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date
import calendar
import csv
import math
import os
import json

# Colors 
DARK_BG        = "#0b1220"
HEADER_BG      = "#0f1730"
HEADER_FG      = "#e6e8ed"
GRID_BG        = "#FAF2F2"
GRID_LINE      = "#e6e8ef"
DAY_TEXT       = "#0b1220"
VAL_TEXT       = "#0b1220"
BTN_BG         = "#1a2442"
BTN_FG         = "#ffffff"
BTN_BG_ACTIVE  = "#223058"

# Heatmap color endpoints
POS_BASE = (231, 248, 239)
POS_PEAK = (32, 164, 112)
NEG_BASE = (255, 236, 239)
NEG_PEAK = (220, 38, 38)

# Smooth heatmap coloring
def lerp(a, b, t): return a + (b - a) * t

def clamp01(x): return max(0.0, min(1.0, x))

def rgb_to_hex(rgb):
    r, g, b = [int(round(v)) for v in rgb]
    return f"#{r:02x}{g:02x}{b:02x}"

def interp_color(base, peak, t):
    return rgb_to_hex((lerp(base[0], peak[0], t),
                       lerp(base[1], peak[1], t),
                       lerp(base[2], peak[2], t)))
    
def heat_color(value, vmax):
    if value == 0:
        return GRID_BG
    if vmax <= 0:
        vmax = 1.0
    t = clamp01(abs(value) / vmax)
    t = math.sqrt(t)
    return interp_color(POS_BASE if value > 0 else NEG_BASE,
                        POS_PEAK if value > 0 else NEG_PEAK, t)

def parse_amount(text: str) -> float:
    """Accept +$100, $-55.75, 1,200, (250), +1,000.00."""
    if text is None:
        raise ValueError("empty")
    s = text.strip().replace("$", "").replace(",", "").replace("+", "")
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    return float(s)

class PnLCalendar:
    # Persistence paths 
    def _data_dir(self):
        return os.path.join(os.path.expanduser("~"), ".pnl_calendar")
    def _data_path(self):
        return os.path.join(self._data_dir(), "data.json")
    def _month_key(self, y, m):
        return f"{y:04d}-{m:02d}"

    def __init__(self, root):
        # Root window setup
        self.root = root
        self.root.title("P&L Calendar")
        self.root.configure(bg=DARK_BG)
        self.today = date.today()
        self.cur_year = tk.IntVar(value=self.today.year)
        self.cur_month = tk.IntVar(value=self.today.month)

        self.data = {} # Stores all PnL data
        self._ensure_data_loaded()

        # ttk styles
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure("WB.TButton", background=BTN_BG, foreground=BTN_FG, padding=(12, 6), borderwidth=0)
        self.style.map("WB.TButton",
            background=[("active", BTN_BG_ACTIVE), ("pressed", BTN_BG_ACTIVE)],
            foreground=[("disabled", "#9aa3b2")])
        self.style.configure("WBHeader.TLabel", background=HEADER_BG, foreground=HEADER_FG)
        self.style.configure("WBDark.TLabel", background=DARK_BG, foreground="#eef2f7")
        self.style.configure("WBSub.TLabel", background=DARK_BG, foreground="#9aa3b2")
        self.style.configure("WBHeader.TFrame", background=HEADER_BG)
        self.style.configure("WBDark.TFrame", background=DARK_BG)
        self.style.configure("WB.TEntry", fieldbackground="#ffffff", foreground=DAY_TEXT)

        self.cells = {} 

        # Header
        self.header = ttk.Frame(root, style="WBHeader.TFrame")
        self.header.pack(fill="x")
        self.build_header()

        # Calendar area
        self.wrap = ttk.Frame(root, style="WBDark.TFrame")
        self.wrap.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas = tk.Frame(self.wrap, bg=GRID_BG, highlightbackground=GRID_LINE, highlightthickness=1)
        self.canvas.pack(fill="both", expand=True)

        # Footer
        self.footer = ttk.Frame(root, style="WBDark.TFrame")
        self.footer.pack(fill="x", padx=12, pady=(0,12))
        self.build_footer()

        self.render_calendar()

        # Save on close 
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # persistence 
    def _ensure_data_loaded(self):
        os.makedirs(self._data_dir(), exist_ok=True)
        path = self._data_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
                
    def _save_data(self):
        # Avoid corruption
        path = self._data_path()
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        
    def on_close(self):
        self._save_data()
        self.root.destroy()

    # UI 
    def build_header(self):
        left = ttk.Frame(self.header, style="WBHeader.TFrame")
        left.pack(side="left", padx=12, pady=10)
        ttk.Button(left, text="◀", style="WB.TButton", command=self.prev_month).pack(side="left", padx=(0,8))
        self.title_lbl = ttk.Label(left, text=self.month_title(), style="WBHeader.TLabel", font=("Arial", 14, "bold"))
        self.title_lbl.pack(side="left")
        ttk.Button(left, text="▶", style="WB.TButton", command=self.next_month).pack(side="left", padx=(8,0))

        right = ttk.Frame(self.header, style="WBHeader.TFrame")
        right.pack(side="right", padx=12, pady=10)
        ttk.Button(right, text="Today", style="WB.TButton", command=self.goto_today).pack(side="left", padx=6)
        ttk.Button(right, text="Import CSV", style="WB.TButton", command=self.load_csv).pack(side="left", padx=6)
        ttk.Button(right, text="Export CSV", style="WB.TButton", command=self.save_csv).pack(side="left", padx=6)  # <-- fixed: no extra ')'

    def build_footer(self):
        def stat(lbl_txt):
            f = ttk.Frame(self.footer, style="WBDark.TFrame")
            ttk.Label(f, text=lbl_txt, style="WBSub.TLabel").pack(anchor="w")
            v = ttk.Label(f, text="—", style="WBDark.TLabel", font=("Arial", 12, "bold"))
            v.pack(anchor="w")
            return f, v
        self.total_box, self.total_val = stat("Monthly Total")
        self.avg_box, self.avg_val = stat("Average (filled days)")
        self.win_box, self.win_val = stat("Win Rate")
        self.total_box.pack(side="left", padx=12)
        self.avg_box.pack(side="left", padx=12)
        self.win_box.pack(side="left", padx=12)

        right = ttk.Frame(self.footer, style="WBDark.TFrame")
        right.pack(side="right")
        ttk.Button(right, text="Clear Month", style="WB.TButton", command=self.clear_month).pack(side="right", padx=6)

    # Calendar 
    def month_title(self):
        return f"{calendar.month_name[int(self.cur_month.get())]} {int(self.cur_year.get())}"
    def prev_month(self):
        m, y = int(self.cur_month.get()), int(self.cur_year.get())
        m = 12 if m == 1 else m - 1
        y = y - 1 if m == 12 else y
        self.cur_month.set(m); self.cur_year.set(y); self.refresh()
    def next_month(self):
        m, y = int(self.cur_month.get()), int(self.cur_year.get())
        m = 1 if m == 12 else m + 1
        y = y + 1 if m == 1 else y
        self.cur_month.set(m); self.cur_year.set(y); self.refresh()
    def goto_today(self):
        self.cur_month.set(self.today.month); self.cur_year.set(self.today.year); self.refresh()
    def refresh(self):
        self.title_lbl.config(text=self.month_title())
        self.render_calendar()

    def render_calendar(self):
        for w in self.canvas.winfo_children():
            w.destroy()
        self.cells.clear()

        year = int(self.cur_year.get())
        month = int(self.cur_month.get())
        mkey = self._month_key(year, month)
        month_data = self.data.get(mkey, {})

        headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for c, name in enumerate(headers):
            h = tk.Label(self.canvas, text=name, bg=GRID_BG, fg=DAY_TEXT, font=("Arial", 10, "bold"))
            h.grid(row=0, column=c, sticky="nsew", pady=(0,4))
            self.canvas.grid_columnconfigure(c, weight=1)

        cal = calendar.Calendar(firstweekday=0)
        for r, week in enumerate(cal.monthdatescalendar(year, month), start=1):
            self.canvas.grid_rowconfigure(r, weight=1)
            for c, day in enumerate(week):
                cell = tk.Frame(self.canvas, bg=GRID_BG, highlightthickness=1, highlightbackground=GRID_LINE)
                cell.grid(row=r, column=c, sticky="nsew")

                day_fg = "#9aa3b2" if day.month != month else DAY_TEXT
                day_lbl = tk.Label(cell, text=str(day.day), bg=GRID_BG, fg=day_fg, font=("Arial", 9, "bold"))
                day_lbl.place(x=8, y=6)

                val_lbl = tk.Label(cell, text="", bg=GRID_BG, fg=VAL_TEXT, font=("Arial", 13, "bold"))
                val_lbl.place(relx=0.5, rely=0.5, anchor="center")


                if day.month == month:
                    saved = month_data.get(str(day.day))
                    v = None
                    if saved is not None:
                        try: v = float(saved)
                        except Exception: v = None
                    if v is not None:
                        val_lbl.config(text=f"${v:,.2f}")

                    def make_editor(d=day.day):
                        return lambda e=None: self.open_editor(year, month, d)
                    for w in (cell, day_lbl, val_lbl):
                        w.bind("<Button-1>", make_editor())

                    self.cells[(year, month, day.day)] = {
                        "frame": cell, "day_lbl": day_lbl, "val_lbl": val_lbl, "value": v
                    }

        self.recompute_stats_and_colors()

    # Editing & coloring 
    def open_editor(self, year, month, day):
        cur = self.cells.get((year, month, day), {})
        cur_val = cur.get("value")
        cur_text = "" if cur_val is None else f"{cur_val:g}"

        win = tk.Toplevel(self.root)
        win.title(f"Edit {year}-{month:02d}-{day:02d}")
        win.configure(bg=HEADER_BG)
        win.resizable(False, False)

        ttk.Label(win, text=f"{calendar.month_name[month]} {day}, {year}",
                  style="WBHeader.TLabel", font=("Arial", 11, "bold")).pack(padx=12, pady=(12, 6))

        e = ttk.Entry(win, width=20, justify="center", font=("Arial", 12), style="WB.TEntry")
        e.pack(padx=12, pady=6)
        e.insert(0, cur_text)
        e.focus_set()

        row = ttk.Frame(win, style="WBHeader.TFrame")
        row.pack(pady=12)

        def save_and_close():
            txt = e.get().strip()
            if txt == "":
                self.set_value(year, month, day, None)
                win.destroy(); return
            try:
                num = parse_amount(txt)
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter -125.5, +$100, 1,200 or (250)")
                return
            self.set_value(year, month, day, num)
            win.destroy()

        ttk.Button(row, text="Save",  style="WB.TButton", command=save_and_close).pack(side="left", padx=6)
        ttk.Button(row, text="Clear", style="WB.TButton",
                   command=lambda: (self.set_value(year, month, day, None), win.destroy())).pack(side="left", padx=6)
        ttk.Button(row, text="Cancel", style="WB.TButton", command=win.destroy).pack(side="left", padx=6)
        e.bind("<Return>", lambda _e: save_and_close())

    def set_value(self, y, m, d, val):
        cell = self.cells.get((y, m, d))
        if not cell: return
        cell["value"] = val
        if val is None:
            cell["val_lbl"].config(text="")
        else:
            if val > 0:
                sign = "+"
            elif val < 0:
                sign = "-"
            else:
                sign = ""
            cell["val_lbl"].config(text=f"{sign}${abs(val):,.2f}")

        mkey = self._month_key(y, m)
        self.data.setdefault(mkey, {})
        if val is None:
            self.data[mkey].pop(str(d), None)
            if not self.data[mkey]:
                self.data.pop(mkey, None)
        else:
            self.data[mkey][str(d)] = float(val)

        self._save_data()                # autosave
        self.recompute_stats_and_colors()

    def recompute_stats_and_colors(self):
        vals = [v["value"] for v in self.cells.values() if v["value"] not in (None, 0)]
        vmax = max((abs(v) for v in vals), default=0.0)

        total = 0.0; count = 0; wins = 0
        for data in self.cells.values():
            val = data["value"]
            bg = GRID_BG
            if val is not None:
                if val != 0: bg = heat_color(val, vmax)
                total += val; count += 1
                if val > 0: wins += 1
            for w in (data["frame"], data["day_lbl"], data["val_lbl"]):
                w.configure(bg=bg)
            data["frame"].configure(highlightbackground=GRID_LINE)
            data["val_lbl"].configure(fg=VAL_TEXT)

        avg = (total / count) if count else 0.0
        win_rate = (wins / count * 100.0) if count else 0.0
        total_color = rgb_to_hex(POS_PEAK if total > 0 else NEG_PEAK) if total != 0 else "#eef2f7"
        self.total_val.config(text=f"${total:,.2f}", foreground=total_color)
        self.avg_val.config(text=f"${avg:,.2f}")
        self.win_val.config(text=f"{win_rate:.1f}%")

    def clear_month(self):
        if not messagebox.askyesno("Clear", "Clear all entries for this month?"):
            return
        y, m = int(self.cur_year.get()), int(self.cur_month.get())
        for (yy, mm, _), data in list(self.cells.items()):
            if yy == y and mm == m:
                data["value"] = None
                data["val_lbl"].config(text="")
                data["frame"].configure(bg=GRID_BG, highlightbackground=GRID_LINE)
                data["day_lbl"].configure(bg=GRID_BG)
                data["val_lbl"].configure(bg=GRID_BG, fg=VAL_TEXT)
        self.data.pop(self._month_key(y, m), None)
        self._save_data()
        self.recompute_stats_and_colors()

    # CSV import/export
    def save_csv(self):
        y, m = int(self.cur_year.get()), int(self.cur_month.get())
        fname = filedialog.asksaveasfilename(defaultextension=".csv",
                    initialfile=f"pnl_{y}_{m:02d}.csv",
                    filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if not fname: return
        try:
            with open(fname, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(["year", "month", "day", "value"])
                month_data = self.data.get(self._month_key(y, m), {})
                for d in range(1, 32):
                    v = month_data.get(str(d))
                    if v is not None: w.writerow([y, m, d, v])
            messagebox.showinfo("Exported", f"Saved to {fname}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export:\n{e}")

    def load_csv(self):
        fname = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if not fname: return
        try:
            rows = []
            with open(fname, "r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    try:
                        y = int(row["year"]); m = int(row["month"]); d = int(row["day"])
                        vtxt = row.get("value", "").strip()
                        v = None if vtxt == "" else parse_amount(vtxt)
                        rows.append((y, m, d, v))
                    except Exception:
                        continue
            if not rows:
                messagebox.showwarning("No Data", "CSV contained no readable rows."); return
            for y, m, d, v in rows:
                mkey = self._month_key(y, m)
                self.data.setdefault(mkey, {})
                if v is None: self.data[mkey].pop(str(d), None)
                else: self.data[mkey][str(d)] = float(v)
            self._save_data()
            y0, m0, *_ = rows[0]
            self.cur_year.set(y0); self.cur_month.set(m0); self.refresh()
            messagebox.showinfo("Imported", f"Loaded {fname}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import:\n{e}")

def main():
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = PnLCalendar(root)
    root.minsize(760, 520)
    root.mainloop()

if __name__ == "__main__":
    main()
