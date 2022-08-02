/** @type {import('tailwindcss').Config} */
// eslint-disable-next-line no-undef
module.exports = {
    content: [
        './src/index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#F9A825',
                    light: '#FFC107',
                    dark: '#FF8F00',
                },
                on: {
                    primary: {
                        DEFAULT: '#424242',
                        soft: '',
                        hard: '',
                        highlight: '#FFD54F',
                    },
                    secondary: {
                        DEFAULT: '#E0E0E0',
                        soft: '#BDBDBD',
                        hard: '#FAFAFA',
                    },
                },
                secondary: {
                    DEFAULT: '#455A64',
                    light: '#607D8B',
                    dark: '#263238',
                },
            },
        },
    },
    plugins: [],
}
