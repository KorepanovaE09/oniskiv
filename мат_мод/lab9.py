import random

x0 = 3
y0 = 4
b = 5

def func(x, y):
    return (x - x0)**2 + (y - y0)**2 + b

s = 10
colony = []
speed = []
fitness = []
steps = []
coord_start = []

for i in range(s):
    x = random.uniform(0, 10)
    y = random.uniform(0, 10)
    colony.append((x, y))
    speed.append((random.uniform(-1, 1), random.uniform(-1, 1)))
    fitness.append(func(x, y))
    steps.append(0)
    coord_start.append((x, y))

print("Начальные fitness:", fitness)

def lambd(lambd0):
    return lambd0 * random.uniform(0, 1)

def coord(bac_coord, lambd_val, bac_speed):
    length = (bac_speed[0]**2 + bac_speed[1]**2) ** 0.5 
    return (bac_coord[0] + lambd_val * bac_speed[0] / length,
            bac_coord[1] + lambd_val * bac_speed[1] / length)

fitness_best = fitness.copy()
lambd0 = 0.2

for j in range(100):
    for i in range(s):
        # Вычисляем новую координату
        new_coord = coord(colony[i], lambd(lambd0), speed[i])
        new_fitness = func(new_coord[0], new_coord[1])
        
        # Сравниваем с лучшим значением
        if new_fitness < fitness_best[i]:
            fitness_best[i] = new_fitness
            colony[i] = new_coord 
            steps[i] += 1
        else:
            speed[i] = (random.uniform(-1, 1), random.uniform(-1, 1))

idx = fitness_best.index(min(fitness_best))

print("Лучшие fitness: ", min(fitness_best))
print("Лучшая бактeрия: ", colony[idx])
print("Число шагов: ", steps[idx])
print("Стартовая точка: ", coord_start[idx])
