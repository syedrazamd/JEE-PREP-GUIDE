import os
import re
import sys
import time
import subprocess
import webbrowser
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CHAPTERS_FILE = "chapters_to_publish.txt"
PROCESSED_FILE = "processed_chapters.txt"
MAX_CHAPTERS_PER_RUN = 2
BASE_URL = "https://jeeprepguide.netlify.app"

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text).strip('-')

def get_chapters_to_process():
    if not os.path.exists(CHAPTERS_FILE):
        return []
    
    processed = set()
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            processed = set([line.strip() for line in f if line.strip()])
            
    to_process = []
    current_section = "general" # Default
    
    with open(CHAPTERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Check if it's a section header (e.g. ⚗️ Physical Chemistry, 🚀 Mechanics)
            if '|' not in line:
                line_lower = line.lower()
                if 'physical' in line_lower:
                    current_section = 'physical'
                elif 'inorganic' in line_lower:
                    current_section = 'inorganic'
                elif 'organic' in line_lower:
                    current_section = 'organic'
                elif 'mechanics' in line_lower:
                    current_section = 'mechanics'
                elif 'thermodynamics' in line_lower:
                    current_section = 'thermodynamics'
                elif 'waves' in line_lower:
                    current_section = 'waves'
                elif 'electromagnetism' in line_lower:
                    current_section = 'electromagnetism'
                elif 'optics' in line_lower:
                    current_section = 'optics'
                elif 'modern' in line_lower:
                    current_section = 'modern'
                elif 'maths' in line_lower or 'algebra' in line_lower:
                    current_section = 'maths'
                continue
                
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                subj_raw = parts[0]
                emoji = "📚"
                # Extract emoji if present
                emoji_match = re.match(r'^([^\w\s]+)\s*(.*)', subj_raw)
                if emoji_match:
                    emoji = emoji_match.group(1).strip()
                    subject = emoji_match.group(2).lower()
                else:
                    subject = subj_raw.lower()
                    
                name, explanation = parts[1], parts[2]
                
                if name not in processed:
                    to_process.append((subject, name, explanation, current_section, emoji))
                    
    return to_process[:MAX_CHAPTERS_PER_RUN]

def mark_as_processed(chapter_name):
    with open(PROCESSED_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{chapter_name}\n")

def generate_thumbnail(subject, chapter_name, slug):
    print(f"Generating thumbnail for {chapter_name} using Gemini Imagen...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return False
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"A highly detailed, visually appealing educational infographic about {chapter_name} for JEE {subject}. Include clean diagrams, key formulas, and structured panels with modern styling. Do not hallucinate symbols."
    
    try:
        response = client.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type='image/png'
            )
        )
        
        img_bytes = response.generated_images[0].image.image_bytes
        img = Image.open(BytesIO(img_bytes))
        
        os.makedirs(f"jee/{subject}/{slug}", exist_ok=True)
        img_path = f"jee/{subject}/{slug}/{slug}.png"
        img.save(img_path)
        return img_path
    except Exception as e:
        print(f"Failed to generate thumbnail via Imagen: {e}")
        print("Falling back to basic Pillow generation...")
        width, height = 1200, 630
        
        bg_color = (37, 99, 235) if subject == 'chemistry' else (147, 51, 234)
        
        img = Image.new('RGB', (width, height), color=bg_color)
        d = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 80)
            font_sub = ImageFont.truetype("arial.ttf", 40)
        except:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
        d.text((100, 250), chapter_name, font=font_title, fill=(255, 255, 255))
        d.text((100, 360), f"Complete JEE {subject.capitalize()} Notes & PYQs", font=font_sub, fill=(200, 200, 255))
        
        os.makedirs(f"jee/{subject}/{slug}", exist_ok=True)
        img_path = f"jee/{subject}/{slug}/{slug}.png"
        img.save(img_path)
        return img_path

def generate_html_content(subject, chapter_name, explanation, slug):
    print(f"Generating HTML content for {chapter_name} via Gemini...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return False
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert web developer and JEE educator. 
    I need you to generate a full, premium HTML page for a new JEE {subject} chapter called "{chapter_name}".
    The single-line explanation of this chapter is: {explanation}.
    The URL path will be `https://jeeprepguide.netlify.app/jee/{subject}/{slug}`.
    The featured image is at `https://jeeprepguide.netlify.app/jee/{subject}/{slug}/{slug}.png`.
    
    ### IMPORTANT: UI/UX INSTRUCTIONS
    You MUST strictly follow the exact UI/UX and code structure of my "Units and Dimensions" page. 
    Use the following skeleton but adapt it for "{chapter_name}":

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{chapter_name} for JEE 2025-26 | Complete Notes with Formulas & Solved Examples</title>
        <meta name="description" content="Master {chapter_name} for JEE Main & Advanced with complete notes, formulas, shortcuts & PYQ analysis. 100% free study material.">
        <!-- Include all SEO tags: og:title, og:description, twitter card, canonical (https://jeeprepguide.netlify.app/jee/{subject}/{slug}), etc. -->
        
        <!-- Fonts & Scripts -->
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>

        <!-- JSON-LD Schemas -->
        <!-- Generate accurate BreadcrumbList, Article, LearningResource, FAQPage (with 5-6 FAQs), HowTo, and Course schemas for {chapter_name} -->

        <style>
            /* Include the custom styles from the template: topic-card, formula-box, example-box, math-display, etc. */
            body {{ font-family: 'Inter', sans-serif; }}
            .topic-card {{ transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
            .topic-card:hover {{ transform: translateY(-6px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }}
            .formula-box {{ background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); }}
            .example-box {{ background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); }}
            .math-display {{ font-size: 1.1rem; padding: 1rem; margin: 1rem 0; overflow-x: auto; }}
        </style>
    </head>
    <body class="bg-gradient-to-br from-gray-50 to-blue-50 text-gray-800">
        <!-- Progress Bar, Header, Breadcrumb (Update to Home > JEE > {subject.capitalize()} > {chapter_name}) -->
        
        <!-- Hero Section with bg-gradient-to-br from-primary via-blue-600 to-secondary -->
        
        <!-- Main Content Grid (3 columns for content, 1 for sticky sidebar TOC) -->
        
        <!-- Content Sections (At least 5-7 detailed chapters/topics) -->
        <!-- Use formula-box for formulas, example-box for solved problems, and custom-table for data -->
        
        <!-- Previous Year Questions Analysis (Detailed weightage and repeated question types) -->
        
        <!-- Practice Problem Set (Level 1, 2, and 3) -->
        
        <!-- Related Notes Section & Footer -->
    </body>
    </html>
    ```

    ### CONTENT REQUIREMENTS:
    1. **Depth**: Provide comprehensive, high-quality educational content. Not just a summary.
    2. **LaTeX**: Use MathJax `\\( ... \\)` for inline and `\\[ ... \\]` for display math.
    3. **Solved Examples**: Include at least 5-10 detailed solved examples across the page.
    4. **SEO**: Ensure the JSON-LD schemas are valid and fully populated.
    5. **Visuals**: Mention the featured image at `https://jeeprepguide.netlify.app/jee/{subject}/{slug}/{slug}.png`.
    
    Output ONLY the raw HTML code. No markdown formatting.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        html_content = response.text
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        with open(f"jee/{subject}/{slug}/index.html", "w", encoding='utf-8') as f:
            f.write(html_content.strip())
        return True
    except Exception as e:
        print(f"Failed to generate HTML: {e}")
        return False

def update_subject_index(subject, chapter_name, explanation, slug, section, emoji):
    print(f"Updating {subject} index.html...")
    index_file = f"jee/{subject}/index.html"
    
    if not os.path.exists(index_file):
        print(f"Index file {index_file} not found.")
        return
        
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Determine theme and marker based on subject and section
    if subject == 'chemistry':
        if section == 'physical':
            theme_class, hover_class = "cat-physical", "group-hover:text-blue-600 text-blue-600"
            marker = "<!-- ADD_NEW_PHYSICAL_CHAPTER -->"
        elif section == 'inorganic':
            theme_class, hover_class = "cat-inorganic", "group-hover:text-red-500 text-red-500"
            marker = "<!-- ADD_NEW_INORGANIC_CHAPTER -->"
        elif section == 'organic':
            theme_class, hover_class = "cat-organic", "group-hover:text-emerald-600 text-emerald-600"
            marker = "<!-- ADD_NEW_ORGANIC_CHAPTER -->"
        else:
            theme_class, hover_class = "cat-physical", "group-hover:text-blue-600 text-blue-600"
            marker = "<!-- ADD_NEW_CHEMISTRY_CHAPTER -->"
    elif subject == 'maths':
        theme_class, hover_class = "cat-algebra", "group-hover:text-purple-600 text-purple-600"
        marker = "<!-- ADD_NEW_MATHS_CHAPTER -->"
    elif subject == 'physics':
        # Physics sections mapping
        sections_map = {
            'mechanics': ("cat-mechanics", "group-hover:text-primary text-primary"),
            'thermodynamics': ("cat-thermodynamics", "group-hover:text-danger text-danger"),
            'waves': ("cat-waves", "group-hover:text-success text-success"),
            'electromagnetism': ("cat-electromagnetism", "group-hover:text-accent text-accent"),
            'optics': ("cat-optics", "group-hover:text-purple-500 text-purple-500"),
            'modern': ("cat-modern", "group-hover:text-pink-500 text-pink-500")
        }
        theme_class, hover_class = sections_map.get(section.lower(), ("cat-mechanics", "group-hover:text-primary text-primary"))
        marker = f"<!-- ADD_NEW_{section.upper()}_CHAPTER -->"
    else:
        theme_class, hover_class = "cat-mechanics", "group-hover:text-primary text-primary"
        marker = f"<!-- ADD_NEW_{subject.upper()}_CHAPTER -->"

    if marker not in content:
        print(f"Marker {marker} not found in {index_file}.")
        return

    card_html = f"""
                    <a href="{BASE_URL}/jee/{subject}/{slug}" class="chapter-card bg-white border-l-4 {theme_class} p-6 rounded-2xl shadow-lg card-hover group" data-category="{section}" data-status="available">
                        <div class="flex items-center justify-between mb-4">
                            <span class="cat-badge text-white px-3 py-1 rounded-full text-sm font-bold">New</span>
                            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">✓ Available</span>
                        </div>
                        <div class="text-4xl mb-4">{emoji}</div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-3 {hover_class.split()[0]} transition">
                            {chapter_name}
                        </h3>
                        <p class="text-gray-600 mb-4">
                            {explanation}
                        </p>
                        <div class="flex items-center justify-between text-sm">
                            <div class="flex items-center space-x-4 text-gray-500">
                                <span>⏱️ 3 hrs</span>
                                <span>📝 100+ MCQs</span>
                            </div>
                            <span class="{hover_class.split()[1]} font-bold group-hover:translate-x-2 transition-transform">
                                Read →
                            </span>
                        </div>
                    </a>

                    {marker}"""

    content = content.replace(marker, card_html)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)

def update_sitemap(subject, slug):
    print("Updating sitemap.xml...")
    sitemap_file = "sitemap.xml"
    if not os.path.exists(sitemap_file):
        return
        
    with open(sitemap_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    today = datetime.today().strftime('%Y-%m-%d')
    url_block = f"""  <url>
    <loc>{BASE_URL}/jee/{subject}/{slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.80</priority>
  </url>
</urlset>"""

    content = content.replace("</urlset>", url_block)
    
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write(content)

def git_push(chapter_names):
    print("Pushing to GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = f"Auto-publish chapters: {', '.join(chapter_names)}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except Exception as e:
        print(f"Git operation failed: {e}")
        return False

def google_indexing(urls):
    print("Submitting to Google Indexing API...")
    KEY_FILE = 'jee-prep-guide-indexing-384648cedaea.json'
    if not os.path.exists(KEY_FILE):
        print(f"Indexing key {KEY_FILE} not found.")
        return
        
    try:
        credentials = service_account.Credentials.from_service_account_file(
            KEY_FILE, scopes=['https://www.googleapis.com/auth/indexing']
        )
        service = build('indexing', 'v3', credentials=credentials)
        
        for url in urls:
            body = {
                "url": url,
                "type": "URL_UPDATED"
            }
            response = service.urlNotifications().publish(body=body).execute()
            print(f"Indexing response for {url}: {response}")
            
        requests.get(f"https://www.google.com/ping?sitemap={BASE_URL}/sitemap.xml")
        print("Sitemap pinged successfully.")
    except Exception as e:
        print(f"Google Indexing failed: {e}")

def main():
    chapters = get_chapters_to_process()
    if not chapters:
        print("No new chapters to process.")
        return
        
    print(f"Found {len(chapters)} chapters to process.")
    
    published_urls = []
    chapter_names = []
    
    for subject, name, explanation, section, emoji in chapters:
        print(f"\n--- Processing: {name} ({subject}) in section ({section}) ---")
        slug = slugify(name)
        
        generate_thumbnail(subject, name, slug)
        
        success = generate_html_content(subject, name, explanation, slug)
        if success:
            update_subject_index(subject, name, explanation, slug, section, emoji)
            update_sitemap(subject, slug)
            mark_as_processed(name)
            published_urls.append(f"{BASE_URL}/jee/{subject}/{slug}")
            chapter_names.append(name)
        else:
            print(f"Skipping updates for {name} due to generation failure.")
            
    if published_urls:
        git_push(chapter_names)
        google_indexing(published_urls)
        
        print("\nOpening URLs in browser for Pinterest saving...")
        for url in published_urls:
            webbrowser.open(url)
            time.sleep(2)
            
        print("\nAll done! Please use your Pinterest extension to save the newly opened pages.")

if __name__ == "__main__":
    # Option 1: Run once immediately (Default)
    # main()
    
    # Option 2: Run continuously every 24 hours
    # If you want to keep your computer running and have this run automatically,
    # comment out `main()` above by adding a # in front of it, and uncomment the lines below:
    
    print("Starting 24-hour automation loop...")
    while True:
        main()
        print("\nWaiting 24 hours before publishing the next batch...")
        time.sleep(86400) # 86400 seconds = 24 hours
