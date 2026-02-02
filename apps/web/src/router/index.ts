import { createRouter, createWebHashHistory } from 'vue-router'
import home from '../views/home.vue'
import test from '../views/test.vue'
import person from '../views/person.vue'
import world from '../views/world.vue'
import nation from '../views/nation.vue'
import internation from '../views/internation.vue'
import UploadPage from '../views/UploadPage.vue'
// 定义路由表
const routes = [
  {name: 'home', path: '/', component: home},
  {name: 'test',path: '/test',component: test},
  {name: 'person',path: '/person',component: person},
  {name: 'world',path: '/world',component: world},
  {name: 'nation',path: '/nation',component: nation},
  {name: 'internation',path: '/internation',component: internation},
  {name: 'uploadpage',path:'/uploadpage',component:UploadPage}
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes //路由表
})

export default router
