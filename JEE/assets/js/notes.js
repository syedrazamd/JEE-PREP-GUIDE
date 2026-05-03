/* ============================================
   JEE Prep Guide — Common Notes Page JS
   Shared across Physics, Chemistry & Maths
   ============================================ */

// ── Reading Progress Bar ──────────────────────
window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    const bar = document.getElementById('progress-bar');
    if (bar) bar.style.width = scrolled + '%';
});

// ── Active Navigation Highlighting ────────────
document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.sticky-nav a[href^="#"]');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 150) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('bg-primary', 'text-white');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('bg-primary', 'text-white');
            }
        });
    });
});

// ── Print / PDF ───────────────────────────────
function printNotes() {
    window.print();
}

// ── Dark Mode Toggle (optional) ───────────────
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

// ── MathJax Configuration ─────────────────────
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

// ── Lazy-Load Images ──────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    const images = document.querySelectorAll('img[loading="lazy"]');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    observer.unobserve(img);
                }
            });
        });
        images.forEach(img => observer.observe(img));
    }
});

// ── Copy Formula to Clipboard ─────────────────
function copyFormula(formula) {
    navigator.clipboard.writeText(formula).then(() => {
        alert('Formula copied to clipboard!');
    });
}

// ── Reading Time Estimation ───────────────────
function calculateReadingTime() {
    const text = document.body.innerText;
    const wordCount = text.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200);
    console.log(`Estimated reading time: ${readingTime} minutes`);
}
calculateReadingTime();
