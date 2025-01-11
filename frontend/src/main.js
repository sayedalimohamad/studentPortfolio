import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; 
import router from './router';
import axios from './axios'; 
import Toast from 'vue-toastification'; 
import 'vue-toastification/dist/index.css'; 

const app = createApp(App);


app.config.globalProperties.$axios = axios;


app.use(Toast, {
  timeout: 3000, 
  position: 'top-right', 
});

app
  .use(vuetify)
  .use(router)
  .mount('#app');