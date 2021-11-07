import http from '@/helpers/http.js'

export default {
  namespaced: true,
  state: {
    quality: JSON.parse(localStorage.getItem('quality')) || [],
    family: JSON.parse(localStorage.getItem('family')) || [],
    species: JSON.parse(localStorage.getItem('species')) || [],
    ilot: JSON.parse(localStorage.getItem('ilot')) || []
  },
  getters: {
    quality: state => state.quality.map(element => ({ value: element.id, text: element.libelle })),
    family: state => state.family.map(element => ({ value: element.id, text: element.libelle })),
    species: state => state.species.map(element => ({ value: element.id, text: element.libelle, family: element.family })),
    ilot: state => state.ilot.map(element => ({
      value: element.id,
      text: element.titre,
      latLng: element.localisation.replace(/^POINT \(([0-9.-]+) ([0-9.-]+)\)$/, '$2 $1').split(' ')
    }))
  },
  mutations: {
    UPDATE_QUALITY (state, newValue) {
      localStorage.setItem('quality', JSON.stringify(newValue))
      state.quality = newValue
    },
    UPDATE_FAMILY (state, newValue) {
      localStorage.setItem('family', JSON.stringify(newValue))
      state.family = newValue
    },
    UPDATE_SPECIES (state, newValue) {
      localStorage.setItem('species', JSON.stringify(newValue))
      state.species = newValue
    },
    UPDATE_ILOT (state, newValue) {
      localStorage.setItem('ilot', JSON.stringify(newValue))
      state.species = newValue
    }
  },
  actions: {
    async updateQualityFamilySpecies ({ commit, state }) {
      if (!state.quality.length || !state.family.length || !state.species.length) {
        const response = await http.get('/api/referential/')
        if (response && response.status === 'success' && response.data) {
          if (response.data.quality) {
            commit('UPDATE_QUALITY', response.data.quality)
          }
          if (response.data.family) {
            commit('UPDATE_FAMILY', response.data.family)
          }
          if (response.data.species) {
            commit('UPDATE_SPECIES', response.data.species)
          }
        }
      }
    },
    async updateQuality ({ commit, state }) {
      if (!state.quality.length) {
        const response = await http.get('/api/referential/quality/')
        if (response && response.status === 'success' && response.data && response.data.quality) {
          commit('UPDATE_QUALITY', response.data.quality)
        }
      }
    },
    async updateFamily ({ commit, state }) {
      if (!state.family.length) {
        const response = await http.get('/api/referential/family/')
        if (response && response.status === 'success' && response.data && response.data.family) {
          commit('UPDATE_FAMILY', response.data.family)
        }
      }
    },
    async updateSpecies ({ commit, state }) {
      if (!state.species.length) {
        const response = await http.get('/api/referential/species/')
        if (response && response.status === 'success' && response.data && response.data.species) {
          commit('UPDATE_SPECIES', response.data.species)
        }
      }
    },
    async updateIlot ({ commit, state }) {
      if (!state.ilot.length) {
        const response = await http.get('/pandoreweb/pandore/ilot/IlotDto')
        if (response && response.success === true && response.data) {
          commit('UPDATE_ILOT', response.data)
        }
      }
    }
  }
}
