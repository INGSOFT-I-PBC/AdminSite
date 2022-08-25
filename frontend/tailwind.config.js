/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
const defaultTheme = require('tailwindcss/defaultTheme')
// eslint-disable-next-line no-undef
module.exports = {
    prefix: 'tw-',
    content: ['./src/index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: colors.yellow[300],
                    light: '#FFC107',
                    dark: colors.yellow[400],
                    night: {
                        DEFAULT: colors.yellow[500],
                        dark: colors.yellow[600],
                    },
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
                    // DEFAULT: '#455A64',
                    DEFAULT: colors.gray[900],
                    light: colors.gray[700],
                    dark: '#263238',
                    night: {
                        DEFAULT: colors.gray[700],
                        dark: colors.gray[800],
                        light: colors.gray[600],
                    },
                },
            },
            fontFamily: {
                'inria-sans': ['Inria Sans'],
                inter: ['Inter'],
                silkscreen: [],
            },
            fontSize: {
                tiny: '.75rem',
                smd: '.89rem',
                md: '.935rem',
                medium: '.895rem',
            },
        },
        screens: {
            sm: '576px',
            md: '768px',
            lg: '992px',
            xl: '1200px',
            '2xl': '1400px',
            '3xl': '1600px',
        },
        fontFamily: {
            sans: ['Inria Sans', ...defaultTheme.fontFamily.sans],
            serif: [...defaultTheme.fontFamily.serif],
            mono: [...defaultTheme.fontFamily.mono],
        },
    },
    plugins: [],
}
