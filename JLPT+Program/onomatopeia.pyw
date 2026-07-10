import tkinter as tk
import random

# File paths
ADVERB_FILE = r"C:\Users\dmitr\Desktop\JLPT+Program\2026\Jun-8 Adverbs.txt"
SENTENCE_FILE = r"C:\Users\dmitr\Desktop\JLPT+Program\sentences.txt"

# Extract ONLY the first column (the adverb itself)
def load_adverbs():
    adverbs = []
    with open(ADVERB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                first_column = line.split("|")[0].strip()
                if first_column:
                    adverbs.append(first_column)
    return adverbs

# Load sentences from external file
# Format: sentence_with_blank|correct_answer
def load_sentences():
    sentences = []
    with open(SENTENCE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                jp, correct = line.split("|")
                sentences.append((jp.strip(), correct.strip()))
    return sentences

ADVERBS = load_adverbs()
SENTENCES = load_sentences()

class QuizApp:
    def __init__(self, root):
        self.root = root
        root.title("JLPT Adverb Trainer")

        self.question_label = tk.Label(root, text="", font=("Meiryo", 20))
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Meiryo", 16),
                            width=20, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.feedback_label = tk.Label(root, text="", font=("Meiryo", 20))
        self.feedback_label.pack(pady=20)

        self.next_question()

    def next_question(self):
        self.feedback_label.config(text="")

        # Pick a random sentence
        self.sentence, self.correct = random.choice(SENTENCES)

        # Pick 3 wrong answers
        wrong = random.sample([w for w in ADVERBS if w != self.correct], 3)

        # Shuffle answer options
        self.options = [self.correct] + wrong
        random.shuffle(self.options)

        # Update GUI
        self.question_label.config(text=self.sentence)
        for i, opt in enumerate(self.options):
            self.buttons[i].config(text=opt)

    def check_answer(self, index):
        chosen = self.options[index]
        if chosen == self.correct:
            self.feedback_label.config(text="⭕ 正解！", fg="green")
            self.root.after(1000, self.next_question)
        else:
            self.feedback_label.config(text="❌ 不正解", fg="red")

root = tk.Tk()
app = QuizApp(root)
root.mainloop()
