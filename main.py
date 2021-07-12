from PIL import Image, ImageDraw
from io import BytesIO
import base64
import time

image_folder = "YOUR_PATH"
original_path = image_folder+"\Original.png"
modified_path = image_folder+"\Modified.png"
report_path = image_folder+"\Report.png"

# Multipliers 1 - 5px ; 2 - 10px ; 3 - 15px etc
# if resolution % (chunk_size * 5px) != 0 some warnings may appear
chunk_multiplier = 2
chunk_size = chunk_multiplier * 5

# Valid noise level between chunks
noise_level = 0.001

#method to collect chunk hash
def process_chunk(source_image, x, y):
    chunk_hash = 0
    #cycle through the chunk and collect summ of the pixels
    for coordinateY in range(y, y + chunk_size):
        for coordinateX in range(x, x + chunk_size):
            try:
                pixel = source_image.getpixel((coordinateX, coordinateY))
                chunk_hash += sum(pixel)
            except:
                #if some of the pixels are not exist means we out of borders
                #need to improve this later
                return

    return chunk_hash


def compare_pictures():
    # open images
    original_img = Image.open(original_path)
    modified_img = Image.open(modified_path)
    # report image is based on modified image
    modified_img.save(report_path)
    report_img = Image.open(report_path)
    
    #check if both images are the same resolution
    if original_img.size != modified_img.size:
        print(" >> ERROR ! Both images should have the same resolution")
 
    screen_width, screen_height = original_img.size

    unequal_chunks = 0
    
    #cycle through the images with chunk_size as step
    for y in range(0, screen_height, chunk_size):
        for x in range(0, screen_width, chunk_size):
            
            #collecting hash for every chunk
            original_hash = process_chunk(original_img, x, y)
            modified_hash = process_chunk(modified_img, x, y)
            
            #exceptions
            if original_hash is None or modified_hash is None:
                print(" >> WARNING! Hash is empty, some chunks at the borders ignored. Adjust the chunk size")
                continue
            
            #calculate chunk difference between the images
            diff = original_hash / modified_hash

            if abs(1 - diff) > noise_level:
                #print("We have something interesting here {} / {}".format(x,y))
                #mark report for unequal chunk
                draw = ImageDraw.Draw(report_img)
                draw.rectangle((x, y, x + chunk_size, y + chunk_size), outline="red")
                #counting unequal chunks for a report purpose
                unequal_chunks+=1

    #save report image
    report_img.save(report_path)

    return unequal_chunks


print("We have {} unequal chunks between images".format(compare_pictures()))
report_img = Image.open(report_path)
report_img.show()