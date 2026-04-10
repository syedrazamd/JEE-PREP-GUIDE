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


def slugify(topic_name):
    """Convert topic name to URL slug."""
    slug = topic_name.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug


# ============================================================
# STEP 1: GENERATE IMAGE USING GEMINI
# ============================================================
def generate_image(topic, subject, save_path):
    """Generate a topic image using Gemini API."""
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""Create an educational illustration/thumbnail for JEE {subject} chapter: "{topic}". 
    The image should be:
    - Clean, modern, and professional
    - Have a gradient background (blue/purple tones)
    - Include relevant scientific/mathematical symbols or diagrams
    - Have the text "{topic}" prominently displayed
    - Suitable as a blog/article thumbnail (1200x630 aspect ratio)
    - Educational and appealing to Indian engineering students
    """

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
    """Create a simple placeholder image if Gemini fails."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (1200, 630), color=(26, 35, 126))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except:
            font = ImageFont.load_default()
            small_font = font
        draw.text((100, 250), topic, fill="white", font=font)
        draw.text((100, 330), "JEE Prep Guide - Complete Notes", fill=(200, 200, 255), font=small_font)
        img.save(save_path, 'WEBP', quality=85)
        print(f"✅ Placeholder image saved to {save_path}")
    except ImportError:
        print("⚠️ Pillow not installed. Skipping image generation.")
        print(f"   Please manually add image at: {save_path}")


# ============================================================
# STEP 2: CREATE FOLDER STRUCTURE AND MOVE HTML FILE
# ============================================================
def setup_notes_folder(topic, subject, html_source_path):
    """Create folder and move HTML file to correct location."""
    slug = slugify(topic)
    config = SUBJECT_CONFIG[subject]

    # Create folder: jee/chemistry/chemical-bonding/
    notes_folder = os.path.join(config["notes_folder"], slug)
    os.makedirs(notes_folder, exist_ok=True)

    # Move HTML file
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
# STEP 3: UPDATE SUBJECT INDEX PAGE (Add card)
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

    # Use relative path from subject index
    card_html = f"""
<a href="{slug}/" class="chapter-card" style="text-decoration:none;">
    <div class="chapter-badge">
        <span class="badge available">Ch. {chapter_num or '?'}</span>
        <span class="status-badge available">Available</span>
    </div>
    <h3>{topic}</h3>
    <p>{description}</p>
    <div class="chapter-meta">
        <span>{read_time}</span>
        <span>130+ MCQs</span>
    </div>
    <span class="read-btn">Read <span>→</span></span>
</a>
"""

    marker = "<!-- ADD_NEW_CHAPTER_HERE -->"
    if marker in content:
        content = content.replace(marker, card_html + "\n" + marker)
    else:
        print(f"⚠️ Marker '{marker}' not found in {index_path}")
        print(f"   Please add this marker where new cards should appear.")
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

    sitemap_entry = f"""
  <url>
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
        print('  python automate.py "Chemical Bonding" chemistry ./chemical-bonding.html 7 "VSEPR theory, hybridization" "4 hrs"')
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

    # Step 1: Setup folder and move HTML
    notes_folder, slug = setup_notes_folder(topic, subject, html_source)

    # Step 2: Generate image
    image_path = os.path.join(notes_folder, f"{slug}.webp")
    generate_image(topic, subject, image_path)

    # Step 3: Update subject index (ONLY THIS, NOT MAIN INDEX)
    update_subject_index(topic, subject, slug, chapter_num, description, read_time)

    # Step 4: Update sitemap
    update_sitemap(subject, slug)

    # Step 5: Git push
    git_push(topic, subject)

    # Step 6: Wait and submit to GSC
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