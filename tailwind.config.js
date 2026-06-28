module.exports = {
  content: [
    "./**/*.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        primary: 'var(--color-primary)',
        'primary-hover': 'var(--color-primary-hover)',
        'primary-focus': 'var(--color-primary-focus)',
        secondary: 'var(--color-secondary)',
        canvas: 'var(--color-canvas)',
        'surface-1': 'var(--color-surface-1)',
        'surface-2': 'var(--color-surface-2)',
        'surface-3': 'var(--color-surface-3)',
        'surface-4': 'var(--color-surface-4)',
        hairline: 'var(--color-hairline)',
        'hairline-strong': 'var(--color-hairline-strong)',
        'hairline-tertiary': 'var(--color-hairline-tertiary)',
        ink: 'var(--color-ink)',
        'ink-muted': 'var(--color-ink-muted)',
        'ink-subtle': 'var(--color-ink-subtle)',
        'ink-tertiary': 'var(--color-ink-tertiary)',
        accent: '#f59e0b',
        success: '#10b981',
        danger: '#ef4444',
      }
    }
  },
  plugins: [],
}