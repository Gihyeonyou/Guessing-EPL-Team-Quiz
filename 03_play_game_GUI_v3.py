from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


# users choose 3, 5 or 10 rounds
class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_play(3)
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:

    def __init__(self, how_many):

        self.play_box = Toplevel()

        # If users press cross at top, closes help and
        # 'releases' help button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        # Variables used to work out statistics, when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Initially set rounds played and rounds won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user score/s
        # used to work out statistics
        self.user_scores = []

        # get all the colours for use in game
        self.all_colours = self.get_all_colours()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading = "Choose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

        instructions = " What team does this mascot belong to? " \


        self.instructions_label = Label(self.quest_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        # get colours for buttons for first round ...
        self.button_colours_list = []

        # create colour buttons (in choice_frame)!
        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        # list to hold references for coloured buttons
        # so that they can be configured for new rounds etc
        self.choice_button_ref = []

        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame,
                                        width=15,
                                        command=lambda i=item: self.to_compare(self.button_colours_list[i])
                                        )
            # add button to reference list for later configuration
            self.choice_button_ref.append(self.choice_button)

            self.choice_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame)
        self.rounds_frame.grid(row=4, pady=5)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#004C99", "Results", "get results"],
            ["#CC6600", "Help", "get help"],
            ["#808080", "Start Over", "start over"],
            ["#34c0eb", "Next Round", "new_round"]
        ]

        # list to hold references for control buttons
        # so that the text of the 'start over' button
        # can easily be configured when the game is over
        self.control_button_ref = []

        for item in range(0, 4):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=9, font=("Arial", "10", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # Add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        # define next button after control buttons are created
        self.next_button = self.control_button_ref[3]

        # at start, get 'new round'
        self.new_round()

    # retrieve colours from csv file
    def get_all_colours(self):
        file = open("football_players.csv", "r")
        var_all_colors = list(csv.reader(file, delimiter=","))
        file.close()

        # removes first entry in list (ie: the header row).
        var_all_colors.pop(0)
        return var_all_colors

    # randomly choose six colours for buttons
    def get_round_colors(self):
        round_colour_list = []
        color_scores = []

        # Get six unique colours
        while len(round_colour_list) < 6:
            # choose item
            chosen_colour = random.choice(self.all_colours)
            index_chosen = self.all_colours.index(chosen_colour)

            # check score is not already in list
            if chosen_colour[1] not in color_scores:
                # add item to rounds list
                round_colour_list.append(chosen_colour)
                color_scores.append(chosen_colour[1])

                # remove item from master list
                self.all_colours.pop(index_chosen)

        return round_colour_list

    # sets up new round when 'next' button is pressed
    def new_round(self):

        # disable next button (enable it at the end
        # of the round)
        self.next_button.config(state=DISABLED)

        # empty button list so we can get new colours
        self.button_colours_list.clear()

        # get new colours for buttons
        self.button_colours_list = self.get_round_colors()

        # Pick random index for answer
        correct_index = self.button_colours_list[random.randint(0, 3)]

        # Ask question
        self.instructions_label.config(
            text=f"What team does the mascot {self.button_colours_list[correct_index][1]} belong to?"
        )

        # set button bg, fg and text
        count = 0
        for item in self.choice_button_ref:
            item['text'] = self.button_colours_list[count][0]
            item['state'] = NORMAL

            count += 1

        # retrieve number of rounds wanted / played
        # and update heading.
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = "Choose - Round {} of " \
                      "{}".format(current_round + 1, how_many)
        self.choose_heading.config(text=new_heading)

    # work out who won and if the game is over
    # update win / loss labels and buttons
    def to_compare(self, user_choice):

        how_many = self.rounds_wanted.get()

        # Add one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)

        # deactivate colour buttons!
        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        # set up background colours...
        win_colour = "#D5E8D4"
        lose_colour = "#F8CECC"

        # retrieve user score, make it into an integer
        # and add to list for stats
        user_score_current = int(user_choice[1])
        self.user_scores.append(user_score_current)

        # remove user choice from button colours list
        to_remove = self.button_colours_list.index(user_choice)
        self.button_colours_list.pop(to_remove)

        # get total scores for user ...
        user_total = sum(self.user_scores)

        self._results_label.config(text="")

        # if the game is over, disable all buttons
        # and change text of 'next' button to either
        # 'You Win' or 'You Lose' and disable all buttons

        if current_round == how_many:
            # Change 'next' button to show overall
            # win / loss result and disable it
            self.next_button.config(state=DISABLED,
                                    text=" ")

            # update 'start over button'
            start_over_button = self.control_button_ref[2]
            start_over_button['text'] = "Play Again"
            start_over_button['bg'] = "#009900"

            # change all colour button background to light grey
            for item in self.choice_button_ref:
                item['bg'] = "#C0C0C0"

        else:
            # enable next round button and update heading
            self.next_button.config(state=NORMAL)

    # Detects which 'control' button was pressed and
    # invokes necessary function.  Can possibly replace functions
    # with calls to classes in this section!
    def to_do(self, action):
        if action == "get help":
            self.get_help()
        elif action == "get results":
            self.get_results()
        else:
            self.close_play()

    def get_results(self):
        print("You chose to get the results")

    def get_help(self):
        print("You chose to get help")

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    ChooseRounds()
    root.mainloop()