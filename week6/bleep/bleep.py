#!/usr/bin/python
from sys import argv
from cs50 import get_string

# Dictionary set
words = set()


def main():
    # Validate the arguments
    dictionary = validate()

    # Load the dictionary
    load_set(dictionary)

    # Prompt for message
    message = get_message("What message would you like to censor?\n").split()

    # Check for matches
    for word in message:
        check(word, message)

    # Print the new message
    censored_message = " ".join(message)
    print(censored_message)


# Validate arguments and return to main if valid
def validate():
    t = argv[1]
    if len(argv) == 2 and t[len(t)-4:len(t)] == '.txt':
        return argv[1]
    else:
        print("Usage: python bleep.py dictionary")
        exit(1)

# Fill set with dictionary words


def load_set(dictionary):
    file = open(dictionary, "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True

# Prompt user for message


def get_message(prompt):
    while True:
        message = get_string(prompt)
        if len(message) > 0:
            return message
        else:
            exit(1)

# Check each word


def check(word, message):
    if word.lower() in words:
        i = message.index(word)
        message[i] = ('*' * len(word))


# Execute program
if __name__ == "__main__":
    main()
