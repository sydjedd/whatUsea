import http from '@/helpers/http.js'
import referential from '@/store/modules/referential'

export default {
  namespaced: true,
  state: {
    observation: JSON.parse(localStorage.getItem('observation')) || []
  },
  getters: {
    observation: state => state.observation.map(e => {
      const date = new Date(e.date_time)
      return {
        ...e,
        date_time: `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()} à ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`,
        ilot: referential.state.ilot.find(o => o.id === e.ilot),
        quality: referential.state.quality.find(o => o.id === e.quality),
        species: referential.state.species.find(o => o.id === e.species),
        family: referential.state.family.find(o => o.id === e.family),
        fish_single: e.fish_single ? 'Oui' : (e.fish_single === false ? 'Non' : '')
      }
    })
  },
  mutations: {
    UPDATE_OBSERVATION (state, newValue) {
      localStorage.setItem('observation', JSON.stringify(newValue))
      state.observation = newValue
    }
  },
  actions: {
    async updateObservation ({ commit, state }) {
      const response = await http.get('/api/observation/')
      if (response && response.status === 'success' && response.data && response.data.observation) {
        commit('UPDATE_OBSERVATION', response.data.observation)
      }
    }
  }
}
