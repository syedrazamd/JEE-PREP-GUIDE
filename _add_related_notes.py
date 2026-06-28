"""Add Related Notes recirculation block to all 40 chapter files."""
import os
import re

BASE = r"e:\jeeprepguide\JEE"

PHYSICS_FILES = sorted([
    "alternating-current.html", "atoms-and-nuclei.html", "capacitance.html",
    "centre-of-mass-and-collision.html", "current-electricity.html",
    "dual-nature-of-radiation-and-matter.html", "electromagnetic-induction.html",
    "electromagnetic-waves.html", "electrostatics.html", "fluid-mechanics.html",
    "gravitation.html", "kinematics.html", "kinetic-theory-of-gases.html",
    "laws-of-motion.html", "magnetic-effect-of-current-and-magnetism.html",
    "ray-optics.html", "rotational-motion.html", "semiconductors.html",
    "simple-harmonic-motion.html", "thermal-properties-of-matter.html",
    "thermodynamics.html", "units-and-dimensions.html", "wave-motion.html",
    "wave-optics.html", "work-energy-and-power.html",
])

CHEMISTRY_FILES = sorted([
    "atomic-structure.html", "chemical-equilibrium.html", "chemical-kinetics.html",
    "electrochemistry.html", "ionic-equilibrium.html",
    "some-basic-concepts-of-chemistry.html", "states-of-matter.html",
    "surface-chemistry.html", "thermodynamics.html",
])

MATHS_FILES = sorted([
    "complex-numbers.html", "permutations-and-combinations.html",
    "quadratic-equations.html", "relations-functions.html",
    "sequences-and-series.html", "sets.html",
])


def to_title(slug):
    """Convert filename slug to display title, e.g. 'alternating-current' -> 'Alternating Current'."""
    return " ".join(word.capitalize() for word in slug.replace(".html", "").split("-"))


def build_block(related):
    """Build the Related Notes HTML block."""
    cards = ""
    for slug in related:
        title = to_title(slug)
        cards += f'''            <a href="./{slug}" class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition border-t-4 border-primary">
                <h4 class="font-bold text-lg text-gray-900 mb-2">{title}</h4>
                <span class="text-primary font-semibold text-sm">Read Notes &rarr;</span>
            </a>
'''
    return f'''    <!-- Related Notes -->
    <section class="pt-8 border-t">
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Related Notes</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
{cards}        </div>
    </section>
'''


def get_related(chapters, current):
    """Get next 3 chapters from sorted list, wrapping around."""
    idx = chapters.index(current)
    related = []
    for i in range(1, 4):
        related.append(chapters[(idx + i) % len(chapters)])
    return related


def process_folder(folder, chapters):
    """Process all files in a folder."""
    updated = 0
    for slug in chapters:
        fpath = os.path.join(folder, slug)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        related = get_related(chapters, slug)
        block = build_block(related)

        # Insert before </main>
        if '</main>' in content and '<!-- Related Notes -->' not in content:
            new_content = content.replace('</main>', block + '</main>', 1)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1
            print(f"  {slug} -> {related}")
        elif '<!-- Related Notes -->' in content:
            print(f"  SKIP (already exists): {slug}")
        else:
            print(f"  ERROR: no </main> found in {slug}")

    return updated


print("Physics:")
phys_updated = process_folder(os.path.join(BASE, "PHYSICS"), PHYSICS_FILES)

print("\nChemistry:")
chem_updated = process_folder(os.path.join(BASE, "chemistry"), CHEMISTRY_FILES)

print("\nMaths:")
math_updated = process_folder(os.path.join(BASE, "maths"), MATHS_FILES)

print(f"\nDone. Physics={phys_updated}, Chemistry={chem_updated}, Maths={math_updated}, Total={phys_updated + chem_updated + math_updated}")