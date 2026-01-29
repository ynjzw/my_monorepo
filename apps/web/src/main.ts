import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'
import request from './util/request'


const pinia = createPinia()

const app=createApp(App)
app.config.globalProperties.$http=axios
app.provide('$axios',request)
app.use(router)
app.use(pinia)
app.mount('#app')
