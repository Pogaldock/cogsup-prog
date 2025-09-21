"""
Have a look at the script called 'human-guess-a-number.py' (in the same folder as this one).

Your task is to invert it: You should think of a number between 1 and 100, and the computer 
should be programmed to keep guessing at it until it finds the number you are thinking of.

At every step, add comments reflecting the logic of what the particular line of code is (supposed 
to be) doing. 
"""



def guess_number():

    # Set initial parameters
    low = 1
    high = 100
    found = False

    # Keep guessing untill correct number is found
    while not found:

        # Take the middle of the current search space as a guess
        guess = (low+high)//2

        # Ask user for feedback
        response = input(f"Is {guess} the number you are thinking of? Hit '+' if your number is higher, '-' if lower, or press Enter if my guess is correct: ")
        
        # Use user feedback to redefine current search space
        if response == "":
            print(f"I win! Your number was {guess}")
            # This ends the game
            found = True

        elif response == "+":
            # We know the number is between the max and the previous guess so we redefine the search space
            low = guess + 1

        elif response == "-":
            # We know the number is between the min and the previous guess so we redefine the search space
            high = guess - 1

        else:
            # Catches wrong inputs
            print("Invalid response.")

# run the game
guess_number()
