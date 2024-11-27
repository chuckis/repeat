# n = 10
# a = [1, 2, 2, 2, 2, 2, 1, 2, 2, 2]
#-----------------------------------
n = 12
a = [1, 3, 3, 1, 3, 2, 1, 1, 2, 2, 1, 3]
#-----------------------------------
curr_max = a[0]
curr_min = a[0]
ind_curr_max = 0
ind_curr_min = 0
min_count = 0
max_count = 0
min_indexes_lst =[]
max_indexes_lst = []

for i in range(n):
    if i >= ind_curr_min and a[i] <= curr_min:
        curr_min = a[i]
        ind_curr_min = i
        min_count += 1
        min_indexes_lst.append(ind_curr_min+1)

    if i > ind_curr_max and a[i] >= curr_max:
        curr_max = a[i]
        ind_curr_max = i
        max_count += 1
        max_indexes_lst.append(ind_curr_max+1)


print(max_count)
print(max_indexes_lst)
print(min_count)
print(min_indexes_lst)