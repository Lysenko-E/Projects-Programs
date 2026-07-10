import tkinter as tk
import random
import re

# --- Safe Tooltip class ---
class ToolTip:
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.active = True  # tooltips enabled by default

        widget.bind("<Enter>", self.schedule_show)
        widget.bind("<Leave>", self.hide_tip)

    def schedule_show(self, event=None):
        if self.active:
            self.widget.after(300, self.show_tip)

    def show_tip(self, event=None):
        if not self.active or self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            font=("Arial", 10)
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


# --- Load grammar list ---
def load_grammar(filepath):
    grammar_items = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 3:
                grammar_items.append({
                    'pattern': parts[0].strip(),
                    'meaning': parts[1].strip(),
                    'nuance': parts[2].strip(),
                    'jp_example': parts[3].strip() if len(parts) > 3 else '',
                    'en_example': parts[4].strip() if len(parts) > 4 else ''
                })
    return grammar_items


# --- Load sentences ---
def load_sentences(filepath):
    sentences = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 2:
                sentences.append({'sentence': parts[0].strip(), 'correct': parts[1].strip()})
    return sentences


# --- Find grammar item ---
def find_grammar(grammar_items, pattern):
    for g in grammar_items:
        if g['pattern'] == pattern:
            return g
    return None


# --- Grammar Quiz Class ---
class GrammarQuiz:
    def __init__(self, root, grammar_items, sentences):
        self.root = root
        self.grammar_items = grammar_items
        self.sentences = sentences
        self.index = 0
        self.score = 0
        self.correct_item = None
        self.hint_visible = False

        self.setup_ui()
        self.next_question()

    def setup_ui(self):
        self.root.title("JLPT Grammar Quiz")
        self.root.geometry("750x600")
        self.root.configure(bg="#f9f9f9")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        main_frame = tk.Frame(self.root, bg="#f9f9f9")
        main_frame.grid(sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        tk.Label(main_frame, text="Grammar Quiz", font=("Arial", 20, "bold"), bg="#f9f9f9").pack(pady=10)

        tk.Button(main_frame, text="Shuffle Sentences 🔀", font=("Arial", 12),
                  bg="#d0e0ff", command=self.shuffle_sentences).pack(pady=5)

        self.counter_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#f9f9f9")
        self.counter_label.pack()

        self.question_label = tk.Label(main_frame, text="", font=("Arial", 17),
                                       wraplength=700, bg="#f9f9f9", justify="left")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        self.tooltips = []

        for i in range(4):
            frame = tk.Frame(main_frame, bg="#f9f9f9")
            frame.pack(pady=5, fill="x")

            btn = tk.Button(frame, text="", font=("Arial", 14),
                            bg="#e0e0e0", relief="flat")
            btn.pack(side="left", padx=10, fill="x", expand=True)
            btn.config(command=lambda i=i: self.check_answer(i))
            self.option_buttons.append(btn)

            info = tk.Label(frame, text="ℹ", font=("Arial", 14), bg="#f9f9f9")
            info.pack(side="right", padx=10)

            tooltip = ToolTip(info, "")
            self.tooltips.append(tooltip)

        self.feedback_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="#f9f9f9")
        self.feedback_label.pack(pady=10)

        self.hint_button = tk.Button(main_frame, text="Show hint ▼", font=("Arial", 12),
                                     bg="#f0f0f0", command=self.toggle_hint)
        self.hint_button.pack(pady=5)

        self.hint_text = tk.Label(main_frame, text="", font=("Arial", 12),
                                  wraplength=700, justify="left", bg="#f9f9f9")
        self.hint_text.pack(pady=5)

        self.restart_button = tk.Button(main_frame, text="Restart Quiz 🔁", font=("Arial", 12),
                                        bg="#d0ffd0", command=self.restart_quiz)
        self.restart_button.pack(pady=10)

    def shuffle_sentences(self):
        random.shuffle(self.sentences)
        self.index = 0
        self.score = 0
        self.feedback_label.config(text="")
        self.hint_text.config(text="")
        self.hint_button.config(text="Show hint ▼")
        self.hint_visible = False
        self.next_question()

    def restart_quiz(self):
        self.index = 0
        self.score = 0
        random.shuffle(self.sentences)
        self.feedback_label.config(text="")
        self.hint_text.config(text="")
        self.hint_button.config(text="Show hint ▼")
        self.hint_visible = False
        self.next_question()

    def next_question(self):
        if self.index >= len(self.sentences):
            self.feedback_label.config(text=f"Quiz Finished! Score: {self.score}/{len(self.sentences)}", fg="blue")
            self.root.after(1500, self.restart_quiz)
            return

        data = self.sentences[self.index]
        sentence = data['sentence']
        correct_pattern = data['correct']

        self.correct_item = find_grammar(self.grammar_items, correct_pattern)

        # Safety: handle missing grammar entries gracefully
        if self.correct_item is None:
            self.feedback_label.config(
                text=f"⚠ データエラー: 文法「{correct_pattern}」がGrammar Listに見つかりません。",
                fg="red"
            )
            self.index += 1
            self.root.after(1500, self.next_question)
            return

        other_items = [g for g in self.grammar_items if g['pattern'] != correct_pattern]
        options = random.sample(other_items, 3) + [self.correct_item]
        random.shuffle(options)

        # Replace grammar slot with blank
        blanked_sentence = re.sub(r'～[^\s]*', "＿＿＿", sentence)

        self.question_label.config(text=f"{blanked_sentence}\n\n正しい文法はどれ？")
        self.counter_label.config(text=f"Score: {self.score}/{len(self.sentences)}")

        # Update option buttons + tooltips
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i]['pattern'])
            self.tooltips[i].text = f"{options[i]['pattern']} — {options[i]['meaning']}"

        # Reset feedback + hint
        self.feedback_label.config(text="")
        self.hint_text.config(text="")
        self.hint_button.config(text="Show hint ▼")
        self.hint_visible = False

        self.index += 1

    def check_answer(self, i):
        chosen = self.option_buttons[i].cget("text")

        if chosen == self.correct_item['pattern']:
            self.feedback_label.config(text="✅ 正解！", fg="green")
            self.score += 1
            self.root.after(1000, self.next_question)
        else:
            self.feedback_label.config(
                text=f"❌ 不正解。正しい答え: {self.correct_item['pattern']}",
                fg="red"
            )
            self.root.after(1500, self.next_question)

    def toggle_hint(self):
        # Disable tooltips while hint is open
        for tooltip in self.tooltips:
            tooltip.active = False

        if not self.hint_visible:
            hint = (
                f"{self.correct_item['pattern']} — {self.correct_item['meaning']}\n"
                f"Nuance: {self.correct_item['nuance']}\n"
                f"例文: {self.correct_item['jp_example']}\n"
                f"EN: {self.correct_item['en_example']}"
            )
            self.hint_text.config(text=hint)
            self.hint_button.config(text="Hide hint ▲")
            self.hint_visible = True
        else:
            self.hint_text.config(text="")
            self.hint_button.config(text="Show hint ▼")
            self.hint_visible = False

        # Re-enable tooltips
        for tooltip in self.tooltips:
            tooltip.active = True


# --- Run ---
if __name__ == "__main__":
    grammar_items = load_grammar(r"C:\Users\dmitr\Desktop\JLPT+Program\2026\Grammar List.txt")
    sentences = load_sentences(r"C:\Users\dmitr\Desktop\JLPT+Program\grammar program\sentences.txt")
    random.shuffle(sentences)

    root = tk.Tk()
    app = GrammarQuiz(root, grammar_items, sentences)
    root.mainloop()
