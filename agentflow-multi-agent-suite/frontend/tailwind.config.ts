import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0a0a0b',
        surface: '#101012',
        border: '#1f1f23',
        foreground: '#f4f4f5',
        muted: '#a1a1aa',
        accent: '#a78bfa',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.25rem',
      },
      boxShadow: {
        'glow': '0 0 0 1px rgba(167,139,250,0.25), 0 10px 60px -20px rgba(167,139,250,0.4)',
      }
    },
  },
  plugins: [],
} satisfies Config
