from tkinter import *


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
        self.intro_heading_label.grid(row=0, columnspan=3)

        choose_instructions_txt = "In each round you will be given four different " \
                                  "EPL teams to choose from and they will show the mascot of EPL teams. Pick a correct teams and see if " \
                                  "you can get correct or wrong!\n\n" \
                                  "To begin, type the number of rounds you'd like to play"
        self.choose_instructions_label = Label(self.intro_frame,
                                               text=choose_instructions_txt,
                                               wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1, columnspan=3)

        # Entry for Typing number of rounds
        self.Typing_rounds_label = Label(self.intro_frame, text="Typing rounds:")
        self.Typing_rounds_label.grid(row=2, column=0, sticky=E, pady=5,
                                      padx=(0, 10))  # Add padx=(0, 10) to add padding to the right

        self.Typing_rounds_entry = Entry(self.intro_frame)
        self.Typing_rounds_entry.grid(row=2, column=1, sticky=W, pady=5,
                                      padx=(0, 10))  # Add padx=(0, 10) to add padding to the right

        # Submit button for Typing rounds
        self.Start_button = Button(self.intro_frame, text="Start", command=self.submit_Typing_rounds,
                                  font=button_font, width=5)
        self.Start_button.grid(row=2, column=2, pady=5, padx=(5, 0), sticky=W+E, columnspan=1)

        # Merge the two adjacent columns
        self.intro_frame.grid_columnconfigure(0, weight=1)  # Original column weight for label
        self.intro_frame.grid_columnconfigure(1, weight=2)  # Increased weight for entry

    def submit_Typing_rounds(self):
        num_rounds = self.Typing_rounds_entry.get()
        print("You Chose {} rounds".format(num_rounds))


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guessing EPL Team Quiz")
    ChooseRounds()
    root.mainloop()
