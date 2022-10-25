import 'vite/modulepreload-polyfill'
import { createApp, ref } from 'vue'
import { createPinia } from 'pinia'
import Toast, { type PluginOptions, POSITION } from 'vue-toastification'
import { library } from '@fortawesome/fontawesome-svg-core'
import { awesomeIcons } from './icons'
import VueFeather from 'vue-feather'
import {
    FontAwesomeIcon,
    FontAwesomeLayers,
    FontAwesomeLayersText,
} from '@fortawesome/vue-fontawesome'
import BootstrapVue3 from 'bootstrap-vue-3'
import Vue3EasyDataTable from 'vue3-easy-data-table'

import './types'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import '@/scss/styles.scss'
import './assets/main.css'
import 'vue-toastification/dist/index.css'
import './index.css'
import 'vue3-easy-data-table/dist/style.css'

const app = createApp(App)

const defToastOptions: PluginOptions = {
    position: POSITION.TOP_RIGHT,
    closeOnClick: true,
    pauseOnHover: true,
    maxToasts: 5,
    shareAppContext: true,
}
awesomeIcons.forEach(icon => library.add(icon))

if (!import.meta.env.VITE_BACKEND_URL)
    throw new Error('No API url was provided')

app.use(createPinia())
app.use(BootstrapVue3)
app.use(router)
app.use(Toast, defToastOptions)
app.component('EasyDataTable', Vue3EasyDataTable)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.component('FontAwesomeLayers', FontAwesomeLayers)
app.component('FontAwesomeLayersText', FontAwesomeLayersText)
app.component(VueFeather.name, VueFeather)
globalThis.ref = ref
app.mount('#app')
