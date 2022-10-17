/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
    colors: {
      primary: "#1665F5",
      secondary: "#E1E9F2",
      black: "#000000",
      white: "#FFFFFF",
      grey: "#DDDDDD",
    },
    fontSize: {
      subtitle1: ["1.25rem", { fontWeight: 600 }],
      subtitle2: ["1rem", { fontWeight: 600 }],
      body1: ["1rem", { fontWeight: 400 }],
      body2: ["0.75rem", { fontWeight: 500 }],
    },
    fontFamily: {
      general: ["Inter", "serif"],
    },
  },
  plugins: [],
};
