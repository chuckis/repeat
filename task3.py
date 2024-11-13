n = 8
a = [1, 140, 1, 20, -20, -30001, -305, 3000]
p, q, r = 7, 2, -3

res = []
count = 0

for i in range(n):
    if (p!=0 and a[i]%p==0) or (q!=0 and a[i]%q==0) or (r!=0 and a[i]%r==0):
        count += 1
        res.append(a[i])

print(count)

if res:
    print(res[::-1])
else:
    print()