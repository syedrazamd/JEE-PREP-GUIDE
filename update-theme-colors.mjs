import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const base = 'e:/jeeprepguide/jee';

const themes = {
  physics: {
    primary: '#7c3aed',
    secondary: '#6d28d9',
    progressGrad: 'linear-gradient(to right, #7c3aed, #a855f7)',
    bodyClass: 'bg-gradient-to-br from-gray-50 to-purple-50 text-gray-800',
    heroFrom: 'from-primary via-purple-600 to-secondary',
  },
  chemistry: {
    primary: '#059669',
    secondary: '#047857',
    progressGrad: 'linear-gradient(to right, #059669, #34d399)',
    bodyClass: 'bg-gradient-to-br from-gray-50 to-emerald-50 text-gray-800',
    heroFrom: 'from-primary via-emerald-600 to-secondary',
  },
  maths: {
    primary: '#e11d48',
    secondary: '#be123c',
    progressGrad: 'linear-gradient(to right, #e11d48, #fb7185)',
    bodyClass: 'bg-gradient-to-br from-gray-50 to-rose-50 text-gray-800',
    heroFrom: 'from-primary via-rose-600 to-secondary',
  },
};

for (const [subject, theme] of Object.entries(themes)) {
  const dir = join(base, subject);
  const files = readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');
  console.log(`\n=== ${subject.toUpperCase()} ===`);

  for (const file of files) {
    const filePath = join(dir, file);
    let content = readFileSync(filePath, 'utf-8');
    let changes = [];

    // 1. Update tailwind.config primary color
    const oldPrimary = /primary:\s*'#[0-9a-fA-F]{6}'/;
    if (oldPrimary.test(content)) {
      content = content.replace(oldPrimary, `primary: '${theme.primary}'`);
      changes.push('primary');
    }

    // 2. Update tailwind.config secondary color
    const oldSecondary = /secondary:\s*'#[0-9a-fA-F]{6}'/;
    if (oldSecondary.test(content)) {
      content = content.replace(oldSecondary, `secondary: '${theme.secondary}'`);
      changes.push('secondary');
    }

    // 3. Update progress bar gradient (inline style)
    const progressRegex = /background:\s*linear-gradient\(to right,\s*#[0-9a-fA-F]{6},\s*#[0-9a-fA-F]{6}\)/;
    if (progressRegex.test(content)) {
      content = content.replace(progressRegex, `background: ${theme.progressGrad}`);
      changes.push('progress-bar');
    }

    // 4. Update body class background gradient
    const bodyClassRegex = /class="bg-gradient-to-br from-gray-50 to-\w+-50 text-gray-800"/;
    if (bodyClassRegex.test(content)) {
      content = content.replace(bodyClassRegex, `class="${theme.bodyClass}"`);
      changes.push('body-bg');
    }

    // 5. Update hero section gradient (from-primary via-COLOR-600 to-secondary)
    const heroRegex = /from-primary via-\w+-600 to-secondary/g;
    if (heroRegex.test(content)) {
      content = content.replace(/from-primary via-\w+-600 to-secondary/g, theme.heroFrom);
      changes.push('hero');
    }

    if (changes.length > 0) {
      writeFileSync(filePath, content, 'utf-8');
      console.log(`  [OK] ${file} — ${changes.join(', ')}`);
    } else {
      console.log(`  [SKIP] ${file}`);
    }
  }
}

console.log('\n✅ Theme colors updated!');
