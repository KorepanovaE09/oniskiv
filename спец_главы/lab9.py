import numpy as np
import matplotlib.pyplot as plt

# =======================
# ДАННЫЕ
# =======================
chelovek = [(46, 50, 2, 2.0, 0), 
            (36, 42, 2, 1.5, 0), 
            (34, 40, 3, 1.4, 0),
            (28, 45, 1, 0.5, 1),
            (24, 30, 0, 0.3, 1),
            (21, 25, 0, 0.1, 1),
            (35, 40, 1, 0.5, 0),
            (48, 45, 2, 0.35, 0),
            (35, 40, 2, 0.4, 1),
            (37, 54, 2, 0.45, 0),
            (18, 25, 0, 5.0, 1),
            (24, 30, 1, 0.4, 1),
            (33, 45, 2, 3.0, 0),
            (45, 50, 1, 4.0, 1)]

chelovek_test = [(38, 50, 2, 2.5, 0),
                  (24, 25, 1, 5.0, 1),
                  (42, 30, 3, 4.0, 0),
                  (36, 47, 2, 3.0, 0),
                  (23, 35, 0, 1.5, 1),
                  (40, 45, 2, 4.5, 0)]

names = ["возраст", "доход", "дети", "недвижимость"]

# =======================
# ПОДГОТОВКА ДАННЫХ
# =======================
data = np.array(chelovek)
X = data[:, :4]
y = data[:, 4]

# важность признаков (по корреляции)
corrs = []
for i in range(4):
    corr = np.corrcoef(X[:, i], y)[0, 1]
    corrs.append((i, abs(corr)))

corrs_sorted = sorted(corrs, key=lambda x: x[1], reverse=True)
order = [x[0] for x in corrs_sorted]

print("Порядок признаков:", [names[i] for i in order])

# перестановка колонок в соответствии с важностью 
X_sorted = X[:, order]
names_sorted = [names[i] for i in order]

data = np.column_stack((X_sorted, y))


class Node:
    def __init__(self, column=None, value_split=None, left=None, right=None, value=None, prob=None):
        self.column = column
        self.value_split = value_split
        self.left = left
        self.right = right
        self.value = value
        self.prob = prob


def rss(y):
    if len(y) == 0:
        return 0
    return np.sum((y - np.mean(y)) ** 2)


# =======================
# Поиск лучшего разделения на контейнеры
# =======================

def best_split(data, column):
    # сортируем столбец
    sorted_data = data[data[:, column].argsort()]

    best_score = float("inf")
    best_value_split = None

    for i in range(1, len(sorted_data)):
        left = sorted_data[:i]
        right = sorted_data[i:]

        y_left = left[:, 4]
        y_right = right[:, 4]

        score = (len(left)/len(data)) * rss(y_left) + \
                (len(right)/len(data)) * rss(y_right)

        if score < best_score:
            best_score = score
            best_value_split = sorted_data[i, column] 
    
    best_value_split

    return best_value_split

# =======================
# Построение дерева
# =======================

def build_tree(data, column_order, depth=0):

    y = data[:, 4]
    p = np.mean(y)

    # если контейнер получился чистым, то делаем лист и дальше не делим
    if len(np.unique(y)) == 1:
        return Node(value=int(y[0]), prob=p)

    # ограничение глубины
    if depth >= 4:
        return Node(value=int(np.round(p)), prob=p)

    column = depth  # уже отсортированные признаки
    value_split = best_split(data, column)

    if value_split is None:
        return Node(value=int(np.round(p)), prob=p)

    left = data[data[:, column] < value_split]
    right = data[data[:, column] >= value_split]

    if len(left) == 0 or len(right) == 0:
        return Node(value=int(np.round(p)), prob=p)

    return Node(
        column=column,
        value_split=value_split,
        left=build_tree(left, column_order, depth+1),
        right=build_tree(right, column_order, depth+1),
        prob=p
    )


# =======================
# Расчет ответа 
# =======================

def predict(node, x):
    if node.value is not None:
        return node.value, node.prob

    if x[node.column] < node.value_split:
        return predict(node.left, x)
    else:
        return predict(node.right, x)
    

# =======================
# ВИЗУАЛИЗАЦИЯ
# =======================
def plot_tree(node, x=0, y=0, dx=1.5, dy=1.5):
    if node.value is not None:
        plt.text(x, y, f"{node.value}\np={node.prob:.2f}",
                 ha="center", bbox=dict(boxstyle="round", facecolor="lightgreen"))
        return

    label = f"{names_sorted[node.column]}\n< {node.value_split:.2f}"
    plt.text(x, y, label, ha="center",
             bbox=dict(boxstyle="round", facecolor="lightblue"))

    if node.left:
        plt.plot([x, x-dx], [y, y-dy], 'k-')
        plot_tree(node.left, x-dx, y-dy, dx*0.6, dy)

    if node.right:
        plt.plot([x, x+dx], [y, y-dy], 'k-')
        plot_tree(node.right, x+dx, y-dy, dx*0.6, dy)

def draw_tree(tree):
    plt.figure(figsize=(12,7))
    plot_tree(tree)
    plt.axis("off")
    plt.show()



tree = build_tree(data, order)
draw_tree(tree)



print("\n===== ТЕСТ =====")

correct = 0
for t in chelovek_test:
    x = np.array([t[i] for i in order])
    pred, prob = predict(tree, x)

    print(t[:4], "=>", "НЕЛЬЗЯ" if pred == 1 else "МОЖНО", f"(p={prob:.2f})")

    if pred == t[4]:
        correct += 1

acc = correct / len(chelovek_test)
print(f"\nAccuracy: {acc:.2f} ({correct}/{len(chelovek_test)})")



while True:
    try:
        x_raw = [
            float(input("Возраст: ")),
            float(input("Доход: ")),
            float(input("Дети: ")),
            float(input("Недвижимость: "))
        ]

        x = np.array([x_raw[i] for i in order])

        pred, prob = predict(tree, x)

        print("\nРЕЗУЛЬТАТ:", "НЕЛЬЗЯ КРЕДИТ" if pred == 1 else "МОЖНО КРЕДИТ")
        print(f"Вероятность (класс 1): {prob:.2f}\n")

        if input("Продолжить? (y/n): ") != "y":
            break

    except ValueError:
        print("Ошибка ввода!\n")