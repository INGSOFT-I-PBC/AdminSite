import 'vite/modulepreload-polyfill'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast, {
    type PluginOptions,
    POSITION,
} from 'vue-toastification'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { awesomeIcons } from './icons'

import App from './App.vue'
import router from './router'

import '@/scss/styles.scss'
import * as bootstrap from 'bootstrap'
import './assets/main.css'
import 'vue-toastification/dist/index.css'
import './index.css'

const app = createApp(App)

const defToastOptions: PluginOptions = {
    position: POSITION.TOP_RIGHT,
    closeOnClick: true,
    pauseOnHover: true,
    maxToasts: 5,
}
awesomeIcons.forEach(icon => library.add(icon))

if (!import.meta.env.VITE_BACKEND_URL)
    throw new Error('No API url was provided')

app.use(createPinia())
app.use(router)
app.use(Toast, defToastOptions)
app.component('FontAwesomeIcon', FontAwesomeIcon)

app.mount('#app')
