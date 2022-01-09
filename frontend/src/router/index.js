import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
  },
  {
    path: '/authors/',
    name: 'Authors',
    component: () => import(/* webpackChunkName: "authors" */ '../views/Authors.vue')
  },
  {
    path: '/categories/',
    name: 'Categories',
    component: () => import(/* webpackChunkName: "categories" */ '../views/Categories.vue')
  },
  {
    path: '/series/',
    name: 'Series',
    component: () => import(/* webpackChunkName: "series" */ '../views/Series.vue')
  },
  {
    path: '/books/',
    name: 'Books',
    component: () => import(/* webpackChunkName: "books" */ '../views/Books.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
