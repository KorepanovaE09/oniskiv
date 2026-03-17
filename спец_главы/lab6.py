import numpy as np
import matplotlib.pyplot as plt

k1 = 0.2
k2 = 0.15
k3 = 0.27
A = 3

def ksi(k):
    return np.random.uniform(0, 1) * k

def y_1(A, t):
    return (A*np.sin(2*np.pi*t) + ksi(k1))

def y_2(A, t):
    return (A*np.sin(2*np.pi*t) + t + ksi(k2))

def y_3(A, t):
    return (A*np.sin(np.pi*t) + ksi(k3))

def integral(f, a, b, n):
    h = (b-a)/n
    total = 0.0
    for i in range(n):
        x_mid = a+(i+0.5)*h
        total+=f(x_mid)
    return total*h

#============================
# Вычисление коэффициентов Хаара
#============================

def h_1(t):
    if t >= 0 and t < 1/2: return 1
    elif t >= 1/2 and t < 1: return -1
    else: return 0

def h_2(t):
    return (np.sqrt(2) * h_1(2 * t))
def h_3(t):
    return (np.sqrt(2) * h_1(2 * t - 1))
def h_4(t):
    return (2 * h_1(4 * t))
def h_5(t):
    return (2 * h_1(4 * t - 1))
def h_6(t):
    return (2 * h_1(4 * t - 2))
def h_7(t):
    return (2 * h_1(4 * t - 3))

haar = [h_1, h_2, h_3, h_4, h_5, h_6, h_7]

c_1 = []
for h in haar:
    c_1.append(integral(lambda t: y_1(A, t)*h(t), 0, 1, 1000))

print(c_1)

c_2 = []
for h in haar:
    c_2.append(integral(lambda t: y_2(A, t)*h(t), 0, 1, 1000))
print(c_2)


c_3 = []
for h in haar:
    c_3.append(integral(lambda t: y_3(A, t)*h(t), 0, 1, 1000))
print(c_3)


#============================
# Нормировка 
#============================

norm = 0
for j in c_1:
    norm += j**2 

c_1_norm = []

for j in c_1:
    c_1_norm.append(j / np.sqrt(norm))

norm = np.sqrt(sum(j**2 for j in c_2))
c_2_norm = [j / norm for j in c_2]

norm = np.sqrt(sum(j**2 for j in c_3))
c_3_norm = [j / norm for j in c_3]

cos_1_2 = sum(c_1_norm[j] * c_2_norm[j] for j in range(7))
cos_1_3 = sum(c_1_norm[j] * c_3_norm[j] for j in range(7))
cos_2_3 = sum(c_2_norm[j] * c_3_norm[j] for j in range(7))

MS_1_2 = 1 - cos_1_2
MS_1_3 = 1 - cos_1_3
MS_2_3 = 1 - cos_2_3

print(f"MS_1_2: {MS_1_2}")
print(f"MS_1_3: {MS_1_3}")
print(f"MS_2_3: {MS_2_3}")


# ============================
# Графики сигналов
# ============================

t_vals = np.linspace(0, 1, 1000)

y1_vals = [y_1(A, t) for t in t_vals]
y2_vals = [y_2(A, t) for t in t_vals]
y3_vals = [y_3(A, t) for t in t_vals]

plt.figure()

plt.plot(t_vals, y1_vals, label="y1(t) = A sin(2πt) + Ѯ1(t)")
plt.plot(t_vals, y2_vals, label="y2(t) = A sin(2πt) + t + Ѯ2(t)")
plt.plot(t_vals, y3_vals, label="y3(t) = A sin(πt) + Ѯ3(t)")

plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("Временные ряды с шумом ξ(t)")
plt.legend()
plt.grid(True)

plt.show()
