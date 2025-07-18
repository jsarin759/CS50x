#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int add_values(string word, int word_length, int sum);

const int N = 26;
char letters[N];
int values[N];

int main(void)
{

    for (int i = 0; i < N; i++)
    {
        char j = i + 65;
        if (j == 'A' || j == 'E' || j == 'I' || j == 'L' || j == 'N' || j == 'O' || j == 'R' ||
            j == 'S' || j == 'T' || j == 'U')
        {
            values[i] = 1;
        }
        else if (j == 'D' || j == 'G')
        {
            values[i] = 2;
        }
        else if (j == 'B' || j == 'C' || j == 'M' || j == 'P')
        {
            values[i] = 3;
        }
        else if (j == 'F' || j == 'H' || j == 'V' || j == 'W' || j == 'Y')
        {
            values[i] = 4;
        }
        else if (j == 'K')
        {
            values[i] = 5;
        }
        else if (j == 'J' || j == 'X')
        {
            values[i] = 8;
        }
        else if (j == 'Q' || j == 'Z')
        {
            values[i] = 10;
        }

        letters[i] = j;
    }

    string p1_word = get_string("Player 1: ");
    string p2_word = get_string("Player 2: ");

    int p1_word_length = strlen(p1_word);
    int p2_word_length = strlen(p2_word);

    int p1_sum = 0;
    int p2_sum = 0;

    int p1_score = add_values(p1_word, p1_word_length, p1_sum);
    int p2_score = add_values(p2_word, p2_word_length, p2_sum);
    if (p1_score > p2_score)
    {
        printf("Player 1 wins!\n");
    }
    else if (p1_score < p2_score)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int add_values(string word, int word_length, int sum)
{
    for (int k = 0; k < word_length; k++)
    {
        word[k] = toupper(word[k]);
        for (int l = 0; l < N; l++)
        {
            if (letters[l] == word[k])
            {
                sum += values[l];
            }
        }
    }
    return sum;
}
