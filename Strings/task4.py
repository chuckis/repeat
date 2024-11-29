letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
count_english_letters = 0
word_lst = []

for i in range(5):
    i = input()
    word_lst.append(i)
    if i in letters:
        count_english_letters += 1
        

if count_english_letters > 0:
    print(count_english_letters)
    print(''.join(word_lst))
else: 
    print("No english chars!")