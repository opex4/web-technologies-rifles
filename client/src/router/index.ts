import { createRouter, createWebHistory } from 'vue-router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { ref } from 'vue';
import { useUserInfoStore } from "@/stores/user_info_store.ts"; 

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
    },
    {
      path: '/types_of_mounts',
      name: 'TypesOfMountsView',
      component: () => import('@/views/TypesOfMountsView.vue')
    },
    {
      path: '/attachments',
      name: 'AttachmentsView',
      component: () => import('@/views/AttachmentsView.vue')
    },
    {
      path: '/loadouts',
      name: 'LoadoutsView',
      component: () => import('@/views/LoadoutsView.vue')
    },
    {
      path: '/login',
      name: 'LoginView',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/user',
      name: 'UserView',
      component: () => import('@/views/UserView.vue')
    },
  ],
})

router.beforeEach(async (to, from) => {
  const userInfoStore = useUserInfoStore();
  await userInfoStore.fetchUserInfo();
  if (!userInfoStore.isAuth && to.name != 'LoginView'){
    return { name: 'LoginView' }
  }
})

export default router
