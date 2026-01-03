import numpy as np
import cmath
import matplotlib.pyplot as plt


def calcul_trace(A):
    s = 0
    for i in range(len(A)):
        s += A[i][i]
    return s


def lemme_fourche(A, B, max_iter=1000):
    A = np.array(A, dtype=complex)
    B = np.array(B, dtype=complex)

    a = calcul_trace(A)
    b = calcul_trace(B)
    x = calcul_trace(np.dot(A, B))

    iterations = 0
    while (abs(a) > 2 and abs(b) > 2 and abs(x) > 2) and iterations < max_iter:
        iterations += 1
        c1 = b * x - a
        c2 = a * x - b
        c3 = a * b - x

        if abs(c1) < abs(a):
            a = c1
        elif abs(c2) < abs(b):
            b = c2
        elif abs(c3) < abs(x):
            x = c3
        else:
            break  # aucune amélioration possible → on arrête

    return min([a, b, x], key=abs)


print(calcul_trace([[1, 0, 8], [0, 9, 7], [5, 7, 9]]))
print(lemme_fourche([[560, 0], [56, 3j]], [[3, 89897], [22, 111]]))


def lemme_fourche_complexes(a, b, x, max_iter=5000):
    iterations = 0
    while (abs(a) > 2 and abs(b) > 2 and abs(x) > 2) and iterations < max_iter:
        iterations += 1
        c1 = b * x - a
        c2 = a * x - b
        c3 = a * b - x
        if abs(c1) < abs(a):
            a = c1
        elif abs(c2) < abs(b):
            b = c2
        elif abs(c3) < abs(x):
            x = c3
        else:
            break
    return a, b, x


print(lemme_fourche_complexes(3476, 89, 39))


def kappa(a, b, x):
    return a**2 + b**2 + x**2 - a * b * x - 2


print(kappa(2, 3, 4))


def solve_quadratic(a, b, c):
    # Resout ax^2 + bx + c = 0
    if a == 0:
        raise ValueError("Ce n'est pas un polynôme du second degré (a=0).")
    delta = b**2 - 4 * a * c
    x1 = (-b + cmath.sqrt(delta)) / (2 * a)
    x2 = (-b - cmath.sqrt(delta)) / (2 * a)

    return x1, x2


print(solve_quadratic(1, 2, 1))
print(solve_quadratic(1, 0, 1))

# debut programme
# generer trois complexes
x = 0
liste_images = []
for i in range(-20, 20):
    liste_a = []
    liste_b = []
    liste_x = []
    liste_min = []
    for j in range(0, 5000):
        aj = np.random.uniform(-100, 100) + 1j * np.random.uniform(-100, 100)
        bj = np.random.uniform(-100, 100) + 1j * np.random.uniform(-100, 100)
        liste_a.append(aj)
        liste_b.append(bj)
        x1, x2 = solve_quadratic(1, -aj * bj, aj**2 + bj**2 - 2 - i)
        xj = x1 if abs(x1) > abs(x2) else x2
        liste_x.append(xj)
        afj, bfj, xfj = lemme_fourche_complexes(aj, bj, xj)
        liste_min.append(min(abs(afj), abs(bfj), abs(xfj)))
        v_finale = max(liste_min)
    liste_images.append(v_finale)
print(liste_images)


kappas = list(range(-20, 20))  # axe horizontal
Y = [z for z in liste_images]  # ce que tu veux tracer

plt.plot(kappas, Y)
plt.xlabel("kappa")
plt.ylabel("min(|a|,|b|,|x|)")
plt.grid(True)
plt.show()
