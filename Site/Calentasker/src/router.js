import { createRouter, createWebHistory } from "vue-router";
import TasksPage from "./pages/TasksPage.vue";
import LoginPage from "./pages/LoginPage.vue";
import RegisterPage from "./pages/RegisterPage.vue";

const routes = [
    {path: '/', component: TasksPage},
    {path: '/login', component: LoginPage},
    {path: '/register', component: RegisterPage},
]

export default createRouter({
    history: createWebHistory(),
    routes,
})