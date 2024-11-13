n = int(input())
A = list(map(int, input().split()))
k = list()
p = list()

for i in range(n):
    if A[i] < 0:
        k.append(i + 1)
    elif A[i] > 0:
        p.append(i + 1)

print(*p)
print(*k[::-1])