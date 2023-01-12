import { library } from '@fortawesome/fontawesome-svg-core'
import BootstrapVue3 from 'bootstrap-vue-3'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import 'vite/modulepreload-polyfill'

import { computed, createApp, defineAsyncComponent, ref } from 'vue'
import Vue3EasyDataTable from 'vue3-easy-data-table'
import 'vue3-easy-data-table/dist/style.css'
import OpenLayersMap from 'vue3-openlayers'
import 'vue3-openlayers/dist/vue3-openlayers.css'
import Toast, { POSITION, type PluginOptions } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import '@/scss/styles.scss'
import '@vuepic/vue-datepicker/dist/main.css'

import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import 'bootstrap/dist/css/bootstrap.css'

import '../scss/datepicker-theme.scss'
import './assets/main.css'
import './index.css'
import './scss/styles.scss'

import { awesomeIcons } from './icons'
import router from './router'
import './types'

const app = createApp(defineAsyncComponent(() => import('./App.vue')))

const defToastOptions: PluginOptions = {
    position: POSITION.TOP_RIGHT,
    closeOnClick: true,
    pauseOnHover: true,
    maxToasts: 5,
    shareAppContext: true,
}
awesomeIcons.forEach(icon => library.add(icon))

if (!import.meta.env.VITE_BACKEND_URL) {
    throw new Error('No API url was provided')
}

app.use(createPinia())
app.use(BootstrapVue3)
app.use(router)
app.use(Toast, defToastOptions)
app.use(PrimeVue)
app.use(OpenLayersMap)
app.component('EasyDataTable', Vue3EasyDataTable)
app.component(
    'FontAwesomeIcon',
    defineAsyncComponent(() =>
        import('@fortawesome/vue-fontawesome').then(m => m.FontAwesomeIcon)
    )
)
app.component(
    'FontAwesomeLayers',
    defineAsyncComponent(() =>
        import('@fortawesome/vue-fontawesome').then(m => m.FontAwesomeLayers)
    )
)
app.component(
    'FontAwesomeLayersText',
    defineAsyncComponent(() =>
        import('@fortawesome/vue-fontawesome').then(
            m => m.FontAwesomeLayersText
        )
    )
)
app.component(
    'VeeForm',
    defineAsyncComponent(() =>
        import('vee-validate').then(module => module.Form)
    )
)
app.component(
    'VeeField',
    defineAsyncComponent(() =>
        import('vee-validate').then(module => module.Field)
    )
)
app.component(
    'VeeFieldArray',
    defineAsyncComponent(() =>
        import('vee-validate').then(module => module.FieldArray)
    )
)
app.component(
    'VueFeather',
    defineAsyncComponent(() => import('vue-feather'))
)

globalThis.ref = ref
globalThis.computed = computed
globalThis.undef = (value?: any): value is undefined => value == undefined
globalThis.defined = function <T = any>(value?: T): value is T {
    return value != undefined
}

app.mount('#app')
