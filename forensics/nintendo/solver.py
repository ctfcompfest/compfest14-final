from tkinter import N
from PIL import Image
from Crypto.Util.number import bytes_to_long
from apng import APNG
N = 19
my_png = Image.open('./nintendo.png')
width, height = my_png.size
images = []

im = APNG.open('nintendo.apng')
for i, (png, control) in enumerate(im.frames):
	png.save(f"./images/nintendo{i+1}.png")

print(f"total of {len(im.frames)} images")
for i in range(N):
	images.append(Image.open(f'./images/nintendo{i+1}.png'))

flag = ""

for x in range(N):
        ori_pixel = list(my_png.getpixel((x, x)))
        this_pixel = list(images[x].getpixel((x, x)))
        a = []
        a.append(this_pixel[1])
        a.append(this_pixel[0])
        c = int(bytes_to_long(bytes(a))/ori_pixel[0])
        flag += chr(c)
print(flag)
