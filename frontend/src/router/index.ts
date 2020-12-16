import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { StepPageNames } from '../models/enum'
import Home from '../views/Home.vue'
import PStart from '../views/Start.vue'
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
    path: '/start',
    name: StepPageNames.Start,
    component: PStart
  },
  {
    path: '/frame',
    name: StepPageNames.Frame,
    component: PFrame
  },
  {
    path: '/subtitle',
    name: StepPageNames.Subtitle,
    component: PSubtitle
  },
  {
    path: '/style',
    name: StepPageNames.Style,
    component: PStyle
  },
  {
    path: '/comic',
    name: StepPageNames.Comic,
    component: PComic
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
