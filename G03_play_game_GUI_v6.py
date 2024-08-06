from tkinter import *
from functools import partial
import csv
import random

from G04_results_GUI_v1 import *

class Play:
    def __init__(self, how_many):
        self.play_box = Toplevel()
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.reset_game))

        self.rounds_wanted = how_many
        self.rounds_played = 0
        self.rounds_won = 0
        self.user_scores = []
        self.all_colours = self.get_all_colours()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.choose_heading = Label(self.quest_frame, text=f"Round 1 of {how_many}",
                                    font=("Arial", "16", "bold"))
        self.choose_heading.grid(row=0)

        self.instructions_label = Label(self.quest_frame, text="What team does this mascot belong to?",
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        self.choice_button_ref = []
        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame, width=21,
                                        command=lambda i=item: self.to_compare(self.choice_button_ref[i]['text']))
            self.choice_button_ref.append(self.choice_button)
            self.choice_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

        self.next_round_button = Button(self.quest_frame, text="Next Round",
                                        width=45, pady=4, command=lambda: self.new_round())
        self.next_round_button.grid(row=3)

        self.score_label = Label(self.quest_frame, text="Current Score 0 / 0", font=("Arial", "12"))
        self.score_label.grid(row=4, pady=(5, 0))

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#004C99", "Results", "get results"],
            ["#CC6600", "Help", "get help"],
            ["#808080", "Start Over", "start over"]
        ]

        self.control_button_ref = []
        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame, fg="#FFFFFF",
                                              bg=control_buttons[item][0], text=control_buttons[item][1],
                                              width=11, font=("Arial", "10", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=8, pady=5)
            self.control_button_ref.append(self.make_control_button)

        self.to_help_btn = self.control_button_ref[1]
        self.to_results_btn = self.control_button_ref[1]

        self.new_round()

    def get_all_colours(self):
        with open("football_players.csv", "r") as file:
            var_all_colors = list(csv.reader(file, delimiter=","))
        var_all_colors.pop(0)
        return var_all_colors

    def get_round_colors(self):
        round_colour_list = []
        color_scores = []

        while len(round_colour_list) < 4:
            chosen_colour = random.choice(self.all_colours)
            if chosen_colour[1] not in color_scores:
                round_colour_list.append(chosen_colour)
                color_scores.append(chosen_colour[1])

        return round_colour_list

    def new_round(self):
        self.button_colours_list = self.get_round_colors()
        correct_index = random.randint(0, 3)
        self.correct_answer = self.button_colours_list[correct_index][1]
        round_number = self.rounds_played + 1  # Calculate current round number

        # Update the heading label with the correct round number
        self.choose_heading.config(text=f"Round {round_number} of {self.rounds_wanted}")

        self.instructions_label.config(
            text=f"What team does the mascot {self.button_colours_list[correct_index][0]} belong to?")
        for idx, button in enumerate(self.choice_button_ref):
            button['text'] = self.button_colours_list[idx][1]
            button['state'] = NORMAL

    def to_compare(self, user_choice):
        print(f"User choice: {user_choice}")
        self.rounds_played += 1
        print(f"Rounds played: {self.rounds_played}")

        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        if user_choice == self.correct_answer:
            self.rounds_won += 1
            print(f"Correct choice! Current score: {self.rounds_won}/{self.rounds_played}")
        else:
            print(f"Wrong choice. Current score: {self.rounds_won}/{self.rounds_played}")

        self.score_label.config(
            text=f"Current Score: {self.rounds_won} / {self.rounds_played}"
        )

        if self.rounds_played >= self.rounds_wanted:
            self.next_round_button.config(state=DISABLED, text="Game Over")
            for item in self.choice_button_ref:
                item.config(state=DISABLED)
        else:
            self.next_round_button.config(state=NORMAL)

    def reset_game(self):
        self.rounds_played = 0
        self.rounds_won = 0
        self.user_scores = []
        self.new_round()
        self.next_round_button.config(state=NORMAL, text="Next Round")
        for button in self.choice_button_ref:
            button.config(state=NORMAL)
        self.play_box.destroy()

    def to_do(self, action):
        if action == "get help":
            self.get_help()
        elif action == "get results":
            self.get_results()
        elif action == "start over":
            self.reset_game()
        else:
            self.new_round()

    def get_help(self):
        DisplayHelp(self)

    def get_results(self):
        results_window = DisplayResults(self, self.rounds_won, self.rounds_played)


# Show users help / game tips


class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Hints",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Your goal in this quiz is to get a correct answer " \
                    "and you will see the mascot name in the question - you need to choose the answer" \
                    "If you get a correct your score will showing underneath next round button.\n\n" \
                    "To see your Results, click on " \
                    "the 'Results' button.  \n\n" \
                    "Try to get all correct in this quiz " \
                    "Don't be discouraged if you don't win every " \
                    "round, it's your overall score that counts. \n\n" \
                    "Good luck!  Choose carefully."
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...

        self.help_box.destroy()
        partner.to_help_btn.config(state=NORMAL)

class DisplayResults:
    def __init__(self, partner, correct_count, total_count):
        self.parent = tk.Toplevel()
        self.parent.title("Quiz Results")

        self.right_count = correct_count
        self.wrong_count = total_count - correct_count

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

        dismiss_button = tk.Button(self.parent, text="Dismiss", bg="#FFFF00", command=self.dismiss)
        dismiss_button.pack(pady=10, padx=50, ipadx=50)

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

    def set_results(self, right, wrong, comment):
        self.right_var.set(right)
        self.wrong_var.set(wrong)
        self.comment_var.set(comment)

    def increment_right(self):
        self.right_count += 1
        self.update_results()

    def increment_wrong(self):
        self.wrong_count += 1
        self.update_results()

    def dismiss(self):
        self.parent.destroy()

