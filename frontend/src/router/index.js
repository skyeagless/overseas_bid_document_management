import { createRouter, createWebHistory } from 'vue-router'
import TenderFiles from '../views/TenderFiles.vue'
import ProjectRecords from '../views/ProjectRecords.vue'
import Personnel from '../views/Personnel.vue'
import Suppliers from '../views/Suppliers.vue'
import Equipment from '../views/Equipment.vue'
import Search from '../views/Search.vue'

const routes = [
  { path: '/', redirect: '/tender-files' },
  { path: '/tender-files', name: 'TenderFiles', component: TenderFiles },
  { path: '/project-records', name: 'ProjectRecords', component: ProjectRecords },
  { path: '/personnel', name: 'Personnel', component: Personnel },
  { path: '/suppliers', name: 'Suppliers', component: Suppliers },
  { path: '/equipment', name: 'Equipment', component: Equipment },
  { path: '/search', name: 'Search', component: Search }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
