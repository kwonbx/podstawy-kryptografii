import random

def checkPrime(x):
    for i in range(2, x):
        if x % i == 0:
            return False
    return True

def findPrimeFactors(n):
    factors = []
    d = 2
    num = n

    while d * d <= num:
        if num % d == 0 and checkPrime(d):
            factors.append(d)
            while num % d == 0:
                num //= d
        d += 1
    if num > 1:
        factors.append(num)
    return factors


def findPrimitiveRoot(n):
    phi = n - 1
    factors = findPrimeFactors(phi)

    for g in range(2, n):
        isPrimitive = True
        for q in factors:
            if pow(g, phi // q, n) == 1:
                isPrimitive = False
                break
        if isPrimitive:
            return g
    return None


n = 235111
print("n = " + str(n))

g = findPrimitiveRoot(n)
print("g = " + str(g))

x = random.randint(1, n)
X = pow(g, x, n)

y = random.randint(1, n)
Y = pow(g, y, n)

k_A = pow(Y, x, n)
k_B = pow(X, y, n)

print("\nA = " + str(k_A))
print("B = " + str(k_B))

if k_A == k_B:
    print("\nKlucze są identyczne!")
else:
    print("\nBŁĄD: Klucze nie są identyczne!")