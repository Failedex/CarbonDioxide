#!/usr/bin/env python3

import subprocess
from PIL import Image, ImageDraw
import os

OUT = "/tmp/eww/cover.png"
os.makedirs("/tmp/eww", exist_ok=True)

proc = subprocess.Popen(["playerctl", "metadata", "--format", "{{ mpris:artUrl }}", "-F"], stdout=subprocess.PIPE, text=True)

def crop_to_circle(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")

    min_side = min(img.size)
    left = (img.width - min_side) // 2
    top = (img.height - min_side) // 2
    img = img.crop((left, top, left + min_side, top + min_side))

    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)

    img.putalpha(mask)

    img.save(output_path, format="PNG")

while True: 
    try:
        out = proc.stdout.readline().strip()
        out = out[7:].strip()
        if out == "": 
            continue
        crop_to_circle(out, OUT)
        print(OUT, flush=True)
    except: 
        print("./assets/void.svg")

