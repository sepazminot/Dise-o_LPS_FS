import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
  plugins: [
    laravel({
      input: ['src/main.js'],
      publicDir: 'public',
    }),
  ],
  build: {
    outDir: 'public/build',
    emptyOutDir: true,
  },
});