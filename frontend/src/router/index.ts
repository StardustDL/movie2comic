import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { StepPageNames } from '../models/enum'
import Home from '../views/Home.vue'
import PCreate from '../views/Create.vue'
import PFrame from '../views/Frame.vue'
import PSubtitle from '../views/Subtitle.vue'
import PStyle from '../views/Style.vue'
import PComic from '../views/Comic.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Start',
    name: StepPageNames.Start,
    component: PCreate
  },
  {
    path: '/Frame',
    name: StepPageNames.Frame,
    component: PFrame
  },
  {
    path: '/Subtitle',
    name: StepPageNames.Subtitle,
    component: PSubtitle
  },
  {
    path: '/Style',
    name: StepPageNames.Style,
    component: PStyle
  },
  {
    path: '/Comic',
    name: StepPageNames.Comic,
    component: PComic
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
