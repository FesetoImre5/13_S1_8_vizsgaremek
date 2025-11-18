import { createRouter, createWebHistory } from "vue-router";
import TasksPage from "./pages/TasksPage.vue";

const routes = [
    {path: '/', component: TasksPage},
]

export default createRouter({
    history: createWebHistory(),
    routes,
})