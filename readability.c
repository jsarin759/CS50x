#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string text = get_string("Text: ");
    long n = strlen(text);

    int letter_count = 0;
    int word_count = 1;
    int sentence_count = 0;

    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letter_count++;
        }
    }

    for (int j = 0; j < n; j++)
    {
        if (isblank(text[j]))
        {
            word_count++;
        }
    }

    for (int k = 0; k < n; k++)
    {
        if (text[k] == '.' || text[k] == '?' || text[k] == '!')
        {
            sentence_count++;
        }
    }

    float L = ((float) letter_count / (float) word_count) * 100.0;
    float S = ((float) sentence_count / (float) word_count) * 100.0;

    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) index);
    }
}
