import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
  },
  {
    path: '/:items/:id',
    name: 'Items',
    component: () => import(/* webpackChunkName: "items" */ '../views/Items.vue'),
    props: true,
  },
  {
    path: '/:items/:option/:id',
    name: 'Forms',
    component: () => import(/* webpackChunkName: "forms" */ '../views/Forms.vue'),
  },
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
