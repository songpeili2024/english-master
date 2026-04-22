"""Generate app icon"""
from PIL import Image, ImageDraw, ImageFont
import os

size = 512
img = Image.new('RGB', (size, size), color=(24, 135, 209))
draw = ImageDraw.Draw(img)

margin = 40
draw.rounded_rectangle([margin, margin, size-margin, size-margin], radius=60, fill=(255,255,255))

try:
    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 180)
except:
    font = ImageFont.load_default()

text = 'EM'
bbox = draw.textbbox((0,0), text, font=font)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
x = (size - tw) / 2
y = (size - th) / 2
draw.text((x, y), text, fill=(24, 135, 209), font=font)

out = 'C:/Users/songpeili/.qclaw/workspace-agent-pc/english-master/icon.png'
img.save(out)
print(f'Icon created: {os.path.getsize(out)} bytes')
