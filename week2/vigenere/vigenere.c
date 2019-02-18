#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int shift(char c);

int main(int argc, string argv[])
{
	// If only one key provided
	if (argc == 2)
	{
		for (int i = 1, j = 0, n = strlen(argv[i]); j < n; j++)
		{
			// If any keys aren't digits, break
			if (!isalpha(argv[i][j]))
			{
				printf("Usage: ./vigenere key\n");
				return 1;
			}
		}
	}
	else
	{
		printf("Usage: ./caesar key\n");
		return 1;
	}

	// Get input
	string s = get_string("plaintext: ");

	// Loop through & print deciphered value
	printf("ciphertext: ");
	for (int i = 0, k = 0, n = strlen(s); i < n; i++)
	{
		// If its alphabetic, advance and increment
		if (isalpha(s[i]))
		{
			// Wrap around minus punctuations
			int j = (i - k) % strlen(argv[1]);
			// If it's upper case, keep it
			if (isupper(s[i]))
			{
				printf("%c", 'A' + (((s[i] - 'A') + shift(argv[1][j])) % 26));
			}
			// Else print normal lower
			else if (islower(s[i]))
			{
				printf("%c", 'a' + (((s[i] - 'a') + shift(argv[1][j])) % 26));
			}
		}
		else
		{
			// Just print non-alpha
			printf("%c", s[i]);
			// Increment to not shift other counter
			k++;
		}
	}
	printf("\n");
	return 0;
}

// Takes CHAR, returns shifted INT
int shift(char c)
{
	if (isupper(c))
	{
		return c - 'A';
	}
	else if (islower(c))
	{
		return c - 'a';
	}
	return c;
}
