import numpy as np
import random

N =  10
m = 10
e = 0.000001
best_points = []
points = []
speed = []

def func(x, y):
    return -(1 + np.sin(x)**2)*(1 + np.sin(y)**2)

def calculate_g(points):
    best_func = 10000000
    best_point = []
    for i in range(10):
        current_func = func(points[i][0], points[i][1])
        if current_func < best_func: 
            best_func = current_func
            best_point = points[i][0], points[i][1]
    return best_point, best_func

def alpha_betta():
    alpha = random.uniform(0, 1)
    betta = 1 - alpha
    
    return alpha, betta

def func_speed(v, alpha, betta, p, x, g):
    return (v + alpha*(p - x) + betta*(g - x))

def func_coord(x, v, t):
    return (x + v*t)

for i in range(m):
    x = random.uniform(0, 4*np.pi)
    y = random.uniform(0, 4*np.pi)
    points.append((x, y))

    speed.append(random.uniform(0, np.pi/2))
best_points = points

g, func = calculate_g(points)

best_func = 100000
pred_func = 0

while np.abs(best_func - pred_func) > e:
    for i in range(N):
        alpha, betta = alpha_betta()
        for j in range(m):
            points[j] = func_coord(points[j], speed[j], i + 1)
            speed[j] = func_speed(speed[j], alpha, betta, best_points[j], points[j], g)
            if func(points[j][0], points[j][1]) < func(best_points[j][0], best_points[j][1]):
                best_points[j] = points[j]
        g, func = calculate_g(points)

        if best_func > func: 
            pred_func = best_func
            best_func = func

print(f"Значение функции в точке {g} = {best_func}" )

