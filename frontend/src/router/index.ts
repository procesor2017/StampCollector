import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import EmissionPage from '../views/EmissionsPage.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/emissions',
    name: 'Emissions',
    component: EmissionPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
