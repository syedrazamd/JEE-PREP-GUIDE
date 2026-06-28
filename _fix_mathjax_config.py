"""
Fix MathJax configuration race condition.
Step 1: Add inline MathJax config in <head> before the async script tag (all 40 files).
Step 2: Remove the now-redundant config from notes.js.
"""

import os
import re

BASE = r"e:\jeeprepguide\jee"
NOTESJS = os.path.join(BASE, "assets", "js", "notes.js")

CHAPTER_FILES = [
    r"physics\alternating-current.html",
    r"physics\atoms-and-nuclei.html",
    r"physics\capacitance.html",
    r"physics\centre-of-mass-and-collision.html",
    r"physics\current-electricity.html",
    r"physics\dual-nature-of-radiation-and-matter.html",
    r"physics\electromagnetic-induction.html",
    r"physics\electromagnetic-waves.html",
    r"physics\electrostatics.html",
    r"physics\fluid-mechanics.html",
    r"physics\gravitation.html",
    r"physics\kinematics.html",
    r"physics\kinetic-theory-of-gases.html",
    r"physics\laws-of-motion.html",
    r"physics\magnetic-effect-of-current-and-magnetism.html",
    r"physics\ray-optics.html",
    r"physics\rotational-motion.html",
    r"physics\semiconductors.html",
    r"physics\simple-harmonic-motion.html",
    r"physics\thermal-properties-of-matter.html",
    r"physics\thermodynamics.html",
    r"physics\units-and-dimensions.html",
    r"physics\wave-motion.html",
    r"physics\wave-optics.html",
    r"physics\work-energy-and-power.html",
    r"chemistry\atomic-structure.html",
    r"chemistry\chemical-equilibrium.html",
    r"chemistry\chemical-kinetics.html",
    r"chemistry\electrochemistry.html",
    r"chemistry\ionic-equilibrium.html",
    r"chemistry\some-basic-concepts-of-chemistry.html",
    r"chemistry\states-of-matter.html",
    r"chemistry\surface-chemistry.html",
    r"chemistry\thermodynamics.html",
    r"maths\complex-numbers.html",
    r"maths\permutations-and-combinations.html",
    r"maths\quadratic-equations.html",
    r"maths\relations-functions.html",
    r"maths\sequences-and-series.html",
    r"maths\sets.html",
]

INLINE_CONFIG = """<script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']],
            processEscapes: true
        },
        svg: {
            fontCache: 'global'
        },
        options: {
            skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
        }
    };
</script>
"""

# ── STEP 1: Add inline config before MathJax script tag ──────────────
print("=== STEP 1: Adding inline MathJax config in <head> ===")
ok = 0
missing = []
no_tag = []

for rel in CHAPTER_FILES:
    fp = os.path.join(BASE, rel)
    if not os.path.exists(fp):
        missing.append(rel)
        continue
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(
        r'(<!-- MathJax for LaTeX Rendering -->\s*<script id="MathJax-script"[^>]*></script>)',
        content,
        re.IGNORECASE,
    )
    if not m:
        no_tag.append(rel)
        continue

    # Skip if inline config already present before the script tag
    if "window.MathJax" in content[: m.start()]:
        ok += 1
        continue

    new_content = content[: m.start()] + INLINE_CONFIG + content[m.start() :]
    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_content)
    ok += 1

print(f"  Processed: {ok}/40 files")
for e in missing:
    print(f"  [MISSING] {e}")
for e in no_tag:
    print(f"  [NO SCRIPT TAG] {e}")

# ── STEP 2: Remove MathJax config from notes.js ─────────────────────
print()
print("=== STEP 2: Removing MathJax config from notes.js ===")

with open(NOTESJS, "r", encoding="utf-8") as f:
    notes = f.read()

# Use regex to find and remove the block (handles unicode box-drawing chars)
pattern = r"\n*// \u2500\u2500 MathJax Configuration \u2500+\nwindow\.MathJax = \{[^}]+\}[^}]+\}[^}]+\};\n*"
new_notes, count = re.subn(pattern, "\n", notes)

if count > 0:
    with open(NOTESJS, "w", encoding="utf-8") as f:
        f.write(new_notes)
    print(f"  Removed MathJax config block from notes.js ({count} match(es))")
else:
    print("  MathJax config block not found in notes.js -- may already be removed")

print()
print("Done.")
