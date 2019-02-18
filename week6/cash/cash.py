from cs50 import get_float

# Answer with minimum number of coins possible


def main():
    totalCoins = count_coins(change)
    print(f"{totalCoins}")

# Prompts user for change until valid value
# Returns rounded cents


def get_positive_float(prompt):
    while True:
        dollars = get_float(prompt)
        if dollars > 0:
            cents = round(dollars, 2) * 100
            return cents

# Go through each coin and count


def count_coins(n):
    coinsCount = 0
    for coin in coinsList:
        while n >= coin:
            n -= coin
            coinsCount += 1
    return coinsCount


# Call prompt
askFor = "Change: "
# Store change amount
change = get_positive_float(askFor)

# Define coin variables
coinsList = [25, 10, 5, 1]

# Execute program
if __name__ == "__main__":
    main()