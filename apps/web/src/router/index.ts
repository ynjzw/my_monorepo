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
import timeline from '../components/timeline1.vue'
import brain from '../views/person/brain.vue'
import skill_resource_wish from '../views/skill_resource_wish.vue'
import stock_sector from '../views/stock_sector.vue'
import use_tree from '../views/use_tree.vue'
import use_echarts from '../views/use_echarts.vue'
import 地球 from '../views/world/地球.vue'
import China from '../views/world/China.vue'
import dynamic_graph from '../views/dynamic_graph.vue'
import hundreds_dots from '../views/hundreds_dots.vue'
import thousand_dots from '../views/thousand_dots.vue'
import billion_dots from '../views/billion_dots.vue'
import use_graph from '../views/use_graph.vue'
import use_circle from '../views/use_circle.vue'
import test from '../views/test.vue'
import testPage from '../views/testPage.vue'
import economy from '../views/world/economy.vue'
import entertainment from '../views/world/entertainment.vue'
import finance from '../views/world/finance.vue'
import atom2social from '../views/atom2social.vue'
import cash_flow from '../views/cash_flow.vue'
import maslow_needs from '../views/maslow_needs.vue'
import floors from '../views/floors.vue'
import use_timeline from '../views/use_timeline.vue'
import circle_in from '../views/circle_in&out.vue'
import industry_structure from '../views/industry_structure.vue' 
import auth from '../views/auth.vue'
// 定义路由表
const routes = [
  {name: 'home', path: '/', component: home},
  {name: 'login', path: '/login', component: auth},
  {
    name: 'person',
    path: '/person',
    component: person,
    children: [
      {name: 'brain',path: 'brain',component:()=>import('../views/person/brain.vue')},
      {name: 'body',path: 'body',component: ()=>import('../views/person/body.vue')}
    ]
  },
  {
    name: 'world',
    path: '/world',
    component: world,
    children: [
      {name: 'industry_structure', path: 'industry_structure', component: ()=>import('../views/industry_structure.vue')},  
      {name: 'show_diff_structure',path: 'show_diff_structure',component: ()=>import('../views/show_diff_structure.vue')},
      {
        name: '地球',
        path: '地球',
        component: ()=>import('../views/world/地球.vue'),
        children: [
          {
            name: 'China',path: 'China',component: ()=>import('../views/world/China.vue'),
            children: [
              {name: 'hundreds_dots',path: 'hundreds_dots',component: ()=>import('../views/hundreds_dots.vue')}
            ]
          },
        ]
      },
    ]
  },
  {name: 'nation',path: '/nation',component: nation},
  {name: 'uploadpage',path:'/uploadpage',component:UploadPage},
  {name: 'father',path:'/father',component:father},
  {name: 'internation',path:'/internation',component:internation},
  {name: 'main',path:'/main',component:main},
  {name: 'circle',path:'/circle',component:circle},
  {name: 'use_tree',path:'/use_tree',component:use_tree},
  {name: 'hundreds_dots',path: '/hundreds_dots',component: hundreds_dots},
  {name: 'thousand_dots',path: '/thousand_dots',component: thousand_dots},
  {name: 'billion_dots',path: '/billion_dots',component: billion_dots},
  {name: 'skill_resource_wish', path: '/world/skill_resource_wish', component: skill_resource_wish},
  {name: 'stock_sector', path: '/stock_sector', component: stock_sector},
  {name: 'dynamic_graph', path: '/dynamic_graph', component: dynamic_graph},
  {name: 'use_circle', path: '/use_circle', component: use_circle},
  {name: 'test', path: '/test', component: test},
  {name: 'use_echarts', path: '/use_echarts', component: use_echarts},
  {name: 'use_graph', path: '/use_graph', component: use_graph},
  {name: 'testPage', path: '/testPage', component: testPage},
  {name: 'economy', path: '/economy', component: economy},
  {name: 'entertainment', path: '/entertainment', component: entertainment},
  {name: 'finance', path: '/finance', component: finance},
  {name: 'atom2social', path: '/atom2social', component: atom2social},
  {name: 'cash_flow', path: '/cash_flow', component: cash_flow},
  {name: 'floors', path: '/floors', component: floors},
  {name: 'maslow_needs', path: '/maslow_needs', component: maslow_needs},
  {name: 'circle_in', path: '/circle_in', component: circle_in},
  {name: 'use_timeline', path: '/use_timeline', component: use_timeline},
  {name: 'supply_chain', path: '/supply_chain', component: () => import('../views/supply_chain.vue')}
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes //路由表
})

export default router
