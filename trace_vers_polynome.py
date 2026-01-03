from sympy import symbols, sympify, expand


def change_car_en_liste(mot):
    if not mot:
        return []
    w = []
    for i in range(len(mot) - 1):
        if mot[i] != "'" and mot[i + 1] != "'":
            w.append(mot[i])
        elif mot[i] != "'" and mot[i + 1] == "'":
            w.append(mot[i] + mot[i + 1])
    if mot[-1] != "'":
        w.append(mot[-1])
    return w


def reduction_paire(w):
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(w) - 1:
            if (
                (w[i] == "X" and w[i + 1] == "X'")
                or (w[i] == "X'" and w[i + 1] == "X")
                or (w[i] == "Y" and w[i + 1] == "Y'")
                or (w[i] == "Y'" and w[i + 1] == "Y")
            ):

                # on supprime les deux et on incrémente pas i surtout !
                w.pop(i + 1)
                w.pop(i)
                changed = True
            else:
                i += 1
    return w


def reduction_cyclique(w):
    w = reduction_paire(w)
    changed = True
    while changed and len(w) >= 2:
        changed = False

        if w[0] == "X" and w[-1] == "X'":
            w = w[1:-1]
            changed = True
        elif w[0] == "X'" and w[-1] == "X":
            w = w[1:-1]
            changed = True
        elif w[0] == "Y" and w[-1] == "Y'":
            w = w[1:-1]
            changed = True
        elif w[0] == "Y'" and w[-1] == "Y":
            w = w[1:-1]
            changed = True

        if changed:
            w = reduction_paire(w)

    return w


def occurences(w, lettre):
    compteur = 0
    for elt in w:
        if elt == lettre:
            compteur += 1
    return compteur


def rotate(w):
    return [w[-1]] + w[:-1]


def inversion(w):
    new = []
    for elt in w:
        if elt == "X":
            new.append("X'")
        if elt == "Y":
            new.append("Y'")
        if elt == "X'":
            new.append("X")
        if elt == "Y'":
            new.append("Y")
    new.reverse()
    return new


def reduction_finale(w):
    n = len(reduction_cyclique(w))
    if n < 3 and max(occurences(w, elt) for elt in w) == 1:
        return reduction_cyclique(w)
    if len(w) == 4 and max(occurences(w, elt) for elt in w) == 1:
        return reduction_cyclique(w)
    else:
        star = "X"
        for elt in w:
            if occurences(w, elt) > occurences(w, star):
                star = elt
        while w[-1] != star:
            w = rotate(w)
        u1 = []
        j = 0
        while star not in u1:
            u1.append(w[j])
            j += 1
        u2 = w[j:]
        inverse_u2 = inversion(u2)
        u3 = u1 + inverse_u2
        return u1, u2, reduction_cyclique(u3)


def developper_polynome(expr_str):
    x, y, z = symbols("x y z")
    expr = sympify(expr_str)
    expr_dev = expand(expr)
    return str(expr_dev)


def trace(mot):
    # Si mot est une chaîne, on la convertit en liste
    if isinstance(mot, str):
        w = reduction_cyclique(change_car_en_liste(mot))
    else:
        # Si mot est déjà une liste (u1, u2, u3), on la passe directement
        w = reduction_cyclique(mot)
    n = len(w)
    if n == 0:
        return "2"
    if n == 1:
        if w[0] in ["X", "X'"]:
            return "x"
        elif w[0] in ["Y", "Y'"]:
            return "y"
    if n == 2 and max(occurences(w, elt) for elt in w) == 1:
        a, b = w
        if (a, b) in [("X", "Y"), ("Y", "X"), ("X'", "Y'"), ("Y'", "X'")]:
            return "z"
        if (a, b) in [("X", "Y'"), ("X'", "Y"), ("Y'", "X"), ("Y", "X'")]:
            return "x*y - z"
    if len(w) == 4 and max(occurences(w, elt) for elt in w) == 1:
        return "x**2 + y**2 + z**2 - x*y*z - 2"
    else:
        u1, u2, u3 = reduction_finale(w)
        return developper_polynome(f"({trace(u1)})*({trace(u2)}) - ({trace(u3)})")


print(reduction_paire(["X", "Y", "X'", "Y", "X", "Y'"]))

print(reduction_cyclique(["X", "Y", "X'", "Y", "X", "Y'"]))

print(occurences(["X", "Y", "X'", "Y", "X", "Y'"], "X"))

print(rotate(["X", "Y", "X'", "Y", "X", "Y'"]))
print(rotate(["X", "Y", "X'", "Y", "X", "Y'"])[1] == "X")

print(inversion(["X", "Y", "X'", "Y", "X", "Y'"]))

print(reduction_finale(["X", "Y", "X'", "Y", "X", "Y'"]))
print(reduction_finale(["X", "X"]))

print(trace("X'Y'X'YXYXX'"))
print(developper_polynome(trace("XY'XYX'XX")))
