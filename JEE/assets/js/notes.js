/* ============================================
   JEE Prep Guide — Common Notes Page JS
   Shared across Physics, Chemistry & Maths
   ============================================ */

// ── Mobile Menu Toggle ────────────────────────
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) menu.classList.toggle('hidden');
}

// ── Scroll Handler (throttled via requestAnimationFrame) ─────
document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.sticky-nav a[href^="#"]');
    const progressBar = document.getElementById('progress-bar');

    let ticking = false;

    const updateOnScroll = () => {
        // Reading Progress Bar
        if (progressBar) {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
            progressBar.style.width = scrolled + '%';
        }

        // Active Navigation Highlighting
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

        ticking = false;
    };

    const requestTick = () => {
        if (!ticking) {
            window.requestAnimationFrame(updateOnScroll);
            ticking = true;
        }
    };

    window.addEventListener('scroll', requestTick, { passive: true });
});

// ── Print / PDF ───────────────────────────────
function printNotes() {
    window.print();
}

// ── Dark Mode Toggle (optional) ───────────────
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

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
