import Vue from 'vue'
import Vuex from 'vuex'

import common from './modules/common'
import referential from './modules/referential'
import observation from './modules/observation'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    common,
    referential,
    observation
  },
  strict: process.env.NODE_ENV !== 'production'
})
