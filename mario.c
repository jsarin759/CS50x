#include <cs50.h>
#include <stdio.h>

void spaces(int space);
void hastags(int hastag);

int main(void)
{
    // checks if inputted number is between 1 and 8, inclusive
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    for (int i = 0; i < n; i++) // pyramid will have n columns
    {
        // defines each row
        int c = i + 1;
        spaces(n - c);
        hastags(c);
        printf("  ");
        hastags(c);
        printf("\n");
    }
}

void spaces(int space) // creates the spaces in each row
{
    for (int j = 0; j < space; j++)
    {
        printf(" ");
    }
}

void hastags(int hastag) // creates the hastag symbols in each row
{
    for (int k = 0; k < hastag; k++)
    {
        printf("#");
    }
}
