
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import re
import math

class WordCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Counter - Phase 3")
        self.root.geometry("760x720")
        self.root.configure(bg="#edf2f7")

        tk.Label(root, text="WORD COUNTER",
                 font=("Arial", 20, "bold"),
                 bg="#edf2f7", fg="#183153").pack(pady=12)

        tk.Label(root, text="Enter or paste your text below:",
                 font=("Arial", 11), bg="#edf2f7").pack()

        self.text = tk.Text(root, height=12, width=82, wrap="word")
        self.text.pack(padx=15, pady=8)

        buttons = tk.Frame(root, bg="#edf2f7")
        buttons.pack(pady=5)

        tk.Button(buttons, text="Analyze Text",
                  command=self.analyze,
                  bg="#2563eb", fg="white", width=15).grid(row=0, column=0, padx=4)

        tk.Button(buttons, text="Open Text File",
                  command=self.open_file, width=15).grid(row=0, column=1, padx=4)

        tk.Button(buttons, text="Save Report",
                  command=self.save_report, width=15).grid(row=0, column=2, padx=4)

        tk.Button(buttons, text="Clear",
                  command=self.clear, width=12).grid(row=0, column=3, padx=4)

        tk.Label(root, text="Analysis Results",
                 font=("Arial", 13, "bold"),
                 bg="#edf2f7").pack(pady=(10, 3))

        self.output = tk.Text(root, height=15, width=82, wrap="word")
        self.output.pack(padx=15, pady=8)

        self.report = ""

    def analyze(self):
        text = self.text.get("1.0", "end-1c")

        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        words = re.findall(r"\b[\w']+\b", text.lower(), flags=re.UNICODE)
        characters = len(text)
        characters_without_spaces = sum(not c.isspace() for c in text)
        sentences = len(re.findall(r'[.!?]+', text))
        paragraphs = len([p for p in text.splitlines() if p.strip()])
        unique_words = len(set(words))
        frequency = Counter(words)
        reading_time = max(1, math.ceil(len(words) / 200))

        repeated = {
            word: count for word, count in frequency.most_common()
            if count > 1
        }

        lines = [
            "WORD COUNTER REPORT",
            "=" * 35,
            f"Total Words: {len(words)}",
            f"Total Characters: {characters}",
            f"Characters Without Spaces: {characters_without_spaces}",
            f"Total Sentences: {sentences}",
            f"Total Paragraphs: {paragraphs}",
            f"Unique Words: {unique_words}",
            f"Estimated Reading Time: {reading_time} minute(s)",
            "",
            "MOST FREQUENT WORDS",
            "-" * 35
        ]

        if frequency:
            for word, count in frequency.most_common(10):
                lines.append(f"{word}: {count}")

        lines.extend(["", "REPEATED WORDS", "-" * 35])

        if repeated:
            for word, count in repeated.items():
                lines.append(f"{word}: {count}")
        else:
            lines.append("No repeated words.")

        self.report = "\n".join(lines)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.report)

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.analyze()
        except (OSError, UnicodeError) as error:
            messagebox.showerror("File Error", str(error))

    def save_report(self):
        if not self.report:
            messagebox.showwarning("Warning", "Analyze text first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.report)

            messagebox.showinfo("Success", "Report saved successfully.")
        except OSError as error:
            messagebox.showerror("File Error", str(error))

    def clear(self):
        self.text.delete("1.0", tk.END)
        self.output.delete("1.0", tk.END)
        self.report = ""

root = tk.Tk()
app = WordCounter(root)
root.mainloop()
