"""
Add mobile navigation menu to all 40 chapter files.
Inserts hamburger button after first </nav> and mobile menu panel after the next </div>.
"""
import os
import re

BASE = r"e:\jeeprepguide"
CHAPTERS = [
    # Physics (20 files, excluding index.html)
    (r"JEE\PHYSICS", [
        "alternating-current", "atoms-and-nuclei", "capacitance",
        "centre-of-mass-and-collision", "current-electricity",
        "dual-nature-of-radiation-and-matter", "electromagnetic-induction",
        "electromagnetic-waves", "electrostatics", "fluid-mechanics",
        "gravitation", "kinematics", "kinetic-theory-of-gases",
        "laws-of-motion", "magnetic-effect-of-current-and-magnetism",
        "ray-optics", "rotational-motion", "semiconductors",
        "simple-harmonic-motion", "thermal-properties-of-matter",
        "thermodynamics", "units-and-dimensions", "wave-motion", "wave-optics"
    ]),
    # Chemistry (9 files, excluding index.html)
    (r"JEE\chemistry", [
        "atomic-structure", "chemical-equilibrium", "chemical-kinetics",
        "electrochemistry", "ionic-equilibrium",
        "some-basic-concepts-of-chemistry", "states-of-matter",
        "surface-chemistry", "thermodynamics"
    ]),
    # Maths (7 files, excluding index.html)
    (r"JEE\maths", [
        "complex-numbers", "permutations-and-combinations",
        "quadratic-equations", "relations-functions",
        "sequences-and-series", "sets"
    ]),
]

BUTTON = """                <!-- Mobile Menu Button -->
                <button class="md:hidden text-gray-700" onclick="toggleMobileMenu()" aria-label="Toggle navigation menu">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>"""

PANEL = """            <!-- Mobile Menu -->
            <div id="mobileMenu" class="hidden md:hidden pb-4">
                <div class="flex flex-col space-y-3 pt-2">
                    <a href="https://jeeprepguide.netlify.app" class="text-gray-700 hover:text-primary font-semibold">Home</a>
                    <a href="https://jeeprepguide.netlify.app/jee/physics" class="text-gray-700 hover:text-primary font-semibold">Physics</a>
                    <a href="https://jeeprepguide.netlify.app/jee/chemistry" class="text-gray-700 hover:text-primary font-semibold">Chemistry</a>
                    <a href="https://jeeprepguide.netlify.app/jee/maths" class="text-gray-700 hover:text-primary font-semibold">Maths</a>
                    <a href="https://jeeprepguide.netlify.app/blog" class="text-gray-700 hover:text-primary font-semibold">Blog</a>
                    <a href="#" class="bg-primary text-white px-6 py-2 rounded-full text-center font-semibold">Download PDF</a>
                </div>
            </div>"""


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the first <nav...>...</nav> block
    nav_match = re.search(r'<nav[^>]*>.*?</nav>', content, re.DOTALL)
    if not nav_match:
        print(f"  SKIP: No <nav> found in {filepath}")
        return False

    nav_end = nav_match.end()

    # After </nav>, we expect: </div>\n        </div>\n    </header>
    # Insert button right after </nav> (before the next </div>)
    # Insert panel after that first </div> (before the second </div>)

    # Find the first </div> after </nav>
    rest = content[nav_end:]
    div1_match = re.search(r'</div>', rest)
    if not div1_match:
        print(f"  SKIP: No </div> after </nav> in {filepath}")
        return False

    div1_end = nav_end + div1_match.end()

    # Find the second </div> after the first
    rest2 = content[div1_end:]
    div2_match = re.search(r'</div>', rest2)
    if not div2_match:
        print(f"  SKIP: No second </div> in {filepath}")
        return False

    div2_end = div1_end + div2_match.end()

    # Build new content
    # Part 1: up to nav_end (includes </nav>)
    # Part 2: button + rest up to div1_end (includes first </div>)
    # Part 3: panel + rest from div1_end onward
    new_content = (
        content[:nav_end] + '\n' +
        BUTTON + '\n' +
        content[nav_end:div1_end] + '\n' +
        PANEL + '\n' +
        content[div1_end:]
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  OK: {filepath}")
    return True


def main():
    total = 0
    for folder, chapters in CHAPTERS:
        for chapter in chapters:
            filepath = os.path.join(BASE, folder, chapter + '.html')
            if not os.path.exists(filepath):
                print(f"  MISSING: {filepath}")
                continue
            if process_file(filepath):
                total += 1

    print(f"\nTotal files updated: {total}")


if __name__ == '__main__':
    main()