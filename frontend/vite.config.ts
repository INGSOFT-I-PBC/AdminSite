import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import path, { resolve } from 'node:path'
import { URL, fileURLToPath } from 'node:url'
import { defineConfig, loadEnv } from 'vite'

// https://vitejs.dev/config/
export default ({ mode }: { mode: string }) => {
    process.env = {
        ...process.env,
        ...loadEnv(mode, '../'),
    }
    return defineConfig({
        root: './src/',
        envDir: '../',
        build: {
            manifest: true,
            assetsDir: '',
            emptyOutDir: true,
            minify: 'esbuild',
            outDir: resolve('../static/dist'),
            rollupOptions: {
                input: {
                    main: resolve('./src/main.ts'),
                    style: resolve('./src/assets/main.css'),
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
                '@components': fileURLToPath(
                    new URL('./src/components', import.meta.url)
                ),
                '@views': fileURLToPath(
                    new URL('./src/views', import.meta.url)
                ),
                '@store': fileURLToPath(
                    new URL('./src/store', import.meta.url)
                ),
                '@store-types': fileURLToPath(
                    new URL('./src/store/types', import.meta.url)
                ),
                '@component-types': fileURLToPath(
                    new URL('./src/components/types', import.meta.url)
                ),
                '@custom-components': fileURLToPath(
                    new URL('./src/components/index.ts', import.meta.url)
                ),
                '@': fileURLToPath(new URL('./src', import.meta.url)),
                '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
            },
        },
    })
}
