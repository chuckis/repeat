def odds(data):

    filtered_data = filter(lambda x: x % 2, data)
    l1 = list(filtered_data)
    l2 = list(filtered_data)

    print("l1 = ", l1)
    print("l2 = ", l2)
    if not list(filtered_data):
        print("No")
    else:
        for i in list(filtered_data):
            print(i)
        
    print()

if __name__=='__main__':
    print()
    print(odds([4]))
    print(odds([2,4,6]))
    print(odds([]))

