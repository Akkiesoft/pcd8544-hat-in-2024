import os
import sys
import PIL.Image

def image_to_fb_vlsb(img_path):
    i = PIL.Image.open(img_path).convert("1")

    width, height = i.size
    # TODO: 8の倍数でないときのいい感じのやり方と、その後のビットシフト処理
    y_block_plus = 1 if height % 8 else 0
    y_blocks = height // 8 + y_block_plus

    data = ""
    c = 1
    for y in range(0, y_blocks):
        for x in range(0, width):
            block = 0x00
            for by in range(0, 8):
                p = (255 - i.getpixel((x, y * 8 + by))) // 255
                block = block | p << by
            data += format(block, '#04x')
            data += ", " if c % 16 else ",\n"
            c += 1
    return "output = (\n%s)" % data

if len(sys.argv) < 2:
    print("usage: %s <image file>" % sys.argv[0])
    sys.exit(1)

print(image_to_fb_vlsb(sys.argv[1]))