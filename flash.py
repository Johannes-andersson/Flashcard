import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os

FLASHCARD_DIR = "flashcards"

if not os.path.exists(FLASHCARD_DIR):
    os.makedirs(FLASHCARD_DIR)

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard App")
        self.geometry("400x300")
        
        self.set_name = tk.StringVar()
        self.load_sets()
        
        self.create_widgets()

    def create_widgets(self):
        # Dropdown for sets
        tk.Label(self, text="Select Set:").pack(pady=5)
        self.set_dropdown = tk.OptionMenu(self, self.set_name, *self.sets)
        self.set_dropdown.pack(pady=5)

        # Buttons
        tk.Button(self, text="Add New Card", command=self.add_card).pack(pady=5)
        tk.Button(self, text="Review Cards", command=self.review).pack(pady=5)
        tk.Button(self, text="Delete Card", command=self.delete_card).pack(pady=5)
        tk.Button(self, text="Create New Set", command=self.create_new_set).pack(pady=5)

    def load_sets(self):
        self.sets = [f.replace('.txt', '') for f in os.listdir(FLASHCARD_DIR) if f.endswith('.txt')]
        if not self.sets:
            self.sets = ["Create a new set"]
            self.set_name.set("Create a new set")

    def reload_sets(self):
        self.load_sets()
        menu = self.set_dropdown["menu"]
        menu.delete(0, "end")
        for string in self.sets:
            menu.add_command(label=string, command=lambda value=string: self.set_name.set(value))

    def load_flashcards(self):
        filename = os.path.join(FLASHCARD_DIR, f"{self.set_name.get()}.txt")
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip().split('|') for line in file if line.strip()]

    def save_flashcards(self, cards):
        filename = os.path.join(FLASHCARD_DIR, f"{self.set_name.get()}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            for question, answer in cards:
                file.write(f"{question}|{answer}\n")

    def add_card(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        if question:
            answer = simpledialog.askstring("Input", "Enter the answer:")
            if answer:
                cards = self.load_flashcards()
                cards.append([question, answer])
                self.save_flashcards(cards)
                messagebox.showinfo("Success", "Card added!")

    def review(self):
        cards = self.load_flashcards()
        if not cards:
            messagebox.showinfo("Info", "No cards in this set.")
            return

        self.review_window = tk.Toplevel(self)
        self.review_window.title("Review Flashcards")

        frame = tk.Frame(self.review_window)
        frame.pack(padx=10, pady=10)

        self.current_card = 0
        self.showing_answer = False
        self.question_var = tk.StringVar()
        self.answer_var = tk.StringVar()

        tk.Label(frame, text="Question:").pack()
        tk.Label(frame, textvariable=self.question_var).pack()

        tk.Label(frame, text="Answer:").pack()
        self.answer_label = tk.Label(frame, textvariable=self.answer_var)
        self.answer_label.pack()

        self.show_card()

        tk.Button(self.review_window, text="Prev", command=self.prev_card).pack(side=tk.LEFT)
        tk.Button(self.review_window, text="Next", command=self.next_card).pack(side=tk.RIGHT)

    def show_card(self):
        cards = self.load_flashcards()
        if 0 <= self.current_card < len(cards):
            question, answer = cards[self.current_card]
            self.question_var.set(question)
            if self.showing_answer:
                self.answer_var.set(answer)
            else:
                self.answer_var.set("")
        else:
            self.question_var.set("No more cards.")
            self.answer_var.set("")

    def next_card(self):
        if not self.showing_answer:
            self.showing_answer = True
        else:
            if self.current_card < len(self.load_flashcards()) - 1:
                self.current_card += 1
                self.showing_answer = False
            else:
                messagebox.showinfo("Info", "End of cards.")
        self.show_card()

    def prev_card(self):
        if self.showing_answer:
            self.showing_answer = False
        else:
            if self.current_card > 0:
                self.current_card -= 1
                self.showing_answer = False
            else:
                messagebox.showinfo("Info", "Start of cards.")
        self.show_card()

    def delete_card(self):
        cards = self.load_flashcards()
        if not cards:
            messagebox.showinfo("Info", "No cards to delete.")
            return

        card_to_delete = simpledialog.askinteger("Delete", "Enter the number of the card to delete (1 to {0}):".format(len(cards)))
        if card_to_delete and 1 <= card_to_delete <= len(cards):
            del cards[card_to_delete - 1]
            self.save_flashcards(cards)
            messagebox.showinfo("Success", "Card deleted!")

    def create_new_set(self):
        new_set = simpledialog.askstring("New Set", "Name for the new set:")
        if new_set:
            with open(os.path.join(FLASHCARD_DIR, f"{new_set}.txt"), 'w') as f:
                pass  # Just create the file
            self.reload_sets()
            self.set_name.set(new_set)

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
