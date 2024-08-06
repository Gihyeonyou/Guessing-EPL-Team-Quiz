from tkinter import *
from functools import partial  # To prevent unwanted windows


class ChooseRounds:

    def __init__(self):
        button_fg = "#FFFFFF"
        button_font = ("Arial", "13", "bold")

        # Set up GUI Frame
        self.intro_frame = Frame(padx=10, pady=10)
        self.intro_frame.grid()

        # heading and brief instructions
        self.intro_heading_label = Label(self.intro_frame, text="Guessing EPL Team Quiz",
                                         font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0)

        choose_instructions_txt = "In each round you will be given four different " \
                                  "EPL teams to choose from and they will show the mascot of EPL teams. Pick a correct teams and see if " \
                                  "you can get correct or wrong!\n\n" \
                                  "To begin, type how many rounds you'd like to " \
                                  "play..."
        self.choose_instructions_label = Label(self.intro_frame,
                                               text=choose_instructions_txt,
                                               wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1)

        # Rounds buttons...
        self.how_many_frame = Frame(self.intro_frame)
        self.how_many_frame.grid(row=2)

        button_back = ["#CC0000", "#009900", "#000099"]

        for item in range(1, 4):
            self.rounds_button = Button(self.how_many_frame,
                                        fg=button_fg, bg=button_back[item-1],
                                        text="{} Rounds".format(item),
                                        font=button_font, width=10,
                                        command=lambda i=item: self.to_play(i)
                                        )
            self.rounds_button.grid(row=0, column=item-1,
                                    padx=5, pady=5)

    def to_play(self, num_rounds):
        print("You Chose {} rounds".format(num_rounds))


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guessing EPL Team Quiz")
    ChooseRounds()
    root.mainloop()