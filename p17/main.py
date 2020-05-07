#!/usr/bin/env python3

from PIL import Image
import numpy as np


def extract_tile(img, t):
    W,H = 450//3,600//2
    i,j = t//3, t%3
    return img[i*H:(i+1)*H,j*W:(j+1)*W,:]


def swap_tiles(img, t1, t2):
    tile1 = extract_tile(img, t1)
    tile2 = extract_tile(img, t2)
    tile1_copy = tile1.copy()
    tile1[:] = tile2
    tile2[:] = tile1_copy


im = Image.open("zatoichi.png")

im.show()

mat = np.array(im)

swap_tiles(mat, 4, 0)
swap_tiles(mat, 4, 2)
swap_tiles(mat, 4, 3)
swap_tiles(mat, 4, 1)
swap_tiles(mat, 4, 5)

im_reassembled = Image.fromarray(mat)
im_reassembled.save("zatoichi_reassembled.png")
im_reassembled.show()

# typically hidden messages are encoded in the last bit of each pixel
mat = 255*(mat&np.ones(mat.shape,dtype=np.uint8))
im_mod = Image.fromarray(mat)
im_mod.save("zatoichi_last_bit.png")
im_mod.show()

# We can see a nice pattern there!!


# Message is the last bit of each pixel. It's encoded first by column, then by
# row, and finally by channel. so we go left->right, top->down, r->g->b

data = []
b = 0
count = 0
for c in np.transpose(mat, (1,0,2)).flatten():
    b = (b<<1)|(c&1)
    count += 1
    if count == 8:
        data.append(b)
        count = b = 0
data = bytes(data)

with open("out.bytes", "wb") as f:
    f.write(data)

# Message says "CONGRATULATIONS, YOU FOUND THE HIDDEN (...)" and then a string
# of digits that looks like hexadecimal?

HEX_STRING = "E2A089E2A095E2A09DE2A09BE2A097E2A081E2A09EE2A0A5E2A087E2A081E2A09EE2A08AE2A095E2A09DE2A08E20E2A0BDE2A095E2A0A520E2A099E2A091E2A089E2A095E2A099E2A091E2A09920E2A09EE2A093E2A09120E2A08DE2A091E2A08EE2A08EE2A081E2A09BE2A09120E2A09EE2A093E2A09120E2A08FE2A081E2A08EE2A08EE2A0BAE2A095E2A097E2A09920E2A08AE2A08E20E2A09EE2A093E2A09120E2A08BE2A095E2A087E2A087E2A095E2A0BAE2A08AE2A09DE2A09B20E2A0BAE2A095E2A097E2A09920E2A08AE2A09D20E2A0A5E2A08FE2A08FE2A091E2A097E2A089E2A081E2A08EE2A09120E2A09EE2A081E2A085E2A091E2A08EE2A093E2A08AE2A085E2A08AE2A09EE2A081E2A09DE2A095E2A083E2A08AE2A09EE2A095E2A09EE2A081E2A085E2A091E2A08EE2A093E2A08AE2A093E2A0A5E2A08DE2A095E2A097E2A081E2A08DE2A081E2A097E2A08AE2A087E2A087E2A095E2A0BCE2A083E2A0BCE2A09AE2A0BCE2A083E2A0BCE2A09AE2A09EE2A0A5E2A091E2A09DE2A09EE2A08AE2A089E2A093E2A081E2A087E2A087E2A091E2A09DE2A09BE2A091E2A0BCE2A081E2A0BCE2A09A"

# ASCII? UNICODE?

decoded = []

for byte in (HEX_STRING[i:i+2] for i in range(0, len(HEX_STRING), 2)):
    byte = int(byte, 16)
    decoded.append(byte)

decoded = bytes(decoded).decode()
print(decoded) # braille... zatoichi... things fall in place!


# when translated (thanks https://www.dcode.fr/braille-alphabet), the resulting string reads:
print("CONGRATULATIONS YOU DECODED THE MESSAGE THE PASSWORD IS THE FOLLOWING WORD IN UPPERCASE TAKESHIKITANOBITOTAKESHIHUMORAMARILLO2020TUENTICHALLENGE10")

# And we're done!!

