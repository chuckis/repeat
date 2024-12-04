letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
count_english_letters = 0
word_lst = []

for i in range(5):
    i = input()
    if i and i in letters: # добавил проверку на пустой ввод (энтер)
        word_lst.append(i)
        count_english_letters += 1
        

if count_english_letters > 0:
    print(count_english_letters)
    print(''.join(word_lst))
else: 
    print("No english chars!")