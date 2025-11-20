/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1F4788',
        secondary: '#4A90E2',
        accent: '#45B7D1',
      }
    },
  },
  plugins: [],
}
