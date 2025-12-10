import { resolve } from 'path'
import { defineConfig } from 'vite';

export default defineConfig({
  base: '',
  build: {
    rollupOptions: {
      input: {
        layout: resolve(__dirname, 'dist/resources', 'css', 'app.scss'),
        submit: resolve(__dirname, 'dist/resources', 'js', 'submit.js'),
      },
    },
    outDir: '',
    assetsDir: 'static/assets',
    manifest: 'static/assets/manifest.json',
    emptyOutDir: false,
  },
})
