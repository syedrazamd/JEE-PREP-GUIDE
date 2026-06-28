"""Add mobile menu to the one missing file: work-energy-and-power.html"""
import re

filepath = r"e:\jeeprepguide\JEE\PHYSICS\work-energy-and-power.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

nav_match = re.search(r'<nav[^>]*>.*?</nav>', content, re.DOTALL)
nav_end = nav_match.end()
rest = content[nav_end:]
div1_match = re.search(r'</div>', rest)
div1_end = nav_end + div1_match.end()

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

new_content = (
    content[:nav_end] + '\n' +
    BUTTON + '\n' +
    content[nav_end:div1_end] + '\n' +
    PANEL + '\n' +
    content[div1_end:]
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('OK')