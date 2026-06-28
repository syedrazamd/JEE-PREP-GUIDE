import re

files = [
    r'e:\jeeprepguide\jee\physics\electrostatics.html',
    r'e:\jeeprepguide\jee\physics\kinematics.html',
    r'e:\jeeprepguide\jee\chemistry\electrochemistry.html',
]

for path in files:
    print(f"\n=== {path} ===")
    with open(path, encoding='utf-8') as f:
        content = f.read()
    header_match = re.search(r'<header.*?</header>', content, re.DOTALL)
    if header_match:
        header = header_match.group(0)
        for label in ['Home', 'Physics', 'Chemistry', 'Maths']:
            pat = re.compile(r'<a href="([^"]*)"[^>]*>\s*' + label + r'\s*</a>')
            m = pat.search(header)
            if m:
                print(f"  {label}: {m.group(1)}")
