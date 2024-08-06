import tkinter as tk
from functools import partial
import csv
import random


class ChooseQuestions:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Guessing EPL Team Quiz")
        self.intro_frame = tk.Frame(self.root, padx=10, pady=10)
        self.intro_frame.grid()
        self.intro_heading_label = tk.Label(self.intro_frame, text="Guessing EPL Team Quiz",
                                            font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0, columnspan=3)

        choose_instructions_txt = "In each question you will be given four different " \
                                  "EPL teams to choose from and they will show the mascot of EPL teams. " \
                                  "Pick a correct team and see if you can get it right or wrong!\n\n" \
                                  "To begin, type the number of questions you'd like to answer"
        self.choose_instructions_label = tk.Label(self.intro_frame,
                                                  text=choose_instructions_txt,
                                                  wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1, columnspan=3)

        # Entry for Typing number of questions
        self.typing_questions_label = tk.Label(self.intro_frame, text="Typing questions:")
        self.typing_questions_label.grid(row=2, column=0, sticky=tk.E, pady=5,
                                         padx=(0, 10))

        self.typing_questions_entry = tk.Entry(self.intro_frame)
        self.typing_questions_entry.grid(row=2, column=1, sticky=tk.W, pady=5,
                                         padx=(0, 10))
        # Submit button for Typing questions
        self.start_button = tk.Button(self.intro_frame, text="Start", command=self.submit_typing_questions,
                                      bg="sky blue",
                                      fg="#FFFFFF",
                                      font=("Arial", "13", "bold"), width=5)
        self.start_button.grid(row=2, column=2, pady=5, padx=(5, 0), sticky=tk.W + tk.E)

        # Error label
        self.error_label = tk.Label(self.intro_frame, text="", fg="red")
        self.error_label.grid(row=3, columnspan=3)

        # Merge the two adjacent columns
        self.intro_frame.grid_columnconfigure(0, weight=1)  # Original column weight for label
        self.intro_frame.grid_columnconfigure(1, weight=2)  # Increased weight for entry

        self.root.mainloop()

    # Checks that users enter a number that is more than 0
    def submit_typing_questions(self):
        num_questions = self.typing_questions_entry.get()
        valid = self.check_input(1)
        if valid == "invalid":
            # Input is invalid
            print("Invalid input")

        # if the number is valid, then shows chosen number of rounds
        else:
            self.root.withdraw()
            results_window = DisplayResults(self.root)
            Answer(int(num_questions), results_window, self.root)

    def check_input(self, num_questions):
        has_error = "no"
        error = "Please enter a number that is more than {}"
        response = self.typing_questions_entry.get()

        try:
            response = int(response)
            if response < num_questions:
                has_error = "yes"
        except ValueError:
            has_error = "yes"

        if has_error == "yes":
            self.error_label.config(text=error.format(num_questions))
            return "invalid"
        else:
            self.error_label.config(text="")
            return "valid"


class Answer:

    def __init__(self, how_many, results_instance, main_window):
        self.button_teams_list = []
        self.correct_answer = []
        self.main_window = main_window
        self.answer_box = tk.Toplevel()
        self.answer_box.protocol('WM_DELETE_WINDOW', self.reset_game)

        self.results_instance = results_instance  # Store instance of DisplayResults

        self.questions_wanted = how_many
        self.questions_answered = 0
        self.questions_won = 0
        self.user_scores = []
        self.all_teams = self.get_all_teams()

        self.quest_frame = tk.Frame(self.answer_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.choose_heading = tk.Label(self.quest_frame, text=f"question 1 of {how_many}",
                                       font=("Arial", "16", "bold"))
        self.choose_heading.grid(row=0)

        self.instructions_label = tk.Label(self.quest_frame, text="What team does this mascot belong to?",
                                           wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        self.choice_frame = tk.Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        self.choice_button_ref = []
        for item in range(0, 4):
            self.choice_button = tk.Button(self.choice_frame, width=21,
                                           command=lambda i=item: self.to_compare(self.choice_button_ref[i]['text']))
            self.choice_button_ref.append(self.choice_button)
            self.choice_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

        self.next_question_button = tk.Button(self.quest_frame, text="Next question",
                                              width=45, pady=4, command=self.new_question)
        self.next_question_button.grid(row=3)

        self.score_label = tk.Label(self.quest_frame, text="Current Score 0 / 0", font=("Arial", "12"))
        self.score_label.grid(row=4, pady=(5, 0))

        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Results", "get results"],
            ["#808080", "Start Over", "start over"]
        ]

        self.control_button_ref = []
        for item in range(0, 3):
            self.make_control_button = tk.Button(self.control_frame, fg="#FFFFFF",
                                                 bg=control_buttons[item][0], text=control_buttons[item][1],
                                                 width=11, font=("Arial", "12", "bold"),
                                                 command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)
            self.control_button_ref.append(self.make_control_button)

        self.to_help_btn = self.control_button_ref[0]
        self.to_results_btn = self.control_button_ref[1]  # Add this line to access Results button

        self.new_question()

    @staticmethod
    def get_all_teams():
        with open("football_players.csv", "r") as file:
            var_all_colors = list(csv.reader(file, delimiter=","))
        var_all_colors.pop(0)  # Remove header row
        return var_all_colors

    def get_question_answers(self):
        question_answers_list = []
        color_scores = []

        while len(question_answers_list) < 4:
            chosen_answers = random.choice(self.all_teams)
            if chosen_answers[1] not in color_scores:
                question_answers_list.append(chosen_answers)
                color_scores.append(chosen_answers[1])

        return question_answers_list

    def new_question(self):
        self.button_teams_list = self.get_question_answers()
        correct_index = random.randint(0, 3)
        self.correct_answer = self.button_teams_list[correct_index][1]
        question_number = self.questions_answered + 1  # Calculate current question number

        # Update the heading label with the correct question number
        self.choose_heading.config(text=f"Question {question_number} of {self.questions_wanted}")

        self.instructions_label.config(
            text=f"What team does the mascot {self.button_teams_list[correct_index][0]} belong to?")
        for idx, button in enumerate(self.choice_button_ref):
            button.config(text=self.button_teams_list[idx][1], state=tk.NORMAL, bg="light grey")

    def to_compare(self, user_choice):
        print(f"User choice: {user_choice}")
        self.questions_answered += 1
        print(f"Questions answered: {self.questions_answered}")

        # Disable all buttons
        for item in self.choice_button_ref:
            item.config(state=tk.DISABLED)

        # Update button colors based on correctness
        for button in self.choice_button_ref:
            if button['text'] == self.correct_answer:
                button.config(bg="light green")  # Correct answer
            elif button['text'] == user_choice:
                button.config(bg="red")  # Incorrect answer

        if user_choice == self.correct_answer:
            self.questions_won += 1
            print(f"Correct choice! Current score: {self.questions_won}/{self.questions_answered}")
            self.results_instance.increment_right()  # Update DisplayResults instance for correct answer
        else:
            print(f"Wrong choice. Current score: {self.questions_won}/{self.questions_answered}")
            self.results_instance.increment_wrong()  # Update Display Results instance for wrong answer

        self.score_label.config(
            text=f"Current Score: {self.questions_won} / {self.questions_answered}"
        )

        if self.questions_answered >= self.questions_wanted:
            self.next_question_button.config(state=tk.DISABLED, text="Game Over")
            for item in self.choice_button_ref:
                item.config(state=tk.DISABLED)
        else:
            self.next_question_button.config(state=tk.NORMAL)

    def reset_game(self):
        self.main_window.deiconify()
        self.answer_box.destroy()

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get results":
            self.results_instance.parent.deiconify()  # Show existing results window
        elif action == "start over":
            self.reset_game()
        else:
            self.new_question()


class DisplayHelp:
    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = tk.Toplevel()

        partner.to_help_btn.config(state=tk.DISABLED)

        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        self.help_frame = tk.Frame(self.help_box, width=300, height=200, bg=background)
        self.help_frame.grid()

        self.help_heading_label = tk.Label(self.help_frame, bg=background,
                                           text="Help / Hints",
                                           font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Your goal in this quiz is to guess the correct EPL team based on the displayed mascot. " \
                    "Select one of the options provided.\n\n" \
                    "To see your results, click on the 'Results' button.\n\n" \
                    "Try to get as many correct answers as possible!\n\n" \
                    "Good luck!"
        self.help_text_label = tk.Label(self.help_frame, bg=background,
                                        text=help_text, wraplength=350,
                                        justify="left")
        self.help_text_label.grid(row=1, padx=10, pady=10)

        self.dismiss_button = tk.Button(self.help_frame,
                                        font=("Arial", "12", "bold"),
                                        text="Dismiss", bg="#CC6600",
                                        fg="#FFFFFF",
                                        command=partial(self.close_help,
                                                        partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    def close_help(self, partner):
        self.help_box.destroy()
        partner.to_help_btn.config(state=tk.NORMAL)


class DisplayResults:
    def __init__(self, root):
        self.parent = tk.Toplevel(root)
        self.parent.title("Quiz Results")
        self.parent.withdraw()  # Hide results window initially

        self.right_count = 0
        self.wrong_count = 0

        self.right_var = tk.StringVar()
        self.wrong_var = tk.StringVar()
        self.comment_var = tk.StringVar()

        self.create_widgets()
        self.update_results()

        self.right_entry = None
        self.comment_entry = None
        self.wrong_entry = None

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
        self.parent.withdraw()


if __name__ == "__main__":
    ChooseQuestions()
