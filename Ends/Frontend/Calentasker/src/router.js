import { createRouter, createWebHistory } from "vue-router";
import TasksPage from "./pages/TasksPage.vue";
import AuthPage from "./pages/AuthPage.vue";
import ProfilePage from "./pages/ProfilePage.vue";

const routes = [
    {
        path: '/', 
        name: 'Tasks',
        component: TasksPage,
        meta: { title: 'My Tasks' }
    },
    {
        path: '/auth', 
        name: 'Auth',
        component: AuthPage,
        meta: { title: 'Login' } // Default fallback
    },
    {
        path: '/profile', 
        name: 'Profile',
        component: ProfilePage,
        meta: { title: 'User Profile' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// --- DYNAMIC TITLE LOGIC ---
router.beforeEach((to, from, next) => {
    let pageTitle = to.meta.title || 'Calentasker';

    // 1. Special check for Auth page to distinguish Login vs Register
    if (to.name === 'Auth') {
        const mode = to.query.mode || 'login';
        // Capitalize: login -> Login
        pageTitle = mode.charAt(0).toUpperCase() + mode.slice(1);
    }

    // 2. Set the document title
    document.title = `Calentasker | ${pageTitle}`;

    next();
});

export default router;