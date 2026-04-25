import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  plugins: [],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './resources'),
    },
  },
  server: {
    port: 5173,
    host: 'localhost',
  },
  build: {
    outDir: 'public/dist',
    assetsDir: '',
    emptyOutDir: true,
  },
});
