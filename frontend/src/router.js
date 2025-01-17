import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import StudentView from './views/StudentView.vue';
import AdminView from './views/AdminView.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import ChatInterfaceView from './views/ChatInterfaceView.vue';
import UserProfileView from './views/UserProfileView.vue'; 
import AboutView from './views/AboutView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView,
  },
  {
    path: '/students',
    name: 'Students',
    component: StudentView,
    meta: { requiresAuth: true },  // This route requires authentication
  },
  {
    path: '/admins',
    name: 'Admins',
    component: AdminView,
    meta: { requiresAuth: true },  // This route requires authentication
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatInterfaceView,
    meta: { requiresAuth: true },  // This route requires authentication
  },
  {
    path: '/user/:role/:id',
    name: 'UserProfile',
    component: UserProfileView,
    props: true,
    meta: { requiresAuth: true },  // This route requires authentication
  },
  {
    path: '/:pathMatch(.*)*', // Catch-all route for 404 errors
    name: 'NotFound',
    component: () => import('./views/NotFoundView.vue'), // Lazy load the 404 component
    meta: { title: 'Page Not Found' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Add a global navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // Check if the user is authenticated (e.g., via token)

  // If the route requires authentication and the user is not authenticated, redirect to login
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' }); // Redirect to login page
  } else {
    next(); // Proceed to the requested route
  }
});

export default router;
