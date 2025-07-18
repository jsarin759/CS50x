text = input("Text: ")
length = int(len(text))

letter_count = 0
word_count = 1
sentence_count = 0

for i in range(length):
    if text[i].isalpha():
        letter_count += 1
    elif text[i].isspace():
        word_count += 1
    elif text[i] in [".", "?", "!"]:
        sentence_count += 1

L = (float(letter_count) / float(word_count)) * 100.0
S = (float(sentence_count) / float(word_count)) * 100.0

index = 0.0588 * L - 0.296 * S - 15.8
index = round(index)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
