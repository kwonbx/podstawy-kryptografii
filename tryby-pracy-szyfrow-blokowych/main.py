from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import time
import os

def cipherMode(mode, iv, nonce):
    match mode:
        case 'ECB': return modes.ECB()
        case 'CBC': return modes.CBC(iv)
        case 'CFB': return modes.CFB(iv)
        case 'OFB': return modes.OFB(iv)
        case 'CTR': return modes.CTR(nonce)
        case _: return None

def benchmark(modeNames, key, iv, nonce):
    files = {
        "10MB": 1024*1024,
        "100MB": 1024*1024*10,
        "500MB": 1024*1024*100,
    }

    for label, bytes in files.items():
        data = os.urandom(bytes)
        padder = padding.PKCS7(128).padder()
        paddedData = padder.update(data) + padder.finalize()

        print("\nWielkość danych: " + label)

        for mode in modeNames:
            modeObject = cipherMode(mode, iv, nonce)
            cipher = Cipher(algorithms.AES(key), modeObject, backend=default_backend())

            encryptor = cipher.encryptor()
            startEnc = time.time()
            cipherText = encryptor.update(paddedData) + encryptor.finalize()
            endEnc = time.time()

            decryptor = cipher.decryptor()
            startDec = time.time()
            decryptedText = decryptor.update(cipherText) + decryptor.finalize()
            endDec = time.time()

            totalEnc = endEnc - startEnc
            totalDec = endDec - startDec

            print(mode + ":")
            print("Czas szyfrowania:" + str(totalEnc) + " | Czas deszyfrowania: " + str(totalDec))

def errorPropagation(modeNames, key, iv, nonce):
    plainText = b"Wiadomosc przygotowana na potrzeby testu. ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    plainText = plainText[:64]

    for mode in modeNames:
        modeObject = cipherMode(mode, iv, nonce)
        cipher = Cipher(algorithms.AES(key), modeObject, backend=default_backend())

        encryptor = cipher.encryptor()
        cipherText = encryptor.update(plainText) + encryptor.finalize()
        corruptedText = bytearray(cipherText)
        corruptedText[20] = corruptedText[20] ^ 0xFF

        decryptor = cipher.decryptor()
        decryptedText = decryptor.update(corruptedText) + decryptor.finalize()
        diffs = [i for i in range(len(plainText)) if plainText[i] != decryptedText[i]]

        if len(diffs) == 1:
            print(mode + ": Tylko 1 bajt został zmieniony")
        elif len(diffs) <= 16:
            print(mode + ": Błąd w obrębie 1 bloku (zmieniono " + str(len(diffs)) + " bajtów)")
        else:
            print(mode + ": Propagacja! Uszkodzono " + str(len(diffs)) + " bajtów")

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def cbcEncrypt(text, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    paddedData = padder.update(text) + padder.finalize()

    cipherText = b""
    prevBlock = iv

    for i in range(0, len(paddedData), 16):
        currentBlock = paddedData[i:i + 16]
        blockToEncrypt = xor(currentBlock, prevBlock)
        encryptedBlock = encryptor.update(blockToEncrypt)
        cipherText += encryptedBlock
        prevBlock = encryptedBlock

    return cipherText

def cbcDecrypt(cipherText, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    decryptedText = b""
    prevBlock = iv

    for i in range(0, len(cipherText), 16):
        currentBlock = cipherText[i:i + 16]
        decryptedBlock = decryptor.update(currentBlock)
        plainBlock = xor(decryptedBlock, prevBlock)
        decryptedText += plainBlock
        prevBlock = currentBlock

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decryptedText) + unpadder.finalize()


if __name__ == "__main__":
    modeNames = ["ECB", "CBC", "CFB", "OFB", "CTR"]
    key = os.urandom(16)
    iv = os.urandom(16)
    nonce = os.urandom(16)
    benchmark(modeNames, key, iv, nonce)
    print("")
    errorPropagation(modeNames, key, iv, nonce)

    msg = "Wiadomosc przygotowana na potrzeby testu. (CBC)".encode("utf-8")
    enc = cbcEncrypt(msg, key, iv)
    dec = cbcDecrypt(enc, key, iv)
    print("\nWiadomość do zaszyfrowania: " + str(msg))
    print("Wiadomość zaszyfrowana: " + str(enc))
    print("Wiadomość zdeszyfrowana: " + str(dec))