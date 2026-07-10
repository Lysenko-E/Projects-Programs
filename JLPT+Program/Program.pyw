import tkinter as tk
from tkinter import ttk
import random
import os

VERB_FILE = r"C:\Users\dmitr\Desktop\JLPT+Program\n1_verbs.txt"
WORD_FILE = r"C:\Users\dmitr\Desktop\JLPT+Program\n1_words.txt"
WHITEBOARD_FILE = r"C:\Users\dmitr\Desktop\JLPT+Program\whiteboard.txt"
STUDIED_ROOT = r"C:\Users\dmitr\Desktop\JLPT+Program\2026"


# ---------------- HELPERS ---------------- #

def load_cards(path):
    cards = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 5:
                memo_raw = parts[6] if len(parts) >= 7 else ""
                memo_fixed = memo_raw.replace(" ⏎ ", "\n")
                similar = parts[7] if len(parts) >= 8 else ""
                cards.append({
                    "front": parts[0],
                    "meaning": parts[1],
                    "readings": parts[2],
                    "jp_ex": parts[3],
                    "en_ex": parts[4],
                    "collocations": parts[5] if len(parts) >= 6 else "",
                    "memo": memo_fixed,
                    "similar": similar
                })
    return cards


def load_simple_list(path):
    cards = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                cards.append({
                    "front": word,
                    "meaning": "",
                    "readings": "",
                    "jp_ex": "",
                    "en_ex": "",
                    "collocations": "",
                    "memo": "",
                    "similar": ""
                })
    return cards


def detect_loader(path):
    with open(path, encoding="utf-8") as f:
        first = f.readline()
        if "|" in first:
            return load_cards
        return load_simple_list


# ---------------- APP ---------------- #

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JLPT Study App")
        self.geometry("1100x850")
        self.minsize(900, 700)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 14), padding=8)
        style.configure("TLabel", font=("Segoe UI", 16))
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"))

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, FileSelect, Flashcards):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(MainMenu)

    def show(self, frame_class, **kwargs):
        frame = self.frames[frame_class]
        if hasattr(frame, "load"):
            frame.load(**kwargs)
        frame.tkraise()


# ---------------- MAIN MENU ---------------- #

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        wrapper = ttk.Frame(self, padding=40)
        wrapper.pack(expand=True)

        ttk.Label(wrapper, text="JLPT Study App", style="Title.TLabel").pack(pady=(0, 30))

        ttk.Button(wrapper, text="Verbs",
                   command=lambda: controller.show(Flashcards, path=VERB_FILE)).pack(pady=10, fill="x")
        ttk.Button(wrapper, text="Words",
                   command=lambda: controller.show(Flashcards, path=WORD_FILE)).pack(pady=10, fill="x")
        ttk.Button(wrapper, text="Studied Material",
                   command=lambda: controller.show(FileSelect)).pack(pady=10, fill="x")


# ---------------- FILE SELECT ---------------- #

class FileSelect(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Layout: 70% left, 30% right
        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        # --- Top bar ---
        top = ttk.Frame(self, padding=(20, 10))
        top.grid(row=0, column=0, columnspan=2, sticky="ew")
        top.columnconfigure(0, weight=1)

        ttk.Label(top, text="Studied Material", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Main Menu",
                   command=lambda: controller.show(MainMenu)).grid(row=0, column=1, sticky="e")

        # --- Left: scrollable file list ---
        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=(40, 10), pady=20)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner = ttk.Frame(self.canvas)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # --- Right: whiteboard ---
        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 40), pady=20)

        ttk.Label(right_frame, text="Whiteboard", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 5))

        self.whiteboard = tk.Text(right_frame, font=("Segoe UI", 13), wrap="word",
                                  bg="#ffffff", relief="solid", bd=1)
        self.whiteboard.pack(fill="both", expand=True)

        # Load saved text
        if os.path.exists(WHITEBOARD_FILE):
            with open(WHITEBOARD_FILE, "r", encoding="utf-8") as f:
                self.whiteboard.insert("1.0", f.read())

        # Auto-save
        def save_whiteboard(event=None):
            text = self.whiteboard.get("1.0", "end-1c")
            with open(WHITEBOARD_FILE, "w", encoding="utf-8") as f:
                f.write(text)

        self.whiteboard.bind("<KeyRelease>", save_whiteboard)

    def _on_inner_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.inner_id, width=event.width)

    def load(self):
        for w in self.inner.winfo_children():
            w.destroy()

        if not os.path.isdir(STUDIED_ROOT):
            return

        files = [f for f in os.listdir(STUDIED_ROOT) if f.endswith(".txt")]
        files = sorted(files, key=self._extract_date)

        current_month = None
        for fname in files:
            month = self._extract_month(fname)
            if month and month != current_month:
                current_month = month
                ttk.Label(self.inner, text=month,
                          font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(10, 0))

            full_path = os.path.join(STUDIED_ROOT, fname)
            btn = ttk.Button(self.inner, text=f"📘 {fname}", width=40,
                             command=lambda p=full_path: self.controller.show(Flashcards, path=p))
            btn.pack(anchor="w", pady=3)

    def _extract_month(self, fname):
        import re
        m = re.match(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", fname)
        return m.group(1) if m else None

    def _extract_date(self, fname):
        import re
        m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d+)", fname)
        if m:
            month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(m.group(1))
            day = int(m.group(2))
            return month * 100 + day
        return 9999


# ---------------- FLASHCARDS ---------------- #

class Flashcards(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.path = None
        self.cards = []
        self.queue = []
        self.current = None
        self.showing_back = False

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Top bar
        top_bar = ttk.Frame(self)
        top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        top_bar.columnconfigure(0, weight=1)

        ttk.Button(top_bar, text="Main Menu",
                   command=lambda: controller.show(MainMenu)).grid(row=0, column=0, sticky="w")

        self.counter_label = ttk.Label(top_bar, text="")
        self.counter_label.grid(row=0, column=1, sticky="e")

        # Card area
        card_area = ttk.Frame(self)
        card_area.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        card_area.rowconfigure(0, weight=1)
        card_area.columnconfigure(0, weight=1)

        self.front_label = ttk.Label(card_area, text="", font=("Segoe UI", 40),
                                     wraplength=900, anchor="center", justify="center")
        self.front_label.grid(row=0, column=0, sticky="nsew")

        self.back_text = tk.Text(card_area, font=("Segoe UI", 16),
                                 wrap="word", height=18, width=60, borderwidth=0)
        self.back_text.configure(state="disabled")

        # Bottom controls
        bottom = ttk.Frame(self)
        bottom.grid(row=2, column=0, pady=20)

        self.flip_btn = ttk.Button(bottom, text="Flip", command=self.flip)
        self.flip_btn.grid(row=0, column=0, padx=20)

        self.good_btn = ttk.Button(bottom, text="Good", command=self.good)
        self.good_btn.grid(row=0, column=1, padx=20)

        self.no_btn = ttk.Button(bottom, text="Again", command=self.no)
        self.no_btn.grid(row=0, column=2, padx=20)

        self.memo_btn = ttk.Button(bottom, text="Memo", command=self.open_memo_popup)
        self.memo_btn.grid(row=0, column=3, padx=20)

    def load(self, path):
        self.path = path
        loader = detect_loader(path)
        self.cards = loader(path)

        self.queue = self.cards.copy()
        random.shuffle(self.queue)

        self.processed = 0
        self.workload = len(self.cards)

        self.next_card()

    def update_counter(self):
        self.counter_label.config(text=f"{self.processed} / {self.workload}")

    def show_front(self):
        self.back_text.grid_forget()
        self.front_label.grid(row=0, column=0, sticky="nsew")

    def show_back(self):
        self.front_label.grid_forget()
        self.back_text.grid(row=0, column=0, sticky="nsew")

    def render_back(self):
        c = self.current

        self.back_text.config(state="normal")
        self.back_text.delete("1.0", "end")

        def add(label, value):
            if value:
                self.back_text.insert("end", f"{label}:\n{value}\n\n")

        add("Meaning", c["meaning"])
        add("Readings", c["readings"])
        add("JP Example", c["jp_ex"])
        add("EN Example", c["en_ex"])
        add("Collocations", c["collocations"])
        add("Similar Kanji", c["similar"])
        add("Memo", c["memo"])

        if self.back_text.get("1.0", "end-1c").strip() == "":
            self.back_text.insert("end", "(No details available)\n")

        self.back_text.config(state="disabled")

    def next_card(self):
        if not self.queue:
            self.current = None
            self.front_label.config(text="All done!")
            self.show_front()
            self.update_counter()
            return

        self.current = self.queue.pop(0)
        self.showing_back = False
        self.front_label.config(text=self.current["front"])
        self.update_counter()
        self.show_front()

    def flip(self):
        if not self.current:
            return
        if self.showing_back:
            self.showing_back = False
            self.show_front()
        else:
            self.showing_back = True
            self.render_back()
            self.show_back()

    def good(self):
        if not self.current:
            return
        self.processed += 1
        self.next_card()

    def no(self):
        if not self.current:
            return
        delay = random.randint(1, 10)
        pos = min(len(self.queue), delay)
        self.queue.insert(pos, self.current)
        self.processed += 1
        self.workload += 1
        self.next_card()

    # -------- MEMO SYSTEM (PER-CARD) -------- #

    def open_memo_popup(self):
        if not self.current or not self.path:
            return

        popup = tk.Toplevel(self)
        popup.title("Edit Memo")
        popup.geometry("600x400")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.configure(bg="#f0f0f0")

        frame = ttk.Frame(popup, padding=20)
        frame.pack(fill="both", expand=True)

        label = ttk.Label(frame, text=f"Memo for: {self.current['front']}", font=("Segoe UI", 14))
        label.pack(anchor="w", pady=(0, 10))

        text_frame = ttk.Frame(frame)
        text_frame.pack(fill="both", expand=True)

        memo_text = tk.Text(text_frame, font=("Segoe UI", 13), wrap="word",
                            bg="#ffffff", relief="solid", bd=1)
        memo_text.pack(fill="both", expand=True)

        memo_text.insert("1.0", self.current.get("memo", ""))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        def save_and_close():
            new_memo = memo_text.get("1.0", "end-1c")
            self.current["memo"] = new_memo
            self.save_memos_to_file()
            if self.showing_back:
                self.render_back()
            popup.destroy()

        def cancel():
            popup.destroy()

        save_btn = ttk.Button(btn_frame, text="Save", command=save_and_close)
        save_btn.pack(side="right", padx=(5, 0))

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=cancel)
        cancel_btn.pack(side="right", padx=(0, 5))

        popup.bind("<Control-s>", lambda e: (save_and_close(), "break"))
        memo_text.focus_set()

    def save_memos_to_file(self):
        if not self.path or not self.cards:
            return

        lines = []
        for c in self.cards:
            front = c.get("front", "")
            meaning = c.get("meaning", "")
            readings = c.get("readings", "")
            jp_ex = c.get("jp_ex", "")
            en_ex = c.get("en_ex", "")
            collocations = c.get("collocations", "")
            memo = c.get("memo", "") or ""
            similar = c.get("similar", "") or ""

            memo_encoded = memo.replace("\n", " ⏎ ")

            parts = [
                front,
                meaning,
                readings,
                jp_ex,
                en_ex,
                collocations,
                memo_encoded,
                similar
            ]
            line = " | ".join(parts)
            lines.append(line)

        with open(self.path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")


# ---------------- START ---------------- #

if __name__ == "__main__":
    App().mainloop()
