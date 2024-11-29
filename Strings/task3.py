letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

input_chars = [] 

for i in range(5):
    i = input()
    input_chars.append(i)

print(f'{min(input_chars)} {ord(min(input_chars))}')
print(f'{max(input_chars)} {ord(max(input_chars))}')
