/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#0A1128",     // Deep navy
          secondary: "#1E293B",   // Deep charcoal / slate
          accent: "#0284C7",      // Restrained professional blue/teal
          accentHover: "#0369A1", // Darker blue on hover
          accentLight: "#E0F2FE", // Soft accent tint for badges/tags
          muted: "#64748B",       // Slate gray for secondary text
          surface: "#F8FAFC",     // Very light slate for section backgrounds
          card: "#FFFFFF",        // White for cards
          border: "#E2E8F0",      // Light border
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Oxygen",
          "Ubuntu",
          "Cantarell",
          "Fira Sans",
          "Droid Sans",
          "Helvetica Neue",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};
