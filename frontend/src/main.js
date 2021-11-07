import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'

Vue.config.productionTip = false

store.dispatch('referential/updateQualityFamilySpecies')
store.dispatch('referential/updateIlot')
store.dispatch('observation/updateObservation')

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App)
}).$mount('#app')
