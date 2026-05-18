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
import timeline from '../components/timeline.vue'
import timeaxis from '../components/timeaxis.vue'
import brain from '../views/brain.vue'
import 地球 from '../views/地球.vue'
import skill_resource_wish from '../views/skill_resource_wish.vue'
import stock_sector from '../views/stock_sector.vue'
import ttt from '../views/ttt.vue'
import China from '../views/China.vue'
import dynamic_graph from '../views/dynamic_graph.vue'
import hundreds_dots from '../views/hundreds_dots.vue'
// 定义路由表
const routes = [
  {name: 'home', path: '/', component: home},
  {name: '地球',path: '/地球',component: 地球},
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
  {name: 'brain',path:'/brain',component:brain},
  {name: 'ttt',path:'/ttt',component:ttt},
  {name: 'skill_resource_wish', path: '/skill_resource_wish', component: skill_resource_wish},
  {name: 'stock_sector', path: '/stock_sector', component: stock_sector},
  {name: 'China', path: '/China', component: China},
  {name: 'dynamic_graph', path: '/dynamic_graph', component: dynamic_graph},
  {name: 'hundreds_dots', path: '/hundreds_dots', component: hundreds_dots}
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes //路由表
})

export default router
