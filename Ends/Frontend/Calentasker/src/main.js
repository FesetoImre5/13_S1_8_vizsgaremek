import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import router from './router'
import i18n from './i18n'

// Set the base URL dynamically based on where the app is loaded from
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  axios.defaults.baseURL = 'http://127.0.0.1:8000'
} else {
  // If loaded from anywhere else (like the school server), point to the public IP
  axios.defaults.baseURL = 'http://172.16.130.8:8000'
}

const app = createApp(App)
app.use(router)
app.use(i18n)
app.mount('#app')
