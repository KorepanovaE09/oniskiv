import random
import math
import matplotlib.pyplot as plt

points = [(1, 1), (3, 7), (5, 2), (4, 5), (3, 3), (8, 4), (9, 1), (6, 8), (6, 4), (9, 7)]
m = len(points)

def func(points):
    m = len(points)
    sum = 0
    for i in range(m - 1):
        sum += math.sqrt((points[i+1][0] - points[i][0])**2 + (points[i+1][1] - points[i][1])**2)
    sum += math.sqrt((points[m-1][0] - points[0][0])**2 + (points[m-1][1] - points[0][1])**2)
    return sum

def pointsSwap(points):
    first = points[0]
    rest = points[1:]
    random.shuffle(rest)
    new_points = [first] + rest
    return new_points

def gibbs(f_delta, t):
    if t < 1e-10:
        return 0
    return math.exp(-f_delta / t)

# Три разных t
def t_schedule1(k):
    return 100 * 0.1 / k

def t_schedule2(k):
    return 100 / math.log(k + 1)

def t_schedule3(k):
    t = 100 * (0.95 ** k)
    return max(t, 1e-10)

schedules = [t_schedule1, t_schedule2, t_schedule3]
schedule_names = ["t = 100*0.1/k", "t = 100/ln(k+1)", "t = 100*(0.95^k)"]
best_overall_path = None
best_overall_dist = float('inf')

for idx, t_schedule in enumerate(schedules):
    print(f"\n=== {schedule_names[idx]} ===")
    
    points_copy = points.copy()
    f_current = func(points_copy)
    finish_posled = points_copy.copy()
    k = 1
    iterations = 0
    best_f = f_current
    best_path = points_copy.copy()
    no_improve = 0
    
    while True:
        iterations += 1
        t = t_schedule(k)
        k += 1
        posled = pointsSwap(points_copy)
        f_next = func(posled)
        f_delta = f_next - f_current

        if f_delta < 0:
            f_current = f_next
            points_copy = posled
            finish_posled = posled
            if f_current < best_f:
                best_f = f_current
                best_path = posled.copy()
                no_improve = 0
            else:
                no_improve += 1
        else:
            r = random.random()
            if r < gibbs(f_delta, t):
                f_current = f_next
                points_copy = posled
                finish_posled = posled
            else:
                no_improve += 1
        
        if no_improve > 50000:
            break
        
        if iterations > 200000:
            break
    
    print(f"Количество итераций: {iterations}")
    print(f"Лучшее расстояние: {best_f}")
    print(f"Путь: {best_path}")
    
    if best_f < best_overall_dist:
        best_overall_dist = best_f
        best_overall_path = best_path

# Отрисовка лучшего пути
if best_overall_path:
    plt.figure(figsize=(10, 8))
    
    # Подготовка координат для отрисовки (замыкаем маршрут)
    x_coords = [p[0] for p in best_overall_path] + [best_overall_path[0][0]]
    y_coords = [p[1] for p in best_overall_path] + [best_overall_path[0][1]]
    
    # Рисуем маршрут
    plt.plot(x_coords, y_coords, 'b-', linewidth=2, marker='o', markersize=8, markerfacecolor='red', markeredgecolor='black')
    
    # Подписываем точки
    for i, (x, y) in enumerate(best_overall_path):
        plt.text(x, y, f' {i+1}', fontsize=12, fontweight='bold')
    
    plt.title(f'Лучший найденный маршрут\nРасстояние: {best_overall_dist:.6f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.show()
