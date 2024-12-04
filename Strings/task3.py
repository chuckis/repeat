input_chars = [] 

for i in range(5):
    i = input()
    if i.isalpha(): # Эта проверка позволяет вводить меньше чем 5 букв и проверяет, буква ли введена.
        input_chars.append(i)

if input_chars:
    print(f'{min(input_chars)} {ord(min(input_chars))}')
    print(f'{max(input_chars)} {ord(max(input_chars))}')