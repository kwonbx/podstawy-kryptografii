import hashlib
import time
import random
import string
import numpy as np

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

    testData = ["Lorem ipsum dolor sit amet, consectetur efficitur.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras nec sollicitudin arcu. Curabitur sed sodales nunc, vel feugiat lectus. Nullam tristique scelerisque libero eu ultrices. Suspendisse proin.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque consequat mauris sed mi mollis accumsan. Aenean fermentum commodo risus a venenatis. Duis ut elit urna. Praesent in malesuada nisl, et mollis erat. Quisque pretium enim gravida arcu aliquam, sed dictum odio ultricies. Vivamus viverra, ante commodo congue tincidunt, dui neque varius leo, sit amet pellentesque arcu leo porta erat. Quisque cursus, justo in commodo blandit, lacus erat gravida eros, et rhoncus lacus mi sed purus aenean.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed tempus gravida dolor, vitae molestie tellus tempus et. Aliquam malesuada posuere enim viverra finibus. Duis elementum felis libero, ut dictum dolor condimentum et. Proin eu hendrerit sem. Morbi suscipit tristique sem et dignissim. Curabitur placerat lacus in ex convallis tincidunt. Phasellus nec erat sapien. Ut sem arcu, mollis id ante sit amet, suscipit vehicula urna. Etiam mattis sem turpis, sed ultricies purus sagittis quis. Sed a nulla dolor. Morbi diam nibh, porttitor a orci eget, fringilla finibus nulla. Integer eu faucibus diam. Quisque eu risus dapibus, pellentesque ex sit amet, tempus tellus. Nulla a sapien faucibus tortor gravida facilisis egestas ut enim. Quisque urna nunc, semper nec odio quis, facilisis pulvinar est. Maecenas at metus vel diam gravida pharetra sit amet in lorem. Phasellus dapibus dolor a sapien pharetra, sit amet mattis libero finibus. Nulla at congue nisl, eget viverra est. Nunc aliquet metus in"]

    for algorithm in algorithms:
        start = time.time()
        val = generateHash(userText.encode('utf-8'), algorithm)
        end = time.time()
        print("\nAlgorytm " + algorithm + ": \nTekst użytkownika o długości " + str(len(userText)) + " znaków: " + val + " | Czas działania: " + str(end - start) + " | Długość ciągu wyjściowego: " + str(len(val)))
        for data in testData:
            start = time.time()
            val = generateHash(data.encode('utf-8'), algorithm)
            end = time.time()
            print("Tekst testowy o długości " + str(len(data)) + " znaków: " + val + " | Czas działania: " + str(end - start) + " | Długość ciągu wyjściowego: " + str(len(val)))

    findCollision('sha256')
    prob = testSAC_sha256()
    meanProb = np.mean(prob)
    print("\nŚrednie prawdopodobieństwo zmiany dla wszystkich bitów na wyjściu po zmianie jednego bitu na wejściu: " + str(round(meanProb, 3)))
