from PIL import Image
import numpy as np
def resize_image(image_path, output_path):
    image = Image.open(image_path)
    
    new_width = image.width // 4
    new_height = image.height // 4
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)     
    resized_image.save(output_path)
    print(f"Image saved with new size at {output_path}")

#resize_image('test.png', 'test2.png')
def image_in_image_encode(cover_image, secret_image) :
    img1 = Image.open(cover_image)
    img1 = img1.convert('RGB')
    img2 = Image.open(secret_image)
    img2 = img2.convert('RGB')
    w1, h1 = img1.size
    w2, h2 = img2.size
    assert(w2 <= w1//4 and h2 <= h1//4)
    p1 = img1.load()
    p2 = img2.load()
    x, y = 0, 0
    arr = [192, 48, 12, 3]
    shift_amount = [6, 4, 2, 0]
    for j in range(h2) :
        for i in range(w2) :
            (r, g, b) = p2[i, j]
            for index in range(4) :
                r1, g1, b1 = p1[x, y]
                r1 = ((r & arr[index]) >> shift_amount[index]) |(r1 & ~3)
                b1 = ((b & arr[index]) >> shift_amount[index]) | (b1 & ~3)
                g1 = ((g & arr[index]) >> shift_amount[index]) | (g1 & ~3)
                p1[x, y] = (r1, g1, b1)
                x += 1
        y += 1
        x = 0
    img1.save("encoded_image.png")
    
#image_in_image_encode("test.png", "test2.png")
            

def decode_image_in_image() :
    img = Image.open("encoded_image.png")
    img = img.convert('RGB')
    width, height = img.size
    target_width, target_height = width//4, height//4
    pixels = img.load()
    decoded = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    x, y = 0, 0
    for j in range(target_height) :
        for i in range(target_width) :
            r, g, b = 0, 0, 0
            for index in range(4) :
                r1, g1, b1 = pixels[x, y]
                r |= (r1 & 3) << (6 - 2 * index)
                g |= (g1 & 3) << (6 - 2 * index)
                b |= (b1 & 3) << (6 - 2 * index)
                x += 1
            decoded[j, i, 0] = r
            decoded[j, i, 1] = g
            decoded[j, i, 2] = b
        y += 1
        x = 0
    img2 = Image.fromarray(decoded)
    img2.save("decoded_image.png")
    
#decode_image_in_image()     


def text_encode(image_path, message):
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    
    
    x, y = 0, 0

    for char in message:
        char_index = 0
        if char.isalpha():
            char_index = ord(char.upper()) - 65  
        elif char == " ":
            char_index = 26
        else:
            continue  
        r, g, b = pixels[x, y]

        r = (r & ~3) | ((char_index & 48) >> 4)
        g = (g & ~3) | ((char_index & 12) >> 2)
        b = (b & ~3) | (char_index & 3)

        pixels[x, y] = (r, g, b)
        print(pixels[x , y] , char_index)

        x += 1
        if x == width:
            x = 0
            y += 1
            if y == height:
                raise ValueError("Image is too small to encode the message.")

    if x == width:
        x = 0
        y += 1
    r, g, b = pixels[x, y]
    r = (r & ~3) | 3
    g = (g & ~3) | 3
    b = (b & ~3) | 3
    pixels[x, y] = (r, g, b)
    print(pixels[x,y])

    encoded_image_path = "encoded_" + image_path
    img.save(encoded_image_path)
    print(f"Message encoded and saved as {encoded_image_path}")

def decode(image_path):
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    
    message = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            char_index = ((r & 3) << 4) | ((g & 3) << 2) | (b & 3)

            if char_index == 63:  
                return message
            
            if 0 <= char_index < len(alphabet):
                message += alphabet[char_index]
    return message


text_encode("test.png", "ANURAG AND PRIYANSHU BEST FREIENDS")
print("Decoded Message:", decode("encoded_test.png"))
