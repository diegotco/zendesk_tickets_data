import csv


filename = "ticket_messages.txt"
words = [] # The empty list that will be filled up with th whole words, some lines ahead. 

with open(filename, "r", encoding='utf-8-sig') as f:
    string = f.read()

    # getting index of substrings.
    id1 = string.index("'")
    id2 = string.index("']")

    text = string[id1 + 1: id2]

    text_splited_by_words = text.split()

    for word in text_splited_by_words:
        words.append(word)
        
with open('split_messages.csv', 'w') as f:
    f.write(str(words))
