import os
import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://jeeprepguide.netlify.app"

SUBJECT_CONFIG = {
    "chemistry": {
        "index_path": os.path.join(PROJECT_ROOT, "jee", "chemistry", "index.html"),
        "notes_folder": os.path.join(PROJECT_ROOT, "jee", "chemistry"),
        "url_prefix": "/jee/chemistry/",
    },
    "maths": {
        "index_path": os.path.join(PROJECT_ROOT, "jee", "maths", "index.html"),
        "notes_folder": os.path.join(PROJECT_ROOT, "jee", "maths"),
        "url_prefix": "/jee/maths/",
    },
    "physics": {
        "index_path": os.path.join(PROJECT_ROOT, "jee", "physics", "index.html"),
        "notes_folder": os.path.join(PROJECT_ROOT, "jee", "physics"),
        "url_prefix": "/jee/physics/",
    },
}

SITEMAP_PATH = os.path.join(PROJECT_ROOT, "sitemap.xml")

# Emoji mapping for different topics
TOPIC_EMOJIS = {
    "solutions": "🧪",
    "ionic equilibrium": "🧊",
    "chemical bonding": "🔗",
    "atomic structure": "⚛️",
    "thermodynamics": "🔥",
    "electrochemistry": "🔋",
    "organic chemistry": "🧬",
    "redox reactions": "⚡",
    "coordination compounds": "💎",
    "polymers": "🔬",
    "binomial theorem": "📊",
    "calculus": "∫",
    "trigonometry": "📐",
    "mechanics": "⚙️",
    "optics": "🔬",
    "default": "📚"
}


def slugify(topic_name):
    """Convert topic name to URL slug."""
    slug = topic_name.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug


def get_emoji(topic):
    """Get emoji for topic."""
    topic_lower = topic.lower()
    return TOPIC_EMOJIS.get(topic_lower, TOPIC_EMOJIS["default"])


# ============================================================
# STEP 1: GENERATE IMAGE USING GEMINI (PNG FORMAT)
# ============================================================
def generate_image(topic, subject, save_path):
    """Generate a topic image using Gemini API in PNG format."""
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""Generate an image which is suitable for Google Discover for JEE notes of chapter "{topic}".

Requirements:
- High quality, professional educational thumbnail
- 1200x630 pixels (ideal for Google Discover and social sharing)
- Modern gradient background (blue/purple/teal tones)
- Include relevant scientific diagrams, formulas, or symbols related to "{topic}"
- Bold, clear text showing "{topic}" prominently
- Clean, minimal design
- Appealing to Indian JEE/engineering students
- Suitable for Google Discover feed
- Professional and trustworthy appearance"""

    print(f"🎨 Generating image for '{topic}' using Gemini...")

    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    try:
        response = model.generate_content(prompt)
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = part.inline_data.data
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                print(f"✅ Image saved to {save_path}")
                return True
    except Exception as e:
        print(f"⚠️ Gemini image generation failed: {e}")
        print("📝 Creating placeholder image instead...")
        create_placeholder_image(topic, save_path)
        return True

    create_placeholder_image(topic, save_path)
    return True


def create_placeholder_image(topic, save_path):
    """Create a simple placeholder image if Gemini fails (PNG format)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (1200, 630), color=(26, 35, 126))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 60)
            small_font = ImageFont.truetype("arial.ttf", 32)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
            except:
                font = ImageFont.load_default()
                small_font = font
        
        for y in range(630):
            color_value = int(26 + (y / 630) * 100)
            draw.rectangle([(0, y), (1200, y+1)], fill=(color_value, color_value+20, 126))
        
        draw.text((100, 250), topic, fill="white", font=font)
        draw.text((100, 350), "JEE Prep Guide - Complete Notes", fill=(200, 200, 255), font=small_font)
        
        img.save(save_path, 'PNG', quality=95)
        print(f"✅ Placeholder image saved to {save_path}")
    except ImportError:
        print("⚠️ Pillow not installed. Skipping image generation.")
        print(f"   Install with: pip install Pillow")


# ============================================================
# STEP 2: CREATE FOLDER STRUCTURE AND MOVE HTML FILE
# ============================================================
def setup_notes_folder(topic, subject, html_source_path):
    """Create folder and move HTML file to correct location."""
    slug = slugify(topic)
    config = SUBJECT_CONFIG[subject]

    notes_folder = os.path.join(config["notes_folder"], slug)
    os.makedirs(notes_folder, exist_ok=True)

    html_dest_path = os.path.join(notes_folder, "index.html")
    
    if os.path.exists(html_source_path):
        import shutil
        shutil.move(html_source_path, html_dest_path)
        print(f"✅ Moved HTML to: {html_dest_path}")
    else:
        print(f"❌ Source HTML file not found: {html_source_path}")
        sys.exit(1)

    return notes_folder, slug


# ============================================================
# STEP 3: UPDATE SUBJECT INDEX PAGE
# ============================================================
def update_subject_index(topic, subject, slug, chapter_num=None, description="", read_time="3 hrs"):
    """Add a chapter card to the subject's index.html."""
    config = SUBJECT_CONFIG[subject]
    index_path = config["index_path"]

    if not os.path.exists(index_path):
        print(f"⚠️ Index file not found: {index_path}")
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    emoji = get_emoji(topic)

    card_html = f"""                    <!-- Ch {chapter_num or '?'}: {topic} -->
                    <a href="{slug}/" class="chapter-card bg-white border-l-4 cat-physical p-6 rounded-2xl shadow-lg card-hover group" data-category="physical" data-status="available">
                        <div class="flex items-center justify-between mb-4">
                            <span class="cat-badge text-white px-3 py-1 rounded-full text-sm font-bold">Ch. {chapter_num or '?'}</span>
                            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">✓ Available</span>
                        </div>
                        <div class="text-4xl mb-4">{emoji}</div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition">
                            {topic}
                        </h3>
                        <p class="text-gray-600 mb-4">
                            {description}
                        </p>
                        <div class="flex items-center justify-between text-sm">
                            <div class="flex items-center space-x-4 text-gray-500">
                                <span>⏱️ {read_time}</span>
                                <span>📝 150+ MCQs</span>
                            </div>
                            <span class="text-blue-600 font-bold group-hover:translate-x-2 transition-transform">
                                Read →
                            </span>
                        </div>
                    </a>
"""

    marker = "<!-- ADD_NEW_CHAPTER_HERE -->"
    if marker in content:
        content = content.replace(marker, card_html + "\n" + marker)
    else:
        print(f"⚠️ Marker '{marker}' not found in {index_path}")
        print(f"\n   Add this card manually:")
        print(f"\n{'='*60}")
        print(card_html)
        print(f"{'='*60}\n")
        return

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Chapter card added to {index_path}")


# ============================================================
# STEP 4: UPDATE SITEMAP.XML
# ============================================================
def update_sitemap(subject, slug):
    """Add new URL to sitemap.xml."""
    config = SUBJECT_CONFIG[subject]
    today = datetime.now().strftime("%Y-%m-%d")
    new_url = f"{SITE_URL}{config['url_prefix']}{slug}/"

    if not os.path.exists(SITEMAP_PATH):
        print(f"⚠️ Sitemap not found: {SITEMAP_PATH}")
        return

    with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if new_url in content:
        print(f"⚠️ URL already in sitemap: {new_url}")
        return

    sitemap_entry = f"""  <url>
    <loc>{new_url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""

    content = content.replace("</urlset>", f"{sitemap_entry}\n</urlset>")

    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Sitemap updated with: {new_url}")


# ============================================================
# STEP 5: GIT PUSH
# ============================================================
def git_push(topic, subject):
    """Stage, commit, and push all changes to GitHub."""
    print(f"\n📤 Pushing to GitHub...")

    try:
        subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT, check=True)
        commit_msg = f"Add {subject} notes: {topic}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_ROOT, check=True)
        subprocess.run(["git", "push"], cwd=PROJECT_ROOT, check=True)
        print(f"✅ Pushed to GitHub: '{commit_msg}'")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push failed: {e}")


# ============================================================
# STEP 6: SUBMIT TO GOOGLE SEARCH CONSOLE
# ============================================================
def submit_to_gsc(subject, slug):
    """Submit URL to Google Search Console for indexing."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        new_url = f"{SITE_URL}{SUBJECT_CONFIG[subject]['url_prefix']}{slug}/"
        SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, "gsc-credentials.json")

        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            print(f"⚠️ GSC credentials not found")
            print(f"   Manually submit: {new_url}")
            return

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/indexing"]
        )
        service = build("indexing", "v3", credentials=credentials)

        body = {"url": new_url, "type": "URL_UPDATED"}
        response = service.urlNotifications().publish(body=body).execute()
        print(f"✅ Submitted to GSC: {new_url}")
    except Exception as e:
        print(f"⚠️ GSC submission failed: {e}")


# ============================================================
# MAIN
# ============================================================
def main():
    if len(sys.argv) < 4:
        print("Usage: python automate.py \"Topic Name\" subject path/to/notes.html [chapter_num] [description] [read_time]")
        print("\nExample:")
        print('  python automate.py "Electrochemistry" chemistry .\\electrochemistry.html 8 "Cells, Nernst equation" "4 hrs"')
        sys.exit(1)

    topic = sys.argv[1]
    subject = sys.argv[2].lower()
    html_source = sys.argv[3]
    chapter_num = sys.argv[4] if len(sys.argv) > 4 else None
    description = sys.argv[5] if len(sys.argv) > 5 else f"Complete {topic} notes for JEE"
    read_time = sys.argv[6] if len(sys.argv) > 6 else "3 hrs"

    if subject not in SUBJECT_CONFIG:
        print(f"❌ Invalid subject: {subject}")
        sys.exit(1)

    slug = slugify(topic)

    print(f"\n{'='*60}")
    print(f"🚀 JEE PREP GUIDE - AUTO PUBLISHER")
    print(f"{'='*60}")
    print(f"📚 Topic: {topic}")
    print(f"📂 Subject: {subject.upper()}")
    print(f"🔗 Slug: {slug}")
    print(f"🌐 URL: {SITE_URL}{SUBJECT_CONFIG[subject]['url_prefix']}{slug}/")
    print(f"{'='*60}\n")

    notes_folder, slug = setup_notes_folder(topic, subject, html_source)
    
    image_path = os.path.join(notes_folder, f"{slug}.png")
    generate_image(topic, subject, image_path)
    
    update_subject_index(topic, subject, slug, chapter_num, description, read_time)
    update_sitemap(subject, slug)
    git_push(topic, subject)
    
    print(f"\n⏳ Waiting 60 seconds for Netlify deploy...")
    import time
    time.sleep(60)
    submit_to_gsc(subject, slug)

    print(f"\n{'='*60}")
    print(f"🎉 ALL DONE!")
    print(f"🔗 {SITE_URL}{SUBJECT_CONFIG[subject]['url_prefix']}{slug}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()