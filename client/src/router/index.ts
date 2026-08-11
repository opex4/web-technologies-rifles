import { createRouter, createWebHistory } from 'vue-router';
import 'bootstrap/dist/css/bootstrap.min.css';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "RiflesView",
      component: () => import('@/views/RiflesView.vue')
    },
    {
      path: "/countries",
      name: "CountriesView",
      component: () => import('@/views/CountriesView.vue')
    },
    {
      path: '/constructors',
      name: 'ConstructorsView',
      component: () => import('@/views/ConstructorsView.vue')
    },
    {
      path: '/ammo',
      name: 'AmmoView',
      component: () => import('@/views/AmmoView.vue')
    },
    {
      path: '/conflicts',
      name: 'ConflictsView',
      component: () => import('@/views/ConflictsView.vue')
    }
  ],
})

export default router
