import { createRouter, createWebHistory } from "vue-router";
import TasksPage from "./pages/TasksPage.vue";
import AuthPage from "./pages/AuthPage.vue";
import ProfilePage from "./pages/ProfilePage.vue";

const routes = [
    {path: '/', component: TasksPage},
    {path: '/auth', component: AuthPage},
    {path: '/profile', component: ProfilePage}
]

export default createRouter({
    history: createWebHistory(),
    routes,
})