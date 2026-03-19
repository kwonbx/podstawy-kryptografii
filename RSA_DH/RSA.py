import math
import random

def findE(phi):
    e = random.randint(1, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(1, phi - 1)
    return e

def intoBlocks(m):
    blocks = []
    m = str(m)
    for i in range(0, len(m), 3):
        s = m[i:i + 3]
        blocks.append(int(s))
    return blocks

def compare(m1, m2):
    m1 = str(m1)
    m2 = str(m2)
    for i in range(0, len(m1)):
        if m1[i] != m2[i]:
            print("BŁĄD: Wiadomości nie są identyczne!")
            return False
    print("Wiadomości są identyczne!")

if __name__ == '__main__':
    p = 7433
    q = 2351

    print("p = " + str(p) + ", q = " + str(q))

    n = p * q
    print("n = " + str(n))

    phi = (p - 1) * (q - 1)
    print("phi = " + str(phi))

    e = findE(phi)
    print("e (klucz publiczny) = " + str(e))

    d = pow(e, -1, phi)
    print("d (klucz prywatny) = " + str(d))

    m = 64323887627863278391893731789316431689819363819410

    blocksM = intoBlocks(m)

    c = [pow(x, e, n) for x in blocksM]

    print("WIADOMOŚĆ ZASZYFROWANA: " + "".join(map(str, c)))

    blocksM2 = [pow(x, d, n) for x in c]
    lastBlockLength = len(str(m)) % 3
    if lastBlockLength == 0:
        lastBlockLength = 3

    partsM2 = []
    for i, val in enumerate(blocksM2):
        if i == len(blocksM2) - 1:
            partsM2.append(str(val).zfill(lastBlockLength))
        else:
            partsM2.append(str(val).zfill(3))

    m2_final = int("".join(partsM2))
    print("WIADOMOŚĆ JAWNA: " + str(m2_final))

    compare(m, m2_final)
