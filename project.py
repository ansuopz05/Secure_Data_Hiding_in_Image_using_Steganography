from PIL import Image
import numpy as np
def texttobinary(text):
    return ''.join(format(ord(char), '08b') for char in text)
def binarytotext(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if int(char, 2) != 0)
def encodeimage(imagepath, secretmessage, outputpath):
    img = Image.open(imagepath)
    imgarr = np.array(img, dtype=np.uint8)  
    binarymessage = texttobinary(secretmessage) + '1111111111111110'  
    dataindex = 0
    totalpixels = imgarr.shape[0] * imgarr.shape[1] * 3  
    if len(binarymessage) > totalpixels:
        raise ValueError("Message is too large to fit in the image.")
    for row in imgarr:
        for pixel in row:
            for channel in range(3):  
                if dataindex < len(binarymessage):
                    pixel[channel] = (pixel[channel] & 254) | int(binarymessage[dataindex])  # Fixed line
                    dataindex += 1
                else:
                    break

    encodedimg = Image.fromarray(imgarr)
    encodedimg.save(outputpath)
    print("Message successfully encoded into ",outputpath)

def decodeimage(imagepath):
    img = Image.open(imagepath)
    imgarr = np.array(img)

    binarymessage = ""
    
    for row in imgarr:
        for pixel in row:
            for channel in range(3):  
                binarymessage += str(pixel[channel] & 1)

    endmarker = "1111111111111110"
    if endmarker in binarymessage:
        binarymessage = binarymessage[:binarymessage.index(endmarker)]
        return binarytotext(binarymessage)
    else:
        return "No hidden message found!"

if __name__ == "__main__":
    choice = input("Enter 'e' to encode or 'd' to decode: ").strip().lower()

    if choice == 'e':
        inputimage = input("Enter input image path: ")
        message = input("Enter the message to hide: ")
        outputimage = input("Enter output image path (e.g., output.png): ")
        encodeimage(inputimage, message, outputimage)
    elif choice == 'd':
        input_image = input("Enter the image path to decode: ")
        hidden_message = decodeimage(input_image)
        print("Decoded Message:", hidden_message)
    else:
        print("Invalid choice!")
