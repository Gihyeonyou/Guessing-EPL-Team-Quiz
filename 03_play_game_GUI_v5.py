from tkinter import *
from functools import partial
import csv
import random


class ChooseRounds:
    def __init__(self):
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)
        root.withdraw()  # Hide root window after choosing rounds


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
        self.instructions_label.config(
            text=f"What team does the mascot {self.button_colours_list[correct_index][0]} belong to?")
        self.correct_answer = 1
        for idx, button in enumerate(self.choice_button_ref):
            button['text'] = self.button_colours_list[idx][1]
            button['state'] = NORMAL

    def to_compare(self, user_choice):
        self.rounds_played += 1
        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        if user_choice == self.correct_answer:
            self.rounds_won += 1

        # Update score label to display current score
        self.score_label.config(
            text=f"Current Score: {self.rounds_won} / {self.rounds_played}"
        )

        if self.rounds_played == self.rounds_wanted:
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

# Main routine


if __name__ == "__main__":
    root = Tk()
    root.title("Guessing EPL Teams Quiz")
    ChooseRounds()
    root.mainloop()
