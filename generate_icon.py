"""Generate a galaxy-themed app icon for Faisal's Trading App."""
from PIL import Image, ImageDraw, ImageFilter
import random
import math

SIZE = 1024  # Standard iOS app icon size

img = Image.new('RGB', (SIZE, SIZE))
draw = ImageDraw.Draw(img)

# Fill with deep space background
for y in range(SIZE):
    r = int(5 + 15 * (y / SIZE))
    g = int(0 + 5 * (y / SIZE))
    b = int(25 + 40 * (y / SIZE))
    draw.line([(0, y), (SIZE, y)], fill=(r, g, b))

# Draw nebula glow (purple center)
nebula = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
nebula_draw = ImageDraw.Draw(nebula)
for i in range(80):
    cx, cy = SIZE // 2, SIZE // 2
    rx = random.randint(100, 400)
    ry = random.randint(100, 400)
    ox = random.randint(-150, 150)
    oy = random.randint(-150, 150)
    color_choice = random.choice([
        (120, 30, 200, 8),   # Purple
        (30, 60, 180, 6),    # Blue
        (180, 50, 120, 5),   # Pink
    ])
    nebula_draw.ellipse(
        [cx - rx + ox, cy - ry + oy, cx + rx + ox, cy + ry + oy],
        fill=color_choice
    )
nebula = nebula.filter(ImageFilter.GaussianBlur(radius=80))
img.paste(Image.alpha_composite(img.convert('RGBA'), nebula).convert('RGB'))

# Draw stars
random.seed(42)
for _ in range(300):
    x = random.randint(0, SIZE - 1)
    y = random.randint(0, SIZE - 1)
    size = random.randint(1, 4)
    brightness = random.randint(180, 255)
    gold_g = int(brightness * 0.85)
    draw = ImageDraw.Draw(img)
    draw.ellipse([x, y, x + size, y + size], fill=(brightness, gold_g, 60))

# Draw a bright center star burst (focal point)
center_glow = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
cg_draw = ImageDraw.Draw(center_glow)
for r in range(200, 0, -2):
    alpha = int(40 * (1 - r / 200))
    cg_draw.ellipse(
        [SIZE // 2 - r, SIZE // 2 - r, SIZE // 2 + r, SIZE // 2 + r],
        fill=(180, 140, 255, alpha)
    )
img = Image.alpha_composite(img.convert('RGBA'), center_glow).convert('RGB')
draw = ImageDraw.Draw(img)

# Draw "F" letter in the center (Faisal's initial)
# Using simple geometric shapes for the F
f_left = SIZE // 2 - 80
f_top = SIZE // 2 - 120
f_color = (220, 200, 255)
# Vertical bar of F
draw.rectangle([f_left, f_top, f_left + 40, f_top + 240], fill=f_color)
# Top horizontal bar of F
draw.rectangle([f_left, f_top, f_left + 160, f_top + 40], fill=f_color)
# Middle horizontal bar of F
draw.rectangle([f_left, f_top + 100, f_left + 120, f_top + 140], fill=f_color)

# Add subtle glow around the F
glow_layer = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)
glow_draw.rectangle([f_left - 5, f_top - 5, f_left + 165, f_top + 245],
                     fill=(180, 140, 255, 30))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=15))
img = Image.alpha_composite(img.convert('RGBA'), glow_layer).convert('RGB')

# Add rounded corner mask for iOS icon shape
mask = Image.new('L', (SIZE, SIZE), 0)
mask_draw = ImageDraw.Draw(mask)
radius = int(SIZE * 0.22)  # iOS standard corner radius ~22%
mask_draw.rounded_rectangle([0, 0, SIZE, SIZE], radius=radius, fill=255)

# Apply mask
final = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
final.paste(img, mask=mask)

# Save both versions
final.save('icon.png')
print(f'Generated galaxy icon: icon.png ({SIZE}x{SIZE})')
