import numpy as np
import matplotlib.pyplot as plt

def golden_search(a, b, tol, f):
    """
    Leitar að minnsta gildi falls f á bilinu [a, b]
    með gullsniðsaðferð.
    Skilar (x_min, f(x_min), iterations).
    """
    phi = (np.sqrt(5) - 1) / 2  # ≈ 0.618

    # Upphafspunktar (x1, x2) og fallgildi þeirra
    x1 = a + (1 - phi) * (b - a)
    x2 = a + phi * (b - a)
    f1 = f(x1)
    f2 = f(x2)

    it = 0
    # (b-a)/2 > tol
    while (b - a) / 2 > tol:
        if f1 < f2:
            # minnsta gildið er á bilinu [a, x2]
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (1 - phi) * (b - a)
            f1 = f(x1)
        else:
            # minnsta gildið er á bilinu [x1, b]
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + phi * (b - a)
            f2 = f(x2)

        it += 1

    x_min = (a + b) / 2
    return x_min, f(x_min), it

def f_c1(c1):
    """
    Skilar f(c1) = max Re(s_i(c1)) þar sem s_i eru tvintrætur
    eiginjöfnunnar (raunhluti mestur).
    """
    # Stuðlar margliðunnar fyrir tiltekið c1
    a4 = 2.0
    a3 = 2.0 * c1 + 3.0
    a2 = 35.0 + c1
    a1 = 5.0 * c1 + 10.0
    a0 = 50.0

    coeffs = [a4, a3, a2, a1, a0]

    # Reiknum rætur
    roots = np.roots(coeffs)

    # Veljum tvintrætur (með einhverju ímyndað gildi)
    complex_roots = [r for r in roots if abs(r.imag) > 1e-10]

    # Ef eitthvað klikkar og engar tvinnölutrætur finnast, notum bara allar
    if not complex_roots:
        dominant = max(roots, key=lambda z: z.real)
    else:
        dominant = max(complex_roots, key=lambda z: z.real)

    return dominant.real
if __name__ == "__main__":
    # Leit á bilinu [0, 30] með nákvæmni 1e-6
    a = 0.0
    b = 30.0
    tol = 1e-6

    c1_star, f_star, n_it = golden_search(a, b, tol, f_c1)

    print(f"Best c1 ≈ {c1_star:.6f}")
    print(f"f(c1) ≈ {f_star:.6f}")
    print(f"Fjöldi ítrekana: {n_it}")

cs = np.linspace(0, 30, 301)
vals = [f_c1(c) for c in cs]

plt.plot(cs, vals)
plt.axvline(c1_star, linestyle="--")  # sýna optimum
plt.xlabel("c1")
plt.ylabel("f(c1) = max Re(s_i(c1))")
plt.title("Raunhluti ríkjandi tvinntölurótar sem fall af c1")
plt.grid(True)
plt.show()
