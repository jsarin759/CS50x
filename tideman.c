#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
const int MAX = 9;

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // vote(0, Charlie, ranks)
            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        printf("\n");
        record_preferences(ranks);
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (j < candidate_count)
            {
                preferences[ranks[i]][ranks[j]]++;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    int index = 0;
    for (int i = 0; i < candidate_count; i++) // rows
    {
        for (int j = 0; j < candidate_count; j++) // columns
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[index].winner = i;
                pairs[index].loser = j;
                index++;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
// The idea to switch the pairs using bubble sort was my idea, but the actual implementation of it
// was referenced by this youtube video: https://www.youtube.com/watch?v=B367g8jFePw. I thought I
// had to switch the pairs[i].winner and pairs[i].losers seperately, but the video taught me that I
// could just switch pairs[i] on its own and will thus switch its attributes automatically.
void sort_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - i - 1; j++)
        {
            if (preferences[pairs[j].winner][pairs[j].loser] <
                preferences[pairs[j + 1].winner][pairs[j + 1].loser])
            {
                pair temp = pairs[j];
                pairs[j] = pairs[j + 1];
                pairs[j + 1] = temp;
            }
        }
    }
    return;
}

// The implementation to use a cycle_found function for the logic of a cycle was referenced by this
// youtube video: https://www.youtube.com/watch?v=B367g8jFePw. I knew that for a cycle to take
// place, there must be excatly one 'true' in each row and column. For no cycle to take place, there
// must be a full row or column of 'false.' However, my method wasn't working properly so I sought
// the video for advice. This function is a recursive function that checks if adding a new edge will
// create a cycle.
bool cycle_found(int winner, int loser)
{
    // Base case. If both the winner and loser of each pair are the same (the winner and loser are
    // the same person), then a cycle takes place.
    if (winner == loser)
    {
        return true;
    }

    // Iterates through all of the candidates
    for (int i = 0; i < candidate_count; i++)
        // Checks if there is a locked edge between the loser and candidate i.
        if (locked[loser][i])
        {
            // The recursive call helps explore all possible paths from the winner and candidates.
            if (cycle_found(winner, i))
            {
                return true;
            }
        }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        // if the cycle_found function evaluates to false (no cycle will be present), then the
        // winner's edge over the loser is "locked in."
        if (!cycle_found(pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[0][i] == false && locked[1][i] == false && locked[2][i] == false)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}
