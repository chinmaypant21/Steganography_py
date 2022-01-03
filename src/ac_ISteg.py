from src.utilSteg import is_encodable,pair,Image
from src.util_Isteg import *

#2pixels for flag -> In first two pixel all rgb component will be even
#next 6pixel for image dimensions 3+3 width and height -> 2* 2,2,2  2,2,2  1,1,1
#next 5 pixel for num of pixels in secret image -> 2,2,2  2,2,2  2,2,2  2,2,2  1,1,1
HEADER_SIZE = 13 #pixels

def encode_message(original_image_pixels,secret_image_pixels,secret_image_size):
    num_payload_pixels  = len(secret_image_pixels)
    original_pixel_data,offset = add_header(original_image_pixels,secret_image_size,num_payload_pixels)

    for pixel in secret_image_pixels:
        first2_msb,next2_msb = pixel_MSB(pixel)
        original_image_pixels[offset] = encode_data(original_image_pixels[offset],first2_msb)
        offset += 1
        original_image_pixels[offset] = encode_data(original_image_pixels[offset],next2_msb)
        offset += 1
    
    return original_image_pixels
    
    
def HideData(orig_img_path='media/sierra.jpg',second_img_path='media/mac.jpg'):
    try:
        original_image_pixels = Image.open(orig_img_path)
    except:
        print(f"Unable to open image {orig_img_path}")
        exit(0)
    else:
        original_pixel_data = list(original_image_pixels.getdata())
        
    try:
        secret_image = Image.open(second_img_path)
    except:
        print(f"Unable to open image {second_img_path}")
        exit(0)
    else:
        secret_pixel_data = list(secret_image.getdata())
            
    if is_encodable(original_pixel_data,secret_pixel_data,HEADER_SIZE):
        encoded_msg_bytes = encode_message(original_pixel_data,secret_pixel_data,secret_image.size)
        
        new_img = Image.new(original_image_pixels.mode,original_image_pixels.size)
        new_img.putdata(tuple(encoded_msg_bytes))
        new_img.save('test.png')
        print("[+] Successfully encoded in image")
        pass

    else:
        print("[-] Process Unsuccessful")
        return
    pass

if __name__ == '__main__':
    HideData()