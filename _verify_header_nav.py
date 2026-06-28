import re, glob, os

results = []
for path in glob.glob(os.path.join(r'e:\jeeprepguide', '**', '*.html'), recursive=True):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    header_match = re.search(r'<header.*?</header>', content, re.DOTALL)
    if not header_match:
        continue
    header = header_match.group(0)
    for label in ['Physics', 'Chemistry', 'Maths']:
        pat = re.compile(r'<a href="([^"]*)"[^>]*>\s*' + label + r'\s*</a>')
        href_match = pat.search(header)
        if href_match:
            results.append((path, label, href_match.group(1)))

# Check for any incorrect links
incorrect = []
for path, label, href in results:
    expected = {
        'Physics': 'https://jeeprepguide.netlify.app/jee/physics',
        'Chemistry': 'https://jeeprepguide.netlify.app/jee/chemistry',
        'Maths': 'https://jeeprepguide.netlify.app/jee/maths',
    }
    if href != expected[label]:
        incorrect.append((path, label, href))

print(f"Total header nav links found: {len(results)}")
print(f"Incorrect links: {len(incorrect)}")
if incorrect:
    print("\nIncorrect links:")
    for r in incorrect:
        print(" ", r)
else:
    print("\nAll links are correct!")
