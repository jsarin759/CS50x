// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 475253; // 26^4

// Hash table
node *table[N];

// Word count
unsigned int word_count;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int index = hash(word);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int first_digit = 0;
    int second_digit = 0;
    int third_digit = 0;
    int fourth_digit = 0;
    int first_four_letters = 0;

    int len = strlen(word);

    if (len == 1)
    {
        fourth_digit = tolower(word[0]) - 'a';
        third_digit = 0;
        second_digit = 0;
        first_digit = 0;
    }
    else if (len == 2)
    {
        fourth_digit = tolower(word[1]) - 'a';
        third_digit = tolower(word[0]) - 'a' + 1;
        second_digit = 0;
        first_digit = 0;
    }
    else if (len == 3)
    {
        fourth_digit = tolower(word[2]) - 'a';
        third_digit = tolower(word[1]) - 'a' + 1;
        second_digit = tolower(word[0]) - 'a' + 1;
        first_digit = 0;
    }
    else if (len >= 4)
    {
        fourth_digit = tolower(word[3]) - 'a';
        third_digit = tolower(word[2]) - 'a' + 1;
        second_digit = tolower(word[1]) - 'a' + 1;
        first_digit = tolower(word[0]) - 'a' + 1;
    }

    first_four_letters =
        (17576 * first_digit) + (676 * second_digit) + (26 * third_digit) + fourth_digit;
    return first_four_letters;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        printf("Unable to open the dictionary.\n");
        return false;
    }

    char word[LENGTH + 1];

    // Read each word in the file
    while (fscanf(source, "%s", word) != EOF)
    {
        // Add each word to the hash table
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);

        unsigned int index = hash(word);
        n->next = table[index];
        table[index] = n;
        word_count++;
    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
