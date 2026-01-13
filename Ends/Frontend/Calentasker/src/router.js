import { createRouter, createWebHistory } from "vue-router";
import TasksPage from "./pages/TasksPage.vue";
import AuthPage from "./pages/AuthPage.vue";
import ProfilePage from "./pages/ProfilePage.vue";
// 1. Import the new page
import GroupsPage from "./pages/GroupsPage.vue";
import NotFoundPage from "./pages/NotFoundPage.vue";

const routes = [
    {
        path: '/',
        redirect: '/tasks'
    },
    {
        path: '/tasks',
        name: 'Tasks',
        component: TasksPage,
        meta: { title: 'My Tasks' }
    },
    {
        path: '/groups',
        name: 'Groups',
        component: GroupsPage,
        meta: { title: 'My Groups' }
    },
    {
        path: '/auth',
        name: 'Auth',
        component: AuthPage,
        meta: { title: 'Login' }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfilePage,
        meta: { title: 'User Profile' }
    },
    // 2. ADD THIS CATCH-ALL ROUTE AT THE END
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFoundPage,
        meta: { title: 'Page Not Found' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    let pageTitle = to.meta.title || 'Calentasker';

    if (to.name === 'Auth') {
        const mode = to.query.mode || 'login';
        pageTitle = mode.charAt(0).toUpperCase() + mode.slice(1);
    }

    document.title = `Calentasker | ${pageTitle}`;

    const isAuthenticated = localStorage.getItem('token');

    // 3. Update Guard Logic (Optional but recommended)
    // If you want 404 pages to be visible even if NOT logged in, add to.name !== 'NotFound' here.
    // Currently, if a user is NOT logged in and types a random URL, they will be redirected to Login.
    // If they ARE logged in and type a random URL, they will see the 404 page.

    if (to.name !== 'Auth' && !isAuthenticated) {
        next({ name: 'Auth' });
    }
    else if (to.name === 'Auth' && isAuthenticated) {
        next({ name: 'Tasks' });
    }
    else {
        next();
    }
});

export default router;