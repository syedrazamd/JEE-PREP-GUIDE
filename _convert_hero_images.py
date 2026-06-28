"""Convert hero/blog PNGs to WebP at quality 80, keeping original dimensions."""
from PIL import Image
import os
import sys

ROOT = r"e:\jeeprepguide"
TARGET_DIRS = [
    os.path.join(ROOT, "jee", "physics"),
    os.path.join(ROOT, "jee", "chemistry"),
    os.path.join(ROOT, "blog"),
]

results = []
for d in TARGET_DIRS:
    if not os.path.isdir(d):
        continue
    for name in os.listdir(d):
        if not name.lower().endswith(".png"):
            continue
        src = os.path.join(d, name)
        dst = os.path.join(d, os.path.splitext(name)[0] + ".webp")
        try:
            with Image.open(src) as img:
                # Preserve original dimensions; convert mode if needed for WebP
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img.save(dst, "WEBP", quality=80, method=6)
            src_size = os.path.getsize(src)
            dst_size = os.path.getsize(dst)
            results.append((src, dst, src_size, dst_size))
            print(f"OK  {os.path.relpath(src, ROOT)} -> {os.path.basename(dst)}  ({src_size//1024}KB -> {dst_size//1024}KB)")
        except Exception as e:
            print(f"ERR {src}: {e}")

print(f"\nTotal converted: {len(results)}")
total_src = sum(r[2] for r in results)
total_dst = sum(r[3] for r in results)
print(f"Original total: {total_src/1024/1024:.2f} MB")
print(f"WebP total:     {total_dst/1024/1024:.2f} MB")
print(f"Reduction:      {(1 - total_dst/total_src)*100:.1f}%")
