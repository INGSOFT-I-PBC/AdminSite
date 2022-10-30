import { library } from '@fortawesome/fontawesome-svg-core'
import {
    FontAwesomeIcon,
    FontAwesomeLayers,
    FontAwesomeLayersText,
} from '@fortawesome/vue-fontawesome'
import BootstrapVue3 from 'bootstrap-vue-3'
import { createPinia } from 'pinia'
import { Field, FieldArray, Form } from 'vee-validate'
import 'vite/modulepreload-polyfill'
import { createApp, ref } from 'vue'
import VueFeather from 'vue-feather'
import Toast, { POSITION, type PluginOptions } from 'vue-toastification'
import Vue3EasyDataTable from 'vue3-easy-data-table'
import OpenLayersMap from 'vue3-openlayers'
import { awesomeIcons } from './icons'

import './types'

import App from './App.vue'
import router from './router'

import '@/scss/styles.scss'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'vue-toastification/dist/index.css'
import 'vue3-easy-data-table/dist/style.css'
import 'vue3-openlayers/dist/vue3-openlayers.css'
import './assets/main.css'
import './index.css'

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
app.use(OpenLayersMap)
app.component('EasyDataTable', Vue3EasyDataTable)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.component('FontAwesomeLayers', FontAwesomeLayers)
app.component('FontAwesomeLayersText', FontAwesomeLayersText)
app.component('VeeForm', Form)
app.component('VeeField', Field)
app.component('VeeFieldArray', FieldArray)
app.component(VueFeather.name, VueFeather)
globalThis.ref = ref
app.mount('#app')
