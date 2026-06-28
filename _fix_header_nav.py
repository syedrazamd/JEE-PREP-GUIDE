import re
import glob
import os

CANONICAL = {
    "Home": "https://jeeprepguide.netlify.app/",
    "Physics": "https://jeeprepguide.netlify.app/jee/physics",
    "Chemistry": "https://jeeprepguide.netlify.app/jee/chemistry",
    "Maths": "https://jeeprepguide.netlify.app/jee/maths",
}

changed_files = []

# Use absolute path to avoid issues
base_dir = r"e:\jeeprepguide"

for path in glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    header_match = re.search(r"<header.*?</header>", content, re.DOTALL)
    if not header_match:
        continue
    header = header_match.group(0)
    original_header = header

    for label, correct_href in CANONICAL.items():
        # Matches <a href="ANYTHING" ...other attrs...>Label</a>
        # where Label is the only direct text content
        pattern = re.compile(
            r'(<a\s+href=")[^"]*("[^>]*>\s*' + re.escape(label) + r'\s*</a>)'
        )
        header = pattern.sub(r'\1' + correct_href + r'\2', header)

    if header != original_header:
        content = content.replace(original_header, header)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        changed_files.append(path)

print(f"Modified {len(changed_files)} files:")
for p in changed_files:
    print(" ", p)
