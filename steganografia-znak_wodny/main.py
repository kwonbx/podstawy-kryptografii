from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    encoded_img = img.copy() 
    width, height = img.size
    
    message += "###"
    binary_message = text_to_binary(message)
    message_length = len(binary_message)
    
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))

            for n in range(3):
                if data_index < message_length:
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            
            encoded_img.putpixel((x, y), tuple(pixel))
            
            if data_index >= message_length:
                encoded_img.save(output_path)
                print("Wiadomość została osadzona pomyślnie.")
                return
                
    return "Błąd: Obraz jest zbyt mały, aby pomieścić tę wiadomość."

def decode_lsb(image_path):
    img = Image.open(image_path)
    width, height = img.size
    binary_data = ""
    
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            
            for n in range(3):
                binary_data += str(pixel[n] & 1)
                
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    
    decoded_message = ""
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-3:] == "###":
            break
            
    return decoded_message[:-3]


if __name__ == '__main__':
    encode_lsb("fototapety-kotek.png", "Test", "obraz_z_ukrytym.png")
    msg = decode_lsb("obraz_z_ukrytym.png")
    print("Odczytano:", msg)