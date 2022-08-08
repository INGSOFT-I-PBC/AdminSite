import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { resolve } from 'node:path'

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
            minify: true,
            outDir: resolve('../static/dist'),
            rollupOptions: {
                input: {
                    main: resolve(
                        './src/main.ts'
                    ),
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
                    new URL(
                        './src',
                        import.meta.url
                    )
                ),
                '@components': fileURLToPath(
                    new URL(
                        './src/components',
                        import.meta.url
                    )
                ),
                '@views': fileURLToPath(
                    new URL(
                        './src/views',
                        import.meta.url
                    )
                ),
                '@custom-components':
                    fileURLToPath(
                        new URL(
                            './src/components/custom/index.ts',
                            import.meta.url
                        )
                    ),
            },
        },
    })
}
