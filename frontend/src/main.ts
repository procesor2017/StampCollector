import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importujte router
import axios, { AxiosRequestConfig, AxiosResponse  } from 'axios';
import Antd from 'ant-design-vue';

const app = createApp(App)
app.use(Antd)
.use(router).mount('#app');

// Globální konfigurace Axios
axios.defaults.baseURL = 'http://localhost:8000';