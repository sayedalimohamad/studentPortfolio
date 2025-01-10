import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import StudentView from './views/StudentView.vue';
import AdminView from './views/AdminView.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import ChatInterfaceView from './views/ChatInterfaceView.vue';
import UserProfileView from './views/UserProfileView.vue'; // Import the new UserProfileView

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/students',
    name: 'Students',
    component: StudentView,
  },
  {
    path: '/admins',
    name: 'Admins',
    component: AdminView,
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
  },
  {
    path: '/user/:role/:id', // Dynamic route for user profiles
    name: 'UserProfile',
    component: UserProfileView,
    props: true, // Pass route params as props
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;