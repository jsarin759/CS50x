import csv
import sys


def main():

    # TODO: Check for command-line usage
    while True:
        if len(sys.argv) == 3:
            break
        else:
            print("Format: dna.py [name of file].csv [name of file].txt")
            break

    # TODO: Read database file into a variable
    database_rows = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames  # is a list of the headers
        for row in reader:
            database_rows.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        dna_sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    longest_matches = []
    for i in range(1, len(header)):
        a = longest_match(dna_sequence, header[i])
        longest_matches.append(a)

    # TODO: Check database for matching profiles
    matches = []
    for row in database_rows:
        for i in range(1, len(header)):
            matches.append(int(row[header[i]]))
        if matches == longest_matches:
            print(row["name"])
            break
        matches.clear()
    else:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
