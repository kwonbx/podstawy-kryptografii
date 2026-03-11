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

def singleBitTest(out):
    count = 0

    for b in out:
        if b == 1:
            count += 1

    if count > 9725 and count < 10275:
        print("\nTest pojedynczych bitów pozytywny: " + str(count))
    else:
        print("\nTest pojedynczych bitów negatywny: " + str(count))

def seriesTest(out, b):
    count = [0] * 6
    m = 0
    for i in range(0, len(out)):
        if out[i] == b:
            m += 1
        else:
            if m > 0:
                id = min(m, 6) - 1
                count[id] += 1
            m = 0

    if m > 0:
        id = min(m, 6) - 1
        count[id] += 1

    if (count[0] >= 2315 and count[0] <= 2685) and (count[1] >= 1114 and count[1] <= 1386) and (count[2] >= 527 and count[2] <= 723) and (count[3] >= 240 and count[3] <= 384) and (count[4] >= 103 and count[4] <= 209) and (count[5] >= 103 and count[5] <= 209):
        print("\nTest serii dla bitu " + str(b) + " pozytywny:")
    else:
        print("\nTest serii dla bitu " + str(b) + " negatywny:")

    print("1: " + str(count[0]))
    print("2: " + str(count[1]))
    print("3: " + str(count[2]))
    print("4: " + str(count[3]))
    print("5: " + str(count[4]))
    print("6 lub więcej: " + str(count[5]))

def longSeriesTest(out, b):
    count = 0
    for i in range(0, len(out)):
        if out[i] == b:
            count += 1
        else:
            count = 0

        if count == 26:
            print("\nTest długiej serii dla bitu " + str(b) + " negatywny")
            return

    print("\nTest długiej serii dla bitu " + str(b) + " pozytywny")

def pokerTest(out):
    segments = [out[i:i + 4] for i in range(0, len(out), 4)]
    count = [0] * 16

    for b in segments:
        val = "".join(map(str, b))
        dec = int(val, 2)
        count[dec] += 1

    x = 16/5000 * sum([i ** 2 for i in count]) - 5000

    if x > 2.16 and x < 46.17:
        print("\nTest pokerowy pozytywny: " + str(x))
    else:
        print("\nTest pokerowy negatywny: " + str(x))

if __name__ == '__main__':
    p = findParam(int(input("Podaj liczbę p: ")))
    q = findParam(int(input("Podaj liczbę q: ")))

    print("\np = " + str(p) + ", q = " + str(q))

    N = p * q
    x = findSeed(N)
    print("N = " + str(N) + ", seed = " + str(x))

    output = []
    for i in range(0, 20000):
        x = x**2 % N
        output.append(x % 2)

    print("output = " + " ".join(map(str, output)))
    singleBitTest(output)
    seriesTest(output, 1)
    seriesTest(output, 0)
    longSeriesTest(output, 1)
    longSeriesTest(output, 0)
    pokerTest(output)