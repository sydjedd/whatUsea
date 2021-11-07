import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'
import fr from '@/locale/fr'
import en from '@/locale/en'
import ja from '@/locale/ja'

Vue.use(Vuetify)

export default new Vuetify({
  lang: {
    locales: { fr, en, ja },
    current: 'fr'
  }
})
