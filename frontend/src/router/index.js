import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/Home.vue'
import Map from '@/views/Map.vue'
import ObservationList from '@/views/ObservationList.vue'
import Observation from '@/views/Observation.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    { path: '/home', name: 'Accueil', component: Home },
    { path: '/map', name: 'Carte des observations', component: Map },
    { path: '/observation/list', name: 'Liste des observations', component: ObservationList },
    { path: '/observation/add', name: 'Ajouter une observation', component: Observation },
    { path: '/observation/:id(.+)', name: 'Détails d\'une observation', component: Observation },
    { path: '*', name: 'Redirection accueil', redirect: '/home' }
  ]
})

export default router
