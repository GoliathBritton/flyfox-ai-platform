import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'flyfox': {
          primary: '#FF6B35',
          secondary: '#2C3E50',
          accent: '#E74C3C',
        }
      }
    },
  },
  plugins: [],
} satisfies Config
