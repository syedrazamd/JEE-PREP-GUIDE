#!/usr/bin/env python3
"""Throttle scroll listeners in JEE/assets/js/notes.js by combining them
into a single requestAnimationFrame-throttled handler."""

from pathlib import Path

JS_FILE = Path("JEE/assets/js/notes.js")

OLD_BLOCK = """// ── Reading Progress Bar ──────────────────────
window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    const bar = document.getElementById('progress-bar');
    if (bar) bar.style.width = scrolled + '%';
});

// ── Mobile Menu Toggle ────────────────────────
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) menu.classList.toggle('hidden');
}

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
"""

NEW_BLOCK = """// ── Mobile Menu Toggle ────────────────────────
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
"""


def main() -> None:
    content = JS_FILE.read_text(encoding="utf-8")
    if OLD_BLOCK not in content:
        raise SystemExit("OLD_BLOCK not found - file may already be updated or has changed.")

    new_content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
    if new_content.count("addEventListener('scroll'") != 1:
        raise SystemExit("Replacement would leave more than one scroll listener.")

    JS_FILE.write_text(new_content, encoding="utf-8")
    print("notes.js updated successfully.")


if __name__ == "__main__":
    main()
