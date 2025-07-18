// vite.config.js

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true, // автоматически откроет браузер
    proxy: {
      // Прокси на backend (опционально, но удобно при разработке)
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist', // папка, куда будет собираться production-версия
    assetsDir: 'assets', // папка для статики
    emptyOutDir: true,
  },
  preview: {
    port: 8080, // порт для preview-сервера
  },
  resolve: {
    // Можно добавить алиасы, если используешь
    // alias: {
    //   '@': path.resolve(__dirname, './src'),
    // },
  },
});