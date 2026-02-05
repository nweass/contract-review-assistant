import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue')
  },
  {
    path: '/review',
    name: 'Review',
    component: () => import('@/pages/Review.vue')
  },
  {
    path: '/batch',
    name: 'BatchReview',
    component: () => import('@/pages/BatchReview.vue')
  },
  {
    path: '/rules',
    name: 'Rules',
    component: () => import('@/pages/Rules.vue')
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/pages/History.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
