# A HANGMAN GAME IN PYTHON


import random

words = ("cameleon", "kangaroo", "platapus", "bobcat", "tortise", "flamingo")

# Dictionary Key ()
hangman_art = {0: ("  ",
                   "  ",
                   "  "),
              
               1: (" o ",
                   "   ",
                   "   "),
               
               2: (" o ",
                   " | ",
                   "   "),
               
               3: (" o ",
                   "/| ",
                   "   "),
               
               4: (" o   ",
                   "/|\\ ",
                   "     "),
               
               5: (" o  ",
                   "/|\\ ",
                   "/    "),
               
               6: (" o   ",
                   "/|\\ ",
                   "/ \\ ")}




def display_man(wrong_guesses):
    for line in hangman_art[wrong_guesses]:
        print(line)

def display_hint(hint):
    print(" ".join(hint))

def display_answer(answer):
    print(" ".join(answer))


def main():
    print("Welcome to a hangman game ... let's see if you can guess the name of the animal before your guesses run out 🐾\n")    

def main():
    answer = random.choice(words)
    hint = ["_"] * len(answer)
    wrong_guesses = 0
    guessed_letters = set()
    is_running = True

    while is_running:
        display_man(wrong_guesses)
        display_hint(hint)
        guess = input("Enter a letter: ").lower()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Stop fooling 😒")
            continue

        # Check if already guessed
        if guess in guessed_letters:
            print(f"{guess} is already guessed, try another.")
            continue

        guessed_letters.add(guess)

        # Correct guess
        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
        else:
            wrong_guesses += 1

        # Win condition
        if "_" not in hint:
            display_man(wrong_guesses)
            display_answer(answer)
            print("ALLAH SHAKOR 🎉")
            is_running = False

        # Lose condition
        elif wrong_guesses >= len(hangman_art) - 1:
            display_man(wrong_guesses)
            display_answer(answer)
            print("TAKE YOUR BAG AND GO HOME 😢")
            is_running = False

if __name__ == "__main__":
    main()

