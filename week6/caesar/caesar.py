from sys import argv
from cs50 import get_string

# Main: gets input & prints bars


def main():
    k = validate()
    phrase = get_plaintext('plaintext: ')
    # Encipher and print values
    enciphered = []
    for s in phrase:
        for c in s:
            if c.isalnum():
                enciphered.append(encipher(c, k))
            else:
                enciphered.append(c)
    ciphertext = "".join(enciphered)
    print(f"ciphertext: {ciphertext}")


# Validate argument key


def validate():
    if len(argv) == 2 and argv[1].isnumeric():
        k = int(argv[1])
        if k > 0:
            return k
    else:
        print("Usage: python caesar.py k")
        exit(1)


# Prompt user for plaintext


def get_plaintext(prompt):
    while True:
        phrase = get_string(prompt)
        if len(phrase) > 0:
            return phrase


# Encipher each character and return enciphered value


def encipher(c, shift):
    shifted = ord(c.lower()) - ord('a') + shift
    if c.isupper():
        base = ord('A')
    else:
        base = ord('a')
    return chr(base + (shifted % 26))


# Execute program
if __name__ == "__main__":
    main()