from cs50 import get_int

# Main: gets input & prints bars


def main():
    h = get_positive_int("Height: ")
    for i in range(h):
        print_line(i + 1, h)


# Max height
maxHeight = 8

# Validates only until postive integer (within the range)


def get_positive_int(prompt):
    while True:
        n = get_int(prompt)
        if n > 0 and n <= maxHeight:
            return n


# Calculates spaces and bars, then prints that line


def print_line(lineNumber, h):
    spaces = h - lineNumber
    hashes = lineNumber
    space = ' '
    b = '#'
    # Print line * number of times
    if h == lineNumber:
        print(b * hashes)
    else:
        print(space * (spaces - 1), b * hashes)


# Execute program
if __name__ == "__main__":
    main()
