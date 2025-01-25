import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import StudentView from './views/StudentView.vue';
import AdminView from './views/AdminView.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import ChatInterfaceView from './views/ChatInterfaceView.vue';
import UserProfileView from './views/UserProfileView.vue'; 
import AboutView from './views/AboutView.vue';
import SendEmailView from './views/SendEmailView.vue';
import InboxView from './views/InboxView.vue';
import NotFoundView from './views/NotFoundView.vue';
import EventView from './views/EventView.vue';

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
    path: '/events',
    name: 'Events',
    component: EventView,
    // meta: { requiresAuth: true },
  },
  {
    path: '/students',
    name: 'Students',
    component: StudentView,
    meta: { requiresAuth: true },  
  },
  {
    path: '/admins',
    name: 'Admins',
    component: AdminView,
    meta: { requiresAuth: true },  
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
    meta: { requiresAuth: true },  
  },
  {
    path: '/user/:role/:id',
    name: 'UserProfile',
    component: UserProfileView,
    props: true,
    meta: { requiresAuth: true },  
  },
  {
    path: '/inbox/:id',
    name: 'Inbox',
    component: InboxView,
    meta: { requiresAuth: true },
  },
  {
    path: '/send-email',
    name: 'SendEmail',
    component: SendEmailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*', 
    name: 'NotFound',
    component:NotFoundView, 
    meta: { title: 'Page Not Found' },
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); 
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' }); 
  } else {
    next(); 
  }
});
export default router;
