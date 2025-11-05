import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import ListTask from './components/ListTask.vue'

const app = createApp(App)
app.component('list-task', ListTask)
app.mount('#app')