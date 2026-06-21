import { createRouter, createWebHashHistory } from 'vue-router'
import home from '../views/home.vue'
import show_diff_structure from '../views/show_diff_structure.vue'
import person from '../views/person/person.vue'
import world from '../views/world/world.vue'
import nation from '../views/nation.vue'
import internation from '../views/internation.vue'
import UploadPage from '../views/UploadPage.vue'
import father from '../views/father.vue'
import internet from '../views/world/internet.vue'
import main from '../views/main.vue'
import circle from '../views/circle.vue'
import timeline from '../components/timeline.vue'
import timeaxis from '../components/timeaxis.vue'
import brain from '../views/person/brain.vue'
import skill_resource_wish from '../views/skill_resource_wish.vue'
import stock_sector from '../views/stock_sector.vue'
import ttt from '../views/ttt.vue'
import 地球 from '@/views/world/地球.vue'
import China from '../views/world/China.vue'
import dynamic_graph from '../views/dynamic_graph.vue'
import hundreds_dots from '../views/hundreds_dots.vue'
import vue_liveCycle from '../views/vue_liveCycle.vue'
import use_circle from '../views/use_circle.vue'
// 定义路由表
const routes = [
  {name: 'home', path: '/', component: home},
  {name: 'show_diff_structure',path: '/show_diff_structure',component: show_diff_structure},
  {
    name: 'person',
    path: '/person',
    component: person
  },
  {name: 'brain',path: '/brain',component: brain},
  {
    name: 'world',
    path: '/world',
    component: world,
    children: [
      {name: 'hundreds_dots',path: 'hundreds_dots',component: ()=>import('../views/hundreds_dots.vue')}
    ]
  },
  {name: 'China',path: '/China',component: China,children: [
      {name: 'hundreds_dots',path: 'hundreds_dots',component: ()=>import('../views/hundreds_dots.vue')}
    ]},
  {name: 'internation',path: '/internation',component: internation},
  {name: '地球',path: '/地球',component: 地球},
  {name: 'nation',path: '/nation',component: nation},
  {name: 'uploadpage',path:'/uploadpage',component:UploadPage},
  {name: 'father',path:'/father',component:father},
  {name: 'internet',path:'/internet',component:internet},
  {name: 'main',path:'/main',component:main},
  {name: 'circle',path:'/circle',component:circle},
  {name: 'ttt',path:'/ttt',component:ttt},
  {name: 'hundreds_dots',path: '/hundreds_dots',component: hundreds_dots},
  {name: 'skill_resource_wish', path: '/world/skill_resource_wish', component: skill_resource_wish},
  {name: 'stock_sector', path: '/stock_sector', component: stock_sector},
  {name: 'dynamic_graph', path: '/dynamic_graph', component: dynamic_graph},
  {name: 'use_circle', path: '/use_circle', component: use_circle},
  {name: 'vue_liveCycle', path: '/vue_liveCycle', component: vue_liveCycle}
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes //路由表
})

export default router
