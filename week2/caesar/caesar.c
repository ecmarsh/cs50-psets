#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
	int k;
	// If only one key provided
	if (argc == 2)
	{
		for (int i = 1, j = 0, n = strlen(argv[i]); j < n; j++)
		{
			// If any keys aren't digits, break
			if (!isdigit(argv[i][j]))
			{
				printf("Usage: ./caesar key\n");
				return 1;
			}
		}
		// If all them pass, convert it to an integer
		k = atoi(argv[1]);
	}
	else
	{
		printf("Usage: ./caesar key\n");
		return 1;
	}

	// Get plaintext
	string s = get_string("plaintext: ");

	// Loop through characters & print cipher text
	printf("ciphertext: ");
	for (int i = 0, n = strlen(s); i < n; i++)
	{
		if (isalpha(s[i]))
		{
			if (isupper(s[i]))
			{
				// Conver to digit, then shift and back
				printf("%c", 'A' + ((s[i] - 'A') + k) % 26);
			}
			else if (islower(s[i]))
			{
				// Use lower index a then convert back
				printf("%c", 'a' + ((s[i] - 'a') + k) % 26);
			}
		}
		else
		{
			// Just print the character without shift
			printf("%c", s[i]);
		}
	}
	// New line & exit
	printf("\n");
	return 0;
}
