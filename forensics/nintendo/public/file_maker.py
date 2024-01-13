from PIL import Image
from apng import APNG
from Crypto.Util.number import long_to_bytes

filenames = []
files = []

my_png = Image.open("nintendo.png")
pixels = my_png.load()
width, height = my_png.size

for i in range(len(FLAG)):
    png_filenames = f'./images/nintendo{i+1}.png'
    new_png = Image.new(my_png.mode, my_png.size)
    new_pixels = new_png.load()
    for x in range(width):
        for y in range(height):
            change_pixel = False
            pixels = list(my_png.getpixel((x, y)))
            if (x==i & x==y):
                    pixel = long_to_bytes(pixels[0]*ord(FLAG[i]))
                    new_pixels[x,y] = (pixel[1],pixel[0],0)
                    change_pixel = True
            if (not change_pixel):
                new_pixels[x,y] = my_png.getpixel((x, y))
    new_png.save(png_filenames)
    filenames.append(new_png)
    delay = 100 * (i%10)
    files.append((png_filenames, delay))

my_apng = APNG()
for png_filenames, delay in files:
    my_apng.append_file(png_filenames, delay=delay)
my_apng.save("nintendo.apng")
