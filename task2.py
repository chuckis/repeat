
n = 8
# a = list(map(int, input().split()))
a = [0, 4, 9, -1, 4, 1, -1, -3]

k=[]
p=[]

for i in range(n):
    if a[i] < 0:
        k.append(i+1)
    elif a[i] > 0:
        p.append(i+1)        

print(*p)
print(*k[::-1])