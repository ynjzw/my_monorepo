import { createRouter, createWebHashHistory } from 'vue-router'
import home from '../views/home.vue'
import test from '../views/test.vue'
import person from '../views/person.vue'
import world from '../views/world.vue'
import nation from '../views/nation.vue'
import internation from '../views/internation.vue'
import UploadPage from '../views/UploadPage.vue'
import father from '../views/father.vue'
import internet from '../views/internet.vue'
import main from '../views/main.vue'
import circle from '../views/circle.vue'
import timeline from '../views/timeline.vue'
import timeaxis from '../views/timeaxis.vue'
import skill_resource_wish from '../views/skill_resource_wish.vue'
// 定义路由表
const routes = [
  {name: 'home', path: '/', component: home},
  {name: 'test',path: '/test',component: test},
  {name: 'person',path: '/person',component: person},
  {name: 'world',path: '/world',component: world},
  {name: 'nation',path: '/nation',component: nation},
  {name: 'internation',path: '/internation',component: internation},
  {name: 'uploadpage',path:'/uploadpage',component:UploadPage},
  {name: 'father',path:'/father',component:father},
  {name: 'internet',path:'/internet',component:internet},
  {name: 'main',path:'/main',component:main},
  {name: 'circle',path:'/circle',component:circle},
  {name: 'timeline',path:'/timeline',component:timeline},
  {name: 'timeaxis',path:'/timeaxis',component:timeaxis},
  {name: 'skill_resource_wish', path: '/skill_resource_wish', component: skill_resource_wish}
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes //路由表
})

export default router
