#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

int get_positive_int(char *prompt);

int main(void)
{
	// Returns user answer
	int h = get_positive_int("Height: ");

	for (int i = 1; i <= h; i++)
	{
		// Add spaces for pyramid
		for (int k = h - i; k > 0; k--)
		{
			printf(" ");
		}
		// Prints the pyramid
		for (int j = 1; j <= i; j++)
		{
			printf("#");
		}
		printf("\n");
	}
	// Success
	return 0;
}

// Prompt user for positive integer
int get_positive_int(char *prompt)
{
	int n;
	while (true)
	{
		n = scanf("%s", prompt);
		if (n > 0 && n <= 8)
		{
			return n;
		}
	}
	// Exit - failure
	return 1;
}
