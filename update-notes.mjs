import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const base = 'e:/jeeprepguide/jee';

const subjects = {
  physics: 'notes-physics.css',
  chemistry: 'notes-chemistry.css',
  maths: 'notes-maths.css',
};

let totalUpdated = 0;
let totalSkipped = 0;

for (const [subject, cssFile] of Object.entries(subjects)) {
  const dir = join(base, subject);
  const files = readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');
  console.log(`\n=== ${subject.toUpperCase()} (${files.length} files) ===`);

  for (const file of files) {
    const filePath = join(dir, file);
    let content = readFileSync(filePath, 'utf-8');
    let cssDone = false;
    let jsDone = false;

    // Skip if already has external CSS
    if (content.includes(`notes-${subject}.css`)) {
      cssDone = true;
    }
    // Skip if already has external JS
    if (content.includes('notes.js')) {
      jsDone = true;
    }

    // 1. Replace inline <style>...</style> block with CSS link
    // Match ANY style block that contains "font-family: 'Inter'" 
    const styleRegex = /\s*<style>[\s\S]*?font-family:\s*'Inter'[\s\S]*?<\/style>/;
    if (!cssDone && styleRegex.test(content)) {
      content = content.replace(styleRegex, `\n    <link rel="stylesheet" href="../assets/css/${cssFile}">`);
      cssDone = true;
      console.log(`  [CSS OK] ${file}`);
    } else if (!cssDone) {
      console.log(`  [CSS SKIP] ${file} - no matching style block`);
    } else {
      console.log(`  [CSS ALREADY] ${file}`);
    }

    // 2. Replace bottom inline <script> blocks containing Progress Bar or scroll tracking
    // Try multiple patterns
    if (!jsDone) {
      // Pattern 1: <!-- Scripts --> comment followed by script with Progress Bar
      const p1 = /\s*<!--\s*Scripts?\s*-->\s*\r?\n\s*<script>[\s\S]*?\/\/\s*Progress Bar[\s\S]*?<\/script>/;
      // Pattern 2: Script with Progress Bar (no comment)
      const p2 = /\s*<script>\s*\r?\n\s*\/\/\s*Progress Bar[\s\S]*?<\/script>\s*(?=\r?\n\s*<\/body>)/;
      // Pattern 3: Script with indented Progress Bar
      const p3 = /\s*<script>\s*\r?\n\s+\/\/\s*Progress Bar[\s\S]*?<\/script>\s*(?=\r?\n\s*<\/body>)/;
      // Pattern 4: <!-- Scripts --> then script with window.addEventListener('scroll'
      const p4 = /\s*<!--\s*Scripts?\s*-->\s*\r?\n\s*<script>\s*\r?\n\s*window\.addEventListener[\s\S]*?<\/script>\s*(?=\r?\n\s*<\/body>)/;
      // Pattern 5: Bare script with window.addEventListener before </body>
      const p5 = /\s*<script>\s*\r?\n\s*window\.addEventListener\('scroll'[\s\S]*?<\/script>\s*(?=\r?\n\s*<\/body>)/;

      const jsTag = `\n<!-- Scripts -->\n<script src="../assets/js/notes.js"></script>`;

      if (p1.test(content)) {
        content = content.replace(p1, jsTag);
        jsDone = true;
        console.log(`  [JS OK p1] ${file}`);
      } else if (p4.test(content)) {
        content = content.replace(p4, jsTag);
        jsDone = true;
        console.log(`  [JS OK p4] ${file}`);
      } else if (p2.test(content)) {
        content = content.replace(p2, jsTag);
        jsDone = true;
        console.log(`  [JS OK p2] ${file}`);
      } else if (p3.test(content)) {
        content = content.replace(p3, jsTag);
        jsDone = true;
        console.log(`  [JS OK p3] ${file}`);
      } else if (p5.test(content)) {
        content = content.replace(p5, jsTag);
        jsDone = true;
        console.log(`  [JS OK p5] ${file}`);
      } else {
        console.log(`  [JS SKIP] ${file} - no matching script block`);
      }
    } else {
      console.log(`  [JS ALREADY] ${file}`);
    }

    if (cssDone || jsDone) {
      writeFileSync(filePath, content, 'utf-8');
      totalUpdated++;
    } else {
      totalSkipped++;
    }
  }
}

console.log(`\n✅ Done! Updated: ${totalUpdated}, Skipped: ${totalSkipped}`);
