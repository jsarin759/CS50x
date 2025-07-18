#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

const int N = 26;
char letters[N];

int main(int argc, string argv[])
{
    while (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    while (strlen(argv[1]) != N)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < N; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Key must be alphabetical.\n");
            return 1;
        }
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (i != j && argv[1][i] == argv[1][j])
            {
                printf("Key has repeating letters.\n");
                return 1;
            }
        }
    }

    for (int i = 0; i < N; i++)
    {
        if (islower(argv[1][i]))
        {
            argv[1][i] = toupper(argv[1][i]);
        }
    }

    for (int i = 0; i < N; i++)
    {
        char j = i + 97;
        letters[i] = j;
    }

    string text = get_string("plaintext:  ");
    char original[strlen(text) - 1];
    strcpy(original, text);

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        text[i] = tolower(text[i]);
        if (isalpha(text[i]))
        {
            for (int j = 0; j < N; j++)
            {
                if (letters[j] == text[i])
                {
                    text[i] = argv[1][j];
                }
            }
        }
    }

    for (long i = 0, n = strlen(text); i < n; i++)
    {
        if (islower(original[i]))
        {
            text[i] = tolower(text[i]);
        }
        else if (isupper(original[i]))
        {
            text[i] = toupper(text[i]);
        }
    }

    printf("ciphertext: %s\n", text);

    return 0;
}
