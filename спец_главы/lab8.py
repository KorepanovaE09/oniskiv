# 1 - red
# 2 - blue
# 3 - yellow

shars=[1, 2, 3, 3, 2, 2, 2, 3, 1, 1, 1, 2, 2, 3, 3, 3, 1, 2, 1, 1]

def probability(conteiner):
    n1, n2, n3 = 0, 0, 0
    for i in conteiner:
        if i == 1: n1 += 1
        if i == 2: n2 += 1
        if i == 3: n3 += 1

    p1 = n1 / len(conteiner)
    p2 = n2 / len(conteiner)
    p3 = n3 / len(conteiner)
    
    return p1, p2, p3

def Djunny(conteiner):
    p1, p2, p3 = probability(conteiner)

    return p1*(1-p1) + p2*(1-p2) + p3*(1-p3)

def Djunny_score(conteiner):
    d = Djunny(conteiner)
    return abs(d - 0.5)

def koeff(conteiner):
    n1, n2, n3 = 0, 0, 0

    # k_left, k_middle, k_right = 0, 0, 0
    # for i in conteiner:
    #     if i == 1: n1 += 1
    #     if i == 2: n2 += 1
    #     if i == 3: n3 += 1
    
    return len(conteiner) / len(shars), n2 / len(shars), n3 / len(shars)


def delta_Djunny(H_rod, H_left, H_right, H_middle, conteiners):
    k_left = len(conteiners[0]) / len(shars)
    k_middle = len(conteiners[1]) / len(shars)
    k_right = len(conteiners[2]) / len(shars)

    return H_rod-(k_left * H_left + k_middle * H_middle + k_right * H_right)


containers = []
start = 0

H_rod = Djunny(shars)   # <-- ОБЩАЯ энтропия

for _ in range(2):
    current_container = []
    H_best = -1
    best_end = start

    for i in range(start, len(shars)-2):   # <-- важно!
        current_container.append(shars[i])

        if len(current_container) < 3:
            continue

        # временно делим остаток на 2 части
        rest = shars[i+1:]
        rest = shars[i+1:]

        if len(containers) == 0:
            # первая итерация (как было)
            mid = len(rest)//2
            left = current_container
            middle = rest[:mid]
            right = rest[mid:]
        else:
            # вторая итерация (ВОТ ГЛАВНОЕ ИСПРАВЛЕНИЕ)
            left = containers[0]           # фиксирован
            middle = current_container     # растёт
            right = rest                   # остаток

        if len(middle) < 1 or len(right) < 1:
            continue

        H_left = Djunny(left)
        H_middle = Djunny(middle)
        H_right = Djunny(right)

        H_current = delta_Djunny(H_rod, H_left, H_middle, H_right,
                                [left, middle, right])

        if H_current >= H_best:
            H_best = H_current
            best_end = i
        else:
            current_container.pop()
            break

    containers.append(shars[start:best_end+1])
    start = best_end + 1

containers.append(shars[start:])


for i in containers:
    print(f"{Djunny(i)}: {i}")

print(H_best)
# print(delta_Djunny(H_rod, Djunny([1, 2, 3, 3, 2, 2, 2]),
#                    Djunny([3, 1, 1, 1, 2, 2, 3, 3, 3]),
#                    Djunny([ 1, 2, 1, 1]),
#                    [[1, 2, 3, 3, 2, 2, 2], [3, 1, 1, 1, 2, 2, 3, 3, 3], [ 1, 2, 1, 1]]))
print(containers)