from G03_play_game_GUI_v6 import *

class ChooseRounds:

    def __init__(self):
        button_font = ("Arial", "13", "bold")

        self.var_has_error = StringVar()
        self.var_feedback = StringVar()

        # Set up GUI Frame
        self.intro_frame = Frame(padx=10, pady=10)
        self.intro_frame.grid()

        # heading and brief instructions
        self.intro_heading_label = Label(self.intro_frame, text="Guessing EPL Team Quiz",
                                         font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0, columnspan=3)

        choose_instructions_txt = "In each round you will be given four different " \
                                  "EPL teams to choose from and they will show the mascot of EPL teams. " \
                                  "Pick a correct teams and see if " \
                                  "you can get correct or wrong!\n\n" \
                                  "To begin, type the number of rounds you'd like to play"
        self.choose_instructions_label = Label(self.intro_frame,
                                               text=choose_instructions_txt,
                                               wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1, columnspan=3)

        # Entry for Typing number of rounds
        self.typing_rounds_label = Label(self.intro_frame, text="Typing rounds:")
        self.typing_rounds_label.grid(row=2, column=0, sticky=E, pady=5, padx=(0, 10))  # Add padx=(0, 10) for padding

        self.typing_rounds_entry = Entry(self.intro_frame)
        self.typing_rounds_entry.grid(row=2, column=1, sticky=W, pady=5, padx=(0, 10))  # Add padx=(0, 10) for padding

        # Submit button for Typing rounds
        self.start_button = Button(self.intro_frame, text="Start", command=self.submit_typing_rounds, bg="sky blue",
                                   fg="#FFFFFF",
                                   font=button_font, width=5)
        self.start_button.grid(row=2, column=2, pady=5, padx=(5, 0), sticky=W+E, columnspan=1)

        # Error label
        self.error_label = Label(self.intro_frame, text="", fg="red")
        self.error_label.grid(row=3, columnspan=3)

        # Merge the two adjacent columns
        self.intro_frame.grid_columnconfigure(0, weight=1)  # Original column weight for label
        self.intro_frame.grid_columnconfigure(1, weight=2)  # Increased weight for entry

    def submit_typing_rounds(self):
        num_rounds = self.typing_rounds_entry.get()
        valid = self.check_input(1)
        if valid == "invalid":
            # input is invalid
            print("Invalid input")
        else:
            root.withdraw()
            Play(int(num_rounds))

    # check user input to ensure it's valid, then convert temperature
    def check_input(self, num_rounds):
        has_error = "no"
        error = "Please enter a number that is more " \
                "than {}"
        # check that the user has entered a valid number...

        response = self.typing_rounds_entry.get()

        try:
            response = int(response)

            if response < num_rounds:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # Sets var_has_error so that the entry box and labels
        # can be correctly formatted by the formatting function
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        # if we have no errors...
        else:
            # set to 'no' in case of previous errors
            self.var_has_error.set("no")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guessing EPL Team Quiz")
    ChooseRounds()
    root.mainloop()
