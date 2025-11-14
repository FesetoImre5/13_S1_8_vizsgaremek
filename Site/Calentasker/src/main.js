import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import ListTask from './components/ListTask.vue'
import ListGroup from './components/ListGroup.vue'

const app = createApp(App)
app.component('list-task', ListTask)
app.component('list-group', ListGroup)
app.mount('#app')