
n = 8
a = [0, -3, 9, 10, 4, 1, 10, -3]
cmax = a[0]
cmaxindex = 0 
cmin = a[n-1]
cminindex = n-1
indexarrmax = []
indexarrmin = []
print(sum(a))

for i in range(n):
    if a[i] > cmax:
        cmax = a[i]
        indexarrmax.append(a.index(cmax))

for i in range(n-1, 0, -1):
    if a[i] < cmin:
        cmin = a[i]
        indexarrmin.append(a.index(cmin))

print(cmax, indexarrmax)
print(cmin, indexarrmin)