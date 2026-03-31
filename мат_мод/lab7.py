import random

distance = [[0, 6, 24, 4, 40, 38],
          [6, 0, 7, 5, 30, 32],
          [24, 7, 0, 34, 27, 31],
          [4, 5, 34, 0, 23, 25],
          [40, 30, 27, 23, 0, 4],
          [38, 32, 31, 25, 4, 0]]

def route_length(route):
    total = 0
    for i in range(len(route)-1):
        total += distance[route[i]][route[(i + 1)]]
    return total

#Генерация особей
def create_individual():
    points = list(range(len(distance))) # список всех городов, ещё не посещенных городов
    route = [] # хранит порядок посещения городов
    current = random.choice(points)
    route.append(current)
    points.remove(current)

    while points:
        next_city = random.choice(points)
        route.append(next_city)
        points.remove(next_city)

    return route

def pointsSwap(points):
    first = points[0]
    rest = points[1:]
    random.shuffle(rest)
    new_points = [first] + rest
    return new_points

epochs = 25
best_f = 1000000000000000000000
best_individ = []

for epoch in range(epochs):
    population = []
    fitness = []
    size = 10

    for i in range(0, size):
        individ = create_individual()
        population.append(individ)
        fitness.append(route_length(individ))

    sorted_indices = sorted(range(size), key = lambda i: fitness[i])
    selected = sorted_indices[:int(size/2)]

    for i in range(len(selected)):
        selected[i] += 1

    population_new = []

    for i in selected:
        population_new.append(population[i-1])

    for k in range(len(population_new)):
        for l in range(10):
            current_individ = pointsSwap(population_new[k])
            current_f = route_length(current_individ)
            if current_f < best_f:
                best_f = current_f
                best_individ = current_individ

    print(f"Эпоха {epoch+1}: лучший = {best_f}")


print("\nЛучший маршрут:")
print(best_individ)
print(route_length(best_individ))
