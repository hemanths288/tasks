import tkinter as tk
from tkinter import messagebox, filedialog
from zxcvbn import zxcvbn
import itertools

class PasswordToolApp:
    def __init__(self, root):
        self.root = root
        root.title("Password Tool")
        root.geometry("600x550")

        # Password Analyzer Section
        tk.Label(root, text="🔐 Enter Password:").pack()
        self.password_entry = tk.Entry(root, width=40, show='*')
        self.password_entry.pack()
        tk.Button(root, text="Analyze Strength", command=self.analyze_password).pack(pady=5)

        self.result_box = tk.Text(root, height=8, width=70)
        self.result_box.pack()

        # Wordlist Generator Section
        tk.Label(root, text="📚 Wordlist Generator", font=('Arial', 12, 'bold')).pack(pady=10)

        self.name_entry = self.__make__labeled__input("Name:")
        self.birth_entry = self.__make__labeled__input("Birth Year:")
        self.pet_entry = self.__make__labeled__input("Pet Name:")
        self.fav_entry = self.__make__labeled__input("Favorite Word (optional):")

        tk.Button(root, text="Generate Wordlist", command=self.generate_wordlist).pack(pady=10)

    def __make__labeled__input(self, label):
        tk.Label(self.root, text=label).pack()
        entry = tk.Entry(self.root, width=40)
        entry.pack()
        return entry

    def analyze_password(self):
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return

        try:
            result = zxcvbn(password)
            self.result_box.delete('1.0', tk.END)
            self.result_box.insert(tk.END, f"Score: {result['score']} / 4\n")
            self.result_box.insert(tk.END, f"Guesses: {result['guesses']}\n")
            crack_time = result['crack_times_display'].get('offline_fast_hashing_1e10_per_second', 'N/A')
            self.result_box.insert(tk.END, f"Crack Time: {crack_time}\n")
            feedback = result['feedback']['warning'] or "No major issues."
            self.result_box.insert(tk.END, f"Feedback: {feedback}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_wordlist(self):
        # Collect inputs
        name = self.name_entry.get().strip().lower()
        birth = self.birth_entry.get().strip()
        pet = self.pet_entry.get().strip().lower()
        fav = self.fav_entry.get().strip().lower()

        if not name and not birth and not pet and not fav:
            messagebox.showwarning("Input Error", "Enter at least one field.")
            return

        base_words = list(filter(None, [name, birth, pet, fav]))
        suffixes = ['', '123', '!', '@', '2024', '2025']
        leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}

        def leetspeak(word):
            return ''.join(leet_map.get(c, c) for c in word)

        wordlist = set()

        for word in base_words:
            variations = [
                word,
                word.capitalize(),
                word.upper(),
                leetspeak(word),
                leetspeak(word).capitalize()
            ]
            for v in variations:
                for s in suffixes:
                    wordlist.add(v + s)

        # Combine two words too
        combos = list(itertools.combinations(base_words, 2))
        for a, b in combos:
            combined = [a + b, b + a]
            for c in combined:
                for s in suffixes:
                    wordlist.add(c + s)

        # Export
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'w') as f:
                for word in sorted(wordlist):
                    f.write(word + '\n')
            messagebox.showinfo("Success", f"Wordlist saved to:\n{filepath}")
        else:
            messagebox.showinfo("Cancelled", "No file saved.")
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordToolApp(root)
    root.mainloop()