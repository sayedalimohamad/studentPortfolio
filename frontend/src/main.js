import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import router from './router';
import axios from './axios'; // Import the custom Axios instance

const app = createApp(App);

// Add the custom Axios instance to the Vue prototype
app.config.globalProperties.$axios = axios;

app
  .use(vuetify)
  .use(router)
  .mount('#app');