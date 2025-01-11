const plugin = require('tailwindcss/plugin');

module.exports = {
  corePlugins: {
    preflight: false,  //manually import this in app.css
  },
  content: [
    './{{cookiecutter.repo_name}}/static_source/**/*.html',
    './{{cookiecutter.repo_name}}/static_source/**/*.js',
    './{{cookiecutter.repo_name}}/static_source/**/*.scss',
    './{{cookiecutter.repo_name}}/static_source/**/*.sass',
    './{{cookiecutter.repo_name}}/templates/**/*.html',
    './{{cookiecutter.repo_name}}/components/**/*.html',
    './{{cookiecutter.repo_name}}/components/**/*.svg',
    './{{cookiecutter.repo_name}}/components/**/*.py',

  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "var(--primary)",
          focus: 'var(--primary-focus)',
          content: 'var(--primary-content)'
        },
        secondary: {
          DEFAULT: 'var(--secondary)',
          focus: 'var(--secondary-focus)',
          content: 'var(--secondary-content)'
        },
        accent: {
          DEFAULT: 'var(--accent)',
          'focus': 'var(--accent-focus)',
          'content': 'var(--accent-content)'
        },
        neutral: {
          '100': '#F3F6FA',
          '200': '#E5E7EB',
          '300': '#D1D5DB',
          '400': '#9CA3AF',
          '500': '#6B7280',
          '600': '#4B5563',
          '700': '#374151',
          '800': '#1F2937',
          '900': '#111827',
        },
        debug: {
          DEFAULT: 'var(--info)',
          'focus': 'var(--info-focus)',
          'content': 'var(--info-content)'
        },
        info: {
          DEFAULT: 'var(--info)',
          'focus': 'var(--info-focus)',
          'content': 'var(--info-content)'
        },
        success: {
          DEFAULT: 'var(--success)',
          'focus': 'var(--success-focus)',
          'content':'var(--success-content)',
        },
        warning: {
          DEFAULT: 'var(--warning)',
          'focus': 'var(--warning-focus)',
          'content': 'var(--warning-content)'
        },
        error: {
          DEFAULT: 'var(--error)',
          'focus': 'var(--error-focus)',
          'content': 'var(--error-content)'
        },
      }
    },
  },
  plugins: [
    plugin(function({ addVariant }) {
      // https://www.crocodile.dev/blog/css-transitions-with-tailwind-and-htmx
      addVariant('htmx-settling', ['&.htmx-settling', '.htmx-settling &']);
      addVariant('htmx-request',  ['&.htmx-request',  '.htmx-request &']);
      addVariant('htmx-swapping', ['&.htmx-swapping', '.htmx-swapping &']);
      addVariant('htmx-added',    ['&.htmx-added',    '.htmx-added &']);
    }),
    require('@tailwindcss/forms'),
  ],
}
