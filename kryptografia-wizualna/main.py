import numpy as np
from PIL import Image
import random

def krypto_wizualna(obraz):
    try:
        img = Image.open(obraz).convert('L').resize((100, 100))
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {obraz}.")
        return

    img_array = np.array(img)

    binary_image = (img_array >= 128).astype(int)
    height, width = binary_image.shape
    
    share1 = np.zeros((height, width * 2), dtype=np.uint8)
    share2 = np.zeros((height, width * 2), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pixel = binary_image[i, j]
            choice = random.choice([0, 1])
            
            if pixel == 1: 
                if choice == 0:
                    s1 = [255, 0]
                    s2 = [255, 0]
                else:
                    s1 = [0, 255]
                    s2 = [0, 255]
            else: 
                if choice == 0:
                    s1 = [255, 0]
                    s2 = [0, 255]
                else:
                    s1 = [0, 255]
                    s2 = [255, 0]
                    
            share1[i, j*2 : j*2+2] = s1
            share2[i, j*2 : j*2+2] = s2

    Image.fromarray(share1).save('udzial_1.png')
    Image.fromarray(share2).save('udzial_2.png')

    result = np.minimum(share1, share2)
    Image.fromarray(result).save('zlozony_wynik.png')
    
    print("Szyfrowanie zakończone. Wygenerowano pliki:")
    print("- udzial_1.png")
    print("- udzial_2.png")
    print("- zlozony_wynik.png")

if __name__ == "__main__":
    img = input("Podaj nazwę pliku: ")
    krypto_wizualna(img)