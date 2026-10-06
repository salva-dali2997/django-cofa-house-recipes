import { defineConfig, globalIgnores } from "eslint/config";
import reactRefresh from 'eslint-plugin-react-refresh'
import react from 'eslint-plugin-react';
import globals from 'globals';
import js from '@eslint/js'

export default defineConfig([
  js.configs.recommended,
  react.configs.flat.recommended,
  react.configs.flat['jsx-runtime'],
  reactRefresh.configs.vite,
  globalIgnores(['.venv/', 'static/', 'htmlcov/']),
  {
    files: ['**/*.{js,jsx,mjs,cjs,ts,tsx}'],
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      'react/prop-types': 'off',
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
  {
    files: ['eslint.config.js', 'vite.config.js',],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
  }
]);