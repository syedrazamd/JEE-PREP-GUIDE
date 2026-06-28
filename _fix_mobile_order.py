"""Fix mobile content order on all 40 chapter notes pages.
Step 1: Hide Quick Navigation section on mobile (add hidden lg:block)
Step 2: Reorder sidebar vs main content on mobile (order-1/order-2)
"""
import re
import os

# Files to process (all chapter files, no index.html)
PHYSICS_FILES = [
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
]
CHEMISTRY_FILES = [
    "atomic-structure.html", "chemical-equilibrium.html", "chemical-kinetics.html",
    "electrochemistry.html", "ionic-equilibrium.html",
    "some-basic-concepts-of-chemistry.html", "states-of-matter.html",
    "surface-chemistry.html", "thermodynamics.html",
]
MATHS_FILES = [
    "complex-numbers.html", "permutations-and-combinations.html",
    "quadratic-equations.html", "relations-functions.html",
    "sequences-and-series.html", "sets.html",
]

BASE = r"e:\jeeprepguide\JEE"
PHYSICS_BASE = os.path.join(BASE, "PHYSICS")
CHEMISTRY_BASE = os.path.join(BASE, "chemistry")
MATHS_BASE = os.path.join(BASE, "maths")

# Files that should skip Step 1 (no Quick Navigation section)
SKIP_STEP1 = {"kinematics.html"}

# Step 2 replacements (exact byte-identical across all files)
ASIDE_OLD = '<aside class="lg:col-span-1">'
ASIDE_NEW = '<aside class="order-2 lg:order-1 lg:col-span-1">'
MAIN_OLD = '<main class="lg:col-span-3 space-y-12">'
MAIN_NEW = '<main class="order-1 lg:order-2 lg:col-span-3 space-y-12">'

# Step 1: regex to add hidden lg:block to Quick Navigation section
# Matches <section class="bg-gradient-to-r from-...py-6 border-b">
QUICK_NAV_RE = re.compile(
    r'(<section class=")(hidden lg:block )?(bg-gradient-to-r from-\S+ to-\S+ py-6 border-b")'
)

total = 0
step1_done = 0
step2_done = 0

for base, files in [(PHYSICS_BASE, PHYSICS_FILES), (CHEMISTRY_BASE, CHEMISTRY_FILES), (MATHS_BASE, MATHS_FILES)]:
    for fname in files:
        fpath = os.path.join(base, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        step1_changed = [False]  # mutable container to allow closure mutation
        step2_this = False

        def add_hidden(m):
            step1_changed[0] = True
            prefix = m.group(1)
            existing = m.group(2) or ""
            rest = m.group(3)
            return f'{prefix}{existing}hidden lg:block {rest}'
        content = QUICK_NAV_RE.sub(add_hidden, content)
        step1_this = step1_changed[0]

        # Step 2: reorder sidebar vs main content on mobile
        if ASIDE_OLD in content:
            content = content.replace(ASIDE_OLD, ASIDE_NEW, 1)
            step2_this = True
        if MAIN_OLD in content:
            content = content.replace(MAIN_OLD, MAIN_NEW, 1)
            step2_this = True

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            total += 1
            if step1_this:
                step1_done += 1
            if step2_this:
                step2_done += 1
            print(f"  Updated: {fname} (step1={step1_this}, step2={step2_this})")
        else:
            print(f"  No change: {fname}")

print(f"\nDone. {total} files updated.")
print(f"  Step 1 (Quick Nav hidden): {step1_done} files")
print(f"  Step 2 (Sidebar reorder): {step2_done} files")