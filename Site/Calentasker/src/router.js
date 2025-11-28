import { createRouter, createWebHistory } from "vue-router";
import TasksPage from "./pages/TasksPage.vue";
import AuthPage from "./pages/AuthPage.vue";

const routes = [
    {path: '/', component: TasksPage},
    {path: '/auth', component: AuthPage},
]

export default createRouter({
    history: createWebHistory(),
    routes,
})