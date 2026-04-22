import math
import random

def faza_podzialu_tryw(n, s, k):
    if s < 0 or s > k-1:
        print("Liczba s poza zakresem.")
        return

    udzialy = [random.randint(0, k-1) for _ in range(n - 1)]
    suma_udzialy = sum(udzialy)
    s_n = (s - suma_udzialy) % k
    udzialy.append(s_n)

    print(f"Udziały do rozdania: {udzialy}")
    return udzialy

def faza_odtwarzania_tryw(udzialy, k):
    s = sum(udzialy) % k
    print(f"Odtworzony sekret: {s}")
    return s

def czy_pierwsza(n):
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True

def faza_podzialu_shamir(n, t, s, p):
    print("\nFAZA PODZIALU:")
    if p <= s or p <= n:
        print("Liczba p poza zakresem.")
        return
    if not czy_pierwsza(p):
        print("Liczba p musi być liczbą pierwszą.")
        return

    print("\nZatwierdzono liczbę p.")
    wspolczynniki = [s] + [random.randint(1, p-1) for _ in range(t - 1)]
    print(f"\nWygenerowane współczynniki: {wspolczynniki}")

    udzialy = []
    print("\nObliczone udziały:")
    for x in range(1, n + 1):
        s_i = 0
        for j, a_j in enumerate(wspolczynniki):
            s_i += a_j * (x ** j)

        s_i = s_i % p
        udzialy.append((x, s_i))
        print(f"Udział s_{x}: f({x}) = {s_i}")

    return udzialy

def faza_odtwarzania_shamir(udzialy, p, t):
    print("\nFAZA ODTWARZANIA:")
    if len(udzialy) < t:
        print("Za mała liczba udziałów.")
        return

    udzialy_shamir = udzialy[:t]
    print(f"\nZebrano wymaganą liczbę udziałów {t}: {udzialy_shamir}")

    s = 0
    for i in range(t):
        x_i, s_i = udzialy_shamir[i]
        licznik = 1
        mianownik = 1

        for j in range(t):
            if i != j:
                x_j, _ = udzialy_shamir[j]
                licznik = (licznik * (-x_j)) % p
                mianownik = (mianownik * (x_i - x_j)) % p

        odwrocony_mianownik = pow(mianownik, -1, p)
        l_i = (licznik * odwrocony_mianownik)
        s = (s + s_i * l_i) % p

    print(f"\nOdtworzony sekret: {s}")
    return s


if __name__ == "__main__":
    print("METODA TRYWIALNA")
    k = int(input("k = "))
    s = int(input("s = "))
    n = int(input("n = t = "))

    wygenerowane_udzialy_trywialne = faza_podzialu_tryw(n, s, k)
    if wygenerowane_udzialy_trywialne:
        odtworzony_sekret_trywialny = faza_odtwarzania_tryw(wygenerowane_udzialy_trywialne, k)

    print("\n------")
    print("\nSCHEMAT SHAMIRA")
    n = int(input("n = "))
    t = int(input("t = "))
    s = int(input("s = "))
    p = int(input("p = "))

    wygenerowane_udzialy_shamir = faza_podzialu_shamir(n, t, s, p)
    if wygenerowane_udzialy_shamir:
        faza_odtwarzania_shamir(wygenerowane_udzialy_shamir, p, t)