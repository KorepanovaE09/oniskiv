import numpy as np
import matplotlib.pyplot as plt
import random

S = 50
k = 100000
P = 10
e = 5
delta = 1
sh = 0

# fitness хранит значения [целевая функция, x, y]
fitness = []


def funk(x, y):
    a = 1 / (1 + (x - 2)**2 + (y - 10)**2)
    b = 1 / (2 + (x - 10)**2 + (y - 15)**2)
    c = 1 / (2 + (x - 18)**2 + (y - 4)**2)

    return a + b + c


def filter_delta(points):
    filter = []

    for i in points:
        f, x, y = i
        bad_point = False

        for j in filter:
            _, x2, y2 = j

            if abs(x - x2) < delta and abs(y - y2) < delta:
                bad_point = True
                break
        if not bad_point: filter.append(i)

    return filter

def generate_points(points, count):
    new_points = []

    for i in points:
        f, x0, y0 = i

        for _ in range(count):
            x = random.uniform(x0 - delta, x0 + delta)
            y = random.uniform(y0 - delta, y0 + delta)

            new_points.append([funk(x, y), x, y])
    return new_points


for i in range(50):
   x = random.uniform(0, 20) 
   y = random.uniform(0, 20) 
   fitness.append([funk(x, y), x, y])

fitness.sort(key=lambda x: x[0], reverse=True)

elite = fitness[:e]
promising = fitness[e:P]

while sh < k:
    elite = filter_delta(elite)
    promising = filter_delta(promising)

    elite.extend(generate_points(elite, 20))
    promising.extend(generate_points(promising, 5))

    fitness = elite + promising

    fitness.sort(key=lambda x: x[0], reverse=True)

    elite = fitness[:e]
    promising = fitness[e:P]

    sh += 1

print(elite[0])
