# n = 10
# a = [10, 2, 4, 5, -2, 6, 10, -1, 0, -2]
#----------------------------------------
n = 4
a = [-2, 2, 0, -3]
#----------------------------------------
curr_max = a[0]
curr_min = a[n-1]
curr_ind = 0
max_ind, min_ind = 0, n

print(sum(a)) # TODO

for i in range(n):
    curr_ind = i
    re_ind = n - i # этот индекс для "обратного" прохода по списку
    if curr_ind > max_ind and a[i] >= curr_max:
        curr_max = a[i]
        max_ind = curr_ind
    if re_ind < min_ind and a[n-i] <= curr_min:
        curr_min = a[n-i]
        min_ind = re_ind    
    
print(curr_max, max_ind+1)
print(curr_min, min_ind+1)
