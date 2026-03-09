import math
import random

def checkParam(x):
    liczbaPierwsza = True
    for i in range(2, x):
        if x % i == 0:
            liczbaPierwsza = False
            break

    if liczbaPierwsza == False or x % 4 != 3:
        return False
    else:
        return True

def findParam(x):
    while checkParam(x) == False:
        x = x + 1
    return x

def findSeed(N):
    seed = random.randint(1, N - 1)
    while math.gcd(seed, N) != 1:
        seed = random.randint(1, N - 1)
    return seed

if __name__ == '__main__':
    p = findParam(500)
    q = findParam(p + 1)

    N = p * q
    seed = findSeed(N)
    x = seed**2 % N
    output = [x % 2]

    for i in range(1, 20000):
        x = x**2 % N
        output.append(x % 2)
