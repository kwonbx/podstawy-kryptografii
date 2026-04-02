import hashlib
import time
import random
import string
import numpy as np
import os

def generateHash(text, algorithm):
    hashObj = hashlib.new(algorithm)
    hashObj.update(text)
    return hashObj.hexdigest()

def findCollision(algorithm='sha256'):
    hexNum = 12 // 4
    seen = {}
    attemps = 1

    while 1:
        randomText = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        fullHash = generateHash(randomText.encode('utf-8'), algorithm)
        prefix = fullHash[:hexNum]

        if prefix in seen:
            originalText = seen[prefix]
            originalHash = generateHash(originalText.encode('utf-8'), algorithm)
            print("\nZnaleziono kolizję po " + str(attemps) + " próbach:")
            print("Tekst 1: " + originalText + " | Hash: " + originalHash)
            print("Tekst 2: " + randomText + " | Hash: " + fullHash)
            print("Wspólny prefix: " + str(prefix))
            break

        seen[prefix] = randomText

def toBits(data):
    bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    return bits

def sha256Bits(data):
    hashObj = hashlib.new('sha256')
    hashObj.update(data)
    return toBits(hashObj.digest())

def testSAC_sha256():
    outputBytesLength = 256
    changeCounter = np.zeros(outputBytesLength)

    for _ in range(1000):
        inputBytes = np.random.bytes(32)
        hashBits = sha256Bits(inputBytes)

        modifiedInput = bytearray(inputBytes)

        byteID = random.randint(0, 31)
        bitID = random.randint(0, 7)

        modifiedInput[byteID] ^= (1 << bitID)
        modifiedHash = sha256Bits(modifiedInput)
        changeCounter += (hashBits ^ modifiedHash)

    return changeCounter / 1000

if __name__ == '__main__':
    algorithms = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']
    userText = input('Podaj tekst: ')

    files = {
        "10MB": 1024 * 1024 * 10,
        "100MB": 1024 * 1024 * 100,
        "500MB": 1024 * 1024 * 500,
    }

    for algorithm in algorithms:
        start = time.time()
        val = generateHash(userText.encode('utf-8'), algorithm)
        end = time.time()
        print("\nAlgorytm " + algorithm + ": \nTekst użytkownika o długości " + str(len(userText)) + " znaków: " + val + " | Czas działania: " + str(end - start) + " | Długość ciągu wyjściowego: " + str(len(val)))
        for label, bytes in files.items():
            data = os.urandom(bytes)
            start = time.time()
            val = generateHash(data, algorithm)
            end = time.time()
            print("Tekst testowy o wielkości " + label + ": " + val + " | Czas działania: " + str(end - start) + " | Długość ciągu wyjściowego: " + str(len(val)))

    findCollision('sha256')
    prob = testSAC_sha256()
    meanProb = np.mean(prob)
    print("\nŚrednie prawdopodobieństwo zmiany dla wszystkich bitów na wyjściu po zmianie jednego bitu na wejściu: " + str(round(meanProb, 3)))
