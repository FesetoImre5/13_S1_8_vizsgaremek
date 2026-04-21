import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import router from './router'
import i18n from './i18n'

// Vite proxy handles the routing securely now, so no base URL is needed!

const app = createApp(App)
app.use(router)
app.use(i18n)
app.mount('#app')
