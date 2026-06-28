"""Convert PNG files to WebP at quality 80, keeping original dimensions."""
import os
from pathlib import Path
from PIL import Image

ROOT = Path(r"e:\jeeprepguide")
TARGET_DIRS = [
    ROOT / "jee" / "physics",
    ROOT / "jee" / "chemistry",
    ROOT / "blog",
]

QUALITY = 80
results = []

for d in TARGET_DIRS:
    if not d.exists():
        print(f"Missing: {d}")
        continue
    for png in sorted(d.glob("*.png")):
        webp = png.with_suffix(".webp")
        try:
            with Image.open(png) as img:
                # Preserve mode; convert palette/alpha appropriately
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    save_img = img.convert("RGBA")
                else:
                    save_img = img.convert("RGB")
                save_img.save(webp, "WEBP", quality=QUALITY, method=6)
            orig_kb = png.stat().st_size / 1024
            new_kb = webp.stat().st_size / 1024
            results.append((str(png), orig_kb, new_kb))
            print(f"{png.name}: {orig_kb:.1f}KB -> {new_kb:.1f}KB")
        except Exception as e:
            print(f"FAILED {png}: {e}")

print(f"\nTotal files converted: {len(results)}")
total_orig = sum(r[1] for r in results)
total_new = sum(r[2] for r in results)
print(f"Total original: {total_orig/1024:.2f}MB")
print(f"Total new:      {total_new/1024:.2f}MB")
print(f"Reduction:      {(1 - total_new/total_orig)*100:.1f}%")

# Check for any over 250KB
over = [r for r in results if r[2] > 250]
if over:
    print(f"\nFiles over 250KB target ({len(over)}):")
    for path, _, nkb in over:
        print(f"  {Path(path).name}: {nkb:.1f}KB")
