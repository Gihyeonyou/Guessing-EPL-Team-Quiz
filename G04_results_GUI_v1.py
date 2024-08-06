import tkinter as tk


class DisplayResults:
    def __init__(self, partner):
        self.parent = tk.Toplevel()
        self.parent.title("Quiz Results")

        self.right_count = 0
        self.wrong_count = 0

        self.right_var = tk.StringVar()
        self.wrong_var = tk.StringVar()
        self.comment_var = tk.StringVar()

        self.create_widgets()
        self.update_results()

    def create_widgets(self):
        results_label = tk.Label(self.parent, text="Results", font=("Arial", 20))
        results_label.pack(pady=10)

        instruction_label = tk.Label(self.parent, text="Here are your game results", font=("Arial", 16))
        instruction_label.pack(pady=10)

        right_frame = tk.Frame(self.parent)
        right_frame.pack(pady=5)
        right_label = tk.Label(right_frame, text="Right", font=("Arial", 15))
        right_label.pack(side="left", padx=5)
        self.right_entry = tk.Entry(right_frame, textvariable=self.right_var, width=30, state='readonly')
        self.right_entry.pack(side="left")

        wrong_frame = tk.Frame(self.parent)
        wrong_frame.pack(pady=5)
        wrong_label = tk.Label(wrong_frame, text="Wrong", font=("Arial", 15))
        wrong_label.pack(side="left", padx=5)
        self.wrong_entry = tk.Entry(wrong_frame, textvariable=self.wrong_var, width=30, state='readonly')
        self.wrong_entry.pack(side="left")

        comment_frame = tk.Frame(self.parent)
        comment_frame.pack(pady=5)
        comment_label = tk.Label(comment_frame, text="Comment", font=("Arial", 15))
        comment_label.pack(side="left", padx=5)
        self.comment_entry = tk.Entry(comment_frame, textvariable=self.comment_var, width=30, state='readonly')
        self.comment_entry.pack(side="left")

        # Specify the button background color using hexadecimal code
        dismiss_button = tk.Button(self.parent, text="Dismiss", bg="#FFFF00", command=self.dismiss)
        dismiss_button.pack(pady=10, padx=50, ipadx=50)

    def set_results(self, right, wrong, comment):
        self.right_var.set(right)
        self.wrong_var.set(wrong)
        self.comment_var.set(comment)

    def update_results(self):
        comment = self.generate_comment()
        self.set_results(str(self.right_count), str(self.wrong_count), comment)

    def generate_comment(self):
        if self.right_count > self.wrong_count:
            return "Good job!"
        elif self.right_count == self.wrong_count:
            return "Nice effort!"
        else:
            return "Keep trying!"

    def increment_right(self):
        self.right_count += 1
        self.update_results()

    def increment_wrong(self):
        self.wrong_count += 1
        self.update_results()

    def dismiss(self):
        self.parent.destroy()