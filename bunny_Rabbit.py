import random


def answer(x, y):
    len_x = len(x)
    len_y = len(y)

    x = [str(value) for value in x]
    y = [str(value) for value in y]

    for num in range(len_y):
        y[num] = str(y[num])

    for num in range(len_x):
        try:
            x.remove(y[num])
        except ValueError:
            return int(y[num])
        except:
            return int(x[0])

x = [13, 5, 6, 2, 5]
y = [5, 2, 5, 13]
# answer(x, y)

import itertools


def answer(l):
    numbers = sorted(l, reverse=True)

    for L in range(len(numbers), 0, - 1):
        permutations = set([])
        combinations = set([])
        for subset in itertools.combinations(numbers, L):
            combinations.update([subset])
        for combination in combinations:
            for subset in itertools.permutations(combination, L):
                number = ""
                for num in subset:
                    number += str(num)
                number = int(number)
                permutations.update([number])
        permutations = sorted(permutations, reverse=True)
        for numbers in permutations:
            if(int(number) % 3 == 0):
                return int(number)

    return 0

l = []
for x in range(9):
    l.append(random.randint(0, 9))
print(answer(l))
