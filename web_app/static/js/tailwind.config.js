/** @type {import('tailwindcss').Config} */

module.exports = {
    content: ["./*.html"],
    theme: {
        screens : {
            'sm': '640px', 
            'md': '768px',
            'lg': '1024px', 
            'xl': '2080px',
            '2xl': '1536px',
        },
        extend: {},
    },
    plugins: [
        require('tailwindcss'),
        require('@tailwindcss/forms')
    ]
}