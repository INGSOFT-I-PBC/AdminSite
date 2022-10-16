import 'vite/modulepreload-polyfill'
import { createApp, ref } from 'vue'
import { createPinia } from 'pinia'
import Toast, { type PluginOptions, POSITION } from 'vue-toastification'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { awesomeIcons } from './icons'
import VueFeather from 'vue-feather'
import ECard from './components/custom/ECard.vue'
import ECol from './components/custom/ECol.vue'
import ERow from './components/custom/ERow.vue'
import BootstrapVue3 from 'bootstrap-vue-3'
import Vue3EasyDataTable from 'vue3-easy-data-table'

import './types'

import App from './App.vue'
import router from './router'
import '@/scss/styles.scss'
import './assets/main.css'
import 'vue-toastification/dist/index.css'
import './index.css'
import 'bootstrap/dist/css/bootstrap.css'
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
app.component(VueFeather.name, VueFeather)
app.component('ECard', ECard)
app.component('ERow', ERow)
app.component('ECol', ECol)
globalThis.ref = ref
app.mount('#app')
