from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random

class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:

    def __init__(self, how_many):

        self.play_box = Toplevel()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Results", "get results"],
            ["#808080", "Start Over", "start over"]
        ]

        # list to hold references for control buttons
        # so that the text of the 'start over' button
        # can easily be configured when the game is over
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # Add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        self.to_help_btn = self.control_button_ref[0]

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            pass
        else:
            self.close_play()

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()


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
                    "and you will see the mascot name in the question - you need to choose the answer " \
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


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guessing EPL Team Quiz")
    ChooseRounds()
    root.mainloop()