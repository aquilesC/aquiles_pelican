/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './themes/aquiles_theme/templates/**/*.html',
    './content/**/*.md',
    './pelicanconf.py',
  ],
  theme: {
    extend: {
      colors: {
        // Design brief palette
        background: '#FFFFFF',
        'text-primary': '#111111',
        'text-secondary': '#4A4A4A',
        accent: '#1E88E5',
        'accent-alt': '#0D47A1',
        'muted-bg': '#F5F7FA',
        border: '#E6E9EF',
        status: {
          info: '#1E88E5',
          success: '#2E7D32',
          warning: '#ED6C02',
        },
      },
      fontSize: {
        // Typography scale from design brief
        h1: ['40px', { lineHeight: '1.2', fontWeight: '700' }],
        h2: ['32px', { lineHeight: '1.2', fontWeight: '700' }],
        h3: ['26px', { lineHeight: '1.2', fontWeight: '700' }],
        h4: ['22px', { lineHeight: '1.2', fontWeight: '700' }],
        body: ['18px', { lineHeight: '1.6', fontWeight: '400' }],
        small: ['16px', { lineHeight: '1.6', fontWeight: '400' }],
        overline: ['12px', { lineHeight: '1.4', fontWeight: '400' }],
      },
      maxWidth: {
        'content': '1200px',
        'reading': '72ch', // Max line length for articles
      },
      spacing: {
        // Spacing scale from design brief
        'xxs': '4px',
        'xs': '8px',
        'sm': '12px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        'xxl': '48px',
      },
      screens: {
        // Breakpoints from design brief
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
      },
      fontFamily: {
        heading: ['serif', 'Georgia', 'serif'], // Serif or humanist sans
        body: ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'], // Neutral sans
      },
    },
  },
  plugins: [],
}

