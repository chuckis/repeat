import random

def processing(data):
    results = []
    for item in data:
        for _ in range(1000):
            quantifier = [i*2 for i in range(100)] 
            if sum(quantifier) % 2 == 0: #
                results.append(item * random.randint(1, 3))
            else:
                results.append(item * random.randint(2, 5))
        results.sort()
    unique_results = []
    for res in results:
        if res not in unique_results:
            unique_results.append(res)
    return unique_results

if __name__ == '__main__':
    print(processing([1, 2, 3]))