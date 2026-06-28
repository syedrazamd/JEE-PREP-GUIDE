import os
import re

# Relationship map: chapter_slug -> [related_slug_1, related_slug_2]
RELATIONSHIPS = {
    # PHYSICS
    "units-and-dimensions": ["kinematics", "laws-of-motion"],
    "kinematics": ["laws-of-motion", "work-energy-and-power"],
    "laws-of-motion": ["kinematics", "work-energy-and-power"],
    "work-energy-and-power": ["laws-of-motion", "centre-of-mass-and-collision"],
    "centre-of-mass-and-collision": ["work-energy-and-power", "rotational-motion"],
    "rotational-motion": ["centre-of-mass-and-collision", "gravitation"],
    "gravitation": ["rotational-motion", "kinematics"],
    "simple-harmonic-motion": ["wave-motion", "rotational-motion"],
    "wave-motion": ["simple-harmonic-motion", "wave-optics"],
    "fluid-mechanics": ["work-energy-and-power", "thermal-properties-of-matter"],
    "thermal-properties-of-matter": ["kinetic-theory-of-gases", "thermodynamics"],
    "kinetic-theory-of-gases": ["thermal-properties-of-matter", "thermodynamics"],
    "thermodynamics": ["kinetic-theory-of-gases", "thermal-properties-of-matter"],
    "electrostatics": ["capacitance", "current-electricity"],
    "capacitance": ["electrostatics", "current-electricity"],
    "current-electricity": ["capacitance", "magnetic-effect-of-current-and-magnetism"],
    "magnetic-effect-of-current-and-magnetism": ["current-electricity", "electromagnetic-induction"],
    "electromagnetic-induction": ["magnetic-effect-of-current-and-magnetism", "alternating-current"],
    "alternating-current": ["electromagnetic-induction", "electromagnetic-waves"],
    "electromagnetic-waves": ["alternating-current", "wave-optics"],
    "ray-optics": ["wave-optics", "dual-nature-of-radiation-and-matter"],
    "wave-optics": ["ray-optics", "wave-motion"],
    "dual-nature-of-radiation-and-matter": ["atoms-and-nuclei", "ray-optics"],
    "atoms-and-nuclei": ["dual-nature-of-radiation-and-matter", "semiconductors"],
    "semiconductors": ["atoms-and-nuclei", "current-electricity"],
    # CHEMISTRY
    "some-basic-concepts-of-chemistry": ["states-of-matter", "atomic-structure"],
    "atomic-structure": ["some-basic-concepts-of-chemistry", "chemical-equilibrium"],
    "states-of-matter": ["some-basic-concepts-of-chemistry", "thermodynamics"],
    "chemical-equilibrium": ["thermodynamics", "ionic-equilibrium"],
    "ionic-equilibrium": ["chemical-equilibrium", "electrochemistry"],
    "electrochemistry": ["ionic-equilibrium", "chemical-kinetics"],
    "chemical-kinetics": ["electrochemistry", "surface-chemistry"],
    "surface-chemistry": ["chemical-kinetics", "ionic-equilibrium"],
    # MATHS
    "sets": ["relations-functions", "quadratic-equations"],
    "relations-functions": ["sets", "quadratic-equations"],
    "quadratic-equations": ["complex-numbers", "relations-functions"],
    "complex-numbers": ["quadratic-equations", "sequences-and-series"],
    "sequences-and-series": ["permutations-and-combinations", "quadratic-equations"],
    "permutations-and-combinations": ["sequences-and-series", "sets"],
}

def slug_to_title(slug):
    """Convert slug to display title: 'magnetic-effect' -> 'Magnetic Effect'"""
    return " ".join(word.capitalize() for word in slug.split("-"))

def build_block(slug):
    """Build the Related Concepts HTML block for a given chapter slug."""
    rel1, rel2 = RELATIONSHIPS[slug]
    title1 = slug_to_title(rel1)
    title2 = slug_to_title(rel2)
    return (
        '    <!-- Related Concepts -->\n'
        '    <div class="bg-gray-50 border-l-4 border-primary rounded-lg p-5 flex flex-col sm:flex-row sm:items-center gap-4">\n'
        '        <span class="text-2xl">🔗</span>\n'
        '        <div>\n'
        '            <p class="font-semibold text-gray-900 mb-1">Builds on these concepts:</p>\n'
        '            <div class="flex flex-wrap gap-3 text-sm">\n'
        f'                <a href="./{rel1}.html" class="text-primary font-semibold hover:underline">{title1} &rarr;</a>\n'
        f'                <a href="./{rel2}.html" class="text-primary font-semibold hover:underline">{title2} &rarr;</a>\n'
        '            </div>\n'
        '        </div>\n'
        '    </div>\n'
    )

def process_file(filepath):
    """Add Related Concepts block as first child of <main>."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract chapter slug from filename
    filename = os.path.basename(filepath)
    slug = filename.replace(".html", "")

    if slug not in RELATIONSHIPS:
        print(f"  SKIP (no map entry): {filepath}")
        return False

    # Check if already inserted
    if "Builds on these concepts" in content:
        print(f"  SKIP (already present): {filepath}")
        return False

    # Find the <main> tag and insert after it
    main_tag = '<main class="order-1 lg:order-2 lg:col-span-3 space-y-12">'
    if main_tag not in content:
        print(f"  SKIP (main tag not found): {filepath}")
        return False

    block = build_block(slug)
    new_content = content.replace(main_tag, main_tag + "\n" + block, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  OK: {filepath}")
    return True

def main():
    base = r"e:\jeeprepguide\jee"
    subjects = ["physics", "chemistry", "maths"]
    total = 0
    updated = 0

    for subject in subjects:
        subject_dir = os.path.join(base, subject)
        print(f"\n=== {subject.upper()} ===")
        for filename in sorted(os.listdir(subject_dir)):
            if not filename.endswith(".html") or filename == "index.html":
                continue
            filepath = os.path.join(subject_dir, filename)
            total += 1
            if process_file(filepath):
                updated += 1

    print(f"\n=== DONE: {updated}/{total} files updated ===")

if __name__ == "__main__":
    main()