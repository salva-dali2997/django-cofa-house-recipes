import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

export default defineConfig({
  base: '/static/', // This should match Django's settings.STATIC_URL
  plugins: [react(), tailwindcss()],
  build: {
    // Where Vite will save its output files.
    // This should be something in your settings.STATICFILES_DIRS
    outDir: path.resolve(__dirname, './static'),
    emptyOutDir: false, // Preserve the outDir to not clobber Django's other files.
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        'index': path.resolve(__dirname, './assets/index.jsx'),
        'tailwind': path.resolve(__dirname, './assets/main.css'),
        'create-recipe': path.resolve(__dirname, './assets/create.jsx'),
      },
      output: {
        // Output JS bundles to js/ directory with -bundle suffix
        entryFileNames: `js/[name]-bundle.js`,
        assetFileNames: `css/[name]-bundle.css`,
      },
    },
  },
});