# здесь пишем все что связано с входными данными (input, map, split...)
x, p, q, r = 10, 1, 2, 3

# создаем массив заполненный нулями. Это способ обойти ошибку "list index out of range"
a = [0]*21 

a[1] = x

for i in range(1, 21):
    a[i] = a[i - 1]*(i-10)+x
     
print(a[p]+a[q]+a[r]) #440
