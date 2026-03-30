"""Resize the generated icon.png into all required iOS app icon sizes."""
import sys
import os
import json
from PIL import Image

icon_dir = sys.argv[1]  # Path to AppIcon.appiconset directory
src = Image.open("icon.png").convert("RGBA")

sizes = [
    (20, 1), (20, 2), (20, 3), (29, 1), (29, 2), (29, 3),
    (40, 2), (40, 3), (60, 2), (60, 3), (76, 1), (76, 2), (83.5, 2), (1024, 1)
]
idioms = {
    (20, 1): "ipad", (20, 2): "iphone", (20, 3): "iphone",
    (29, 1): "ipad", (29, 2): "iphone", (29, 3): "iphone",
    (40, 2): "iphone", (40, 3): "iphone",
    (60, 2): "iphone", (60, 3): "iphone",
    (76, 1): "ipad", (76, 2): "ipad", (83.5, 2): "ipad", (1024, 1): "ios-marketing"
}

images = []
for pts, scale in sizes:
    px = int(pts * scale)
    name = f"icon_{px}x{px}.png"
    resized = src.resize((px, px), Image.LANCZOS)
    resized.save(os.path.join(icon_dir, name))
    images.append({
        "filename": name,
        "idiom": idioms[(pts, scale)],
        "scale": f"{scale}x",
        "size": f"{pts}x{pts}"
    })

contents = {"images": images, "info": {"author": "xcode", "version": 1}}
with open(os.path.join(icon_dir, "Contents.json"), "w") as f:
    json.dump(contents, f, indent=2)

print(f"Generated {len(images)} icon sizes in {icon_dir}")
