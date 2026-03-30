import numpy as np
import random

fitness = [4.0, 3.3, 9.0, 5.0, 2.0, 8, 2.1, 12, 7.1, 4.6, 5.8, 9.1, 1.3, 8.2]

min_fit = min(fitness)
max_fit = max(fitness)

a = 10
b = 30

k = (b - a)/(max_fit - min_fit)
l = a - k * min_fit

fitness_new = []

for i in fitness:
    fitness_new.append(round(k*i+l,3))

print(f'Фитнесс функция до масштабирования {fitness}')
print(f'Фитнесс функция после масштабирования {fitness_new}')

def P_i(fitness):
    doli = []
    for i in fitness:
        doli.append(round(i/sum(fitness),3))
    return doli

print(f"Доли до масштабирования {P_i(fitness)}")
print(f'Доли после масштабирования {P_i(fitness_new)}')

# 1. Рулеточная селекция
def ruletka(fitness):
    q = []
    cumulative = 0
    for prob in P_i(fitness):
        cumulative += prob
        q.append(cumulative) # кумулятивная вероятность

    selected = []
    for i in range(len(fitness)):
        r = random.random()
        for j in range(len(q)):
            if r <= q[j]:
                selected.append(j+1)
                break
    return selected

print("Рулеточная селекция до масштабирования", ruletka(fitness))
print("Рулеточная селекция после масштабирования", ruletka(fitness_new))
