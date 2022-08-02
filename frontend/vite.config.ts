import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { resolve } from 'node:path'

// https://vitejs.dev/config/
export default defineConfig({
    root: './src/',
    build: {
        manifest: true,
        assetsDir: '',
        emptyOutDir: true,
        minify: true,
        outDir: resolve('../static/dist'),
        rollupOptions: {
            input: {
                main: resolve('./src/main.ts'),
                style: resolve(
                    './src/assets/main.css'
                ),
            },
            output: {
                chunkFileNames: undefined,
            },
        },
    },
    base: '/static/',
    publicDir: './public',
    server: {
        host: 'localhost',
        port: 5173,
        open: false,
    },
    plugins: [vue(), vueJsx()],
    resolve: {
        alias: {
            '@': fileURLToPath(
                new URL('./src', import.meta.url)
            ),
            '@components': fileURLToPath(
                new URL(
                    './src/components',
                    import.meta.url
                )
            ),
        },
    },
})
