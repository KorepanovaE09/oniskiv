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
    return (v[0] + alpha*(p[0] - x[0]) + betta*(g[0] - x[0]),
            v[1] + alpha*(p[1] - x[1]) + betta*(g[1] - x[1]))

def func_coord(x, v, t):
    return (x[0] + v[0] * t, x[1] + v[1] * t)

for i in range(m):
    x = random.uniform(0, 4*np.pi)
    y = random.uniform(0, 4*np.pi)
    points.append((x, y))

    speed.append((random.uniform(-1, 1),  random.uniform(-1, 1)))

best_points = points.copy()
g, g_value = calculate_g(points)

best_func = 100000
pred_func = 0

while abs(best_func - pred_func) > e:
    alpha, betta = alpha_betta()
    for i in range(N):
        points[i] = func_coord(points[i], speed[i], 1)
        speed[i] = func_speed(speed[i], alpha, betta, best_points[i], points[i], g)
        if func(points[i][0], points[i][1]) < func(best_points[i][0], best_points[i][1]):
            best_points[i] = points[i]
    g, g_value = calculate_g(points)

    if best_func > g_value: 
        pred_func = best_func
        best_func = g_value

print(f"Значение функции в точке {g} = {best_func}" )

