/** @type {import('tailwindcss').Config} */
module.exports = {
    mode: 'jit',
    content: [
      './{{cookiecutter.project_slug}}/templates/*.html', './{{cookiecutter.project_slug}}/templates/**/*.html'
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require("@tailwindcss/forms"),
      require("@tailwindcss/typography", require("@tailwindcss/line-clamp")),
    ],
  }
  