<template>
  <div>
    <v-alert type="info" dismissible dense>
      Cliquez sur une ligne pour le détail de l'observation
    </v-alert>

    <v-card>
      <v-card-title>
        Observations

        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Rechercher"
          single-line
          hide-details
        ></v-text-field>

        <v-spacer></v-spacer>

        <v-btn color="primary" :fab="this.$vuetify.breakpoint.xsOnly" :small="this.$vuetify.breakpoint.xsOnly" to="/observation/add">
          <v-icon>mdi-plus</v-icon>
          <span v-if="!this.$vuetify.breakpoint.xsOnly">Ajouter</span>
        </v-btn>
        <v-btn color="primary" :fab="this.$vuetify.breakpoint.xsOnly" :small="this.$vuetify.breakpoint.xsOnly" class="ml-4" @click.stop="refreshObservation">
          <v-icon>mdi-refresh</v-icon>
          <span v-if="!this.$vuetify.breakpoint.xsOnly">Rafraichir</span>
        </v-btn>
      </v-card-title>

      <v-data-table
        :loading="loading"
        :headers="headers"
        :items="observation"
        :search="search"
        @click:row="clickRow"
      >
      </v-data-table>
    </v-card>
  </div>
</template>

<style scoped>
  ::v-deep .v-data-table tr:hover {
    cursor: pointer;
  }
</style>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'ObservationList',
  data () {
    return {
      loading: false,
      search: '',
      headers: [
        { text: 'Îlot', value: 'ilot.titre' },
        { text: 'Îlot distance', value: 'ilot_distance' },
        { text: 'Date', value: 'date_time' },
        { text: 'Qualité de l’identification', value: 'quality.libelle' },
        { text: 'Famille d\'animaux', value: 'family.libelle' },
        { text: 'Espèce d\'animaux', value: 'species.libelle' },
        { text: 'Poisson seul', value: 'fish_single' },
        { text: 'Nbr poisson', value: 'fish_number' },
        { text: 'Taille (cm)', value: 'animal_length' },
        { text: 'Temps d’apnée', value: 'mammel_apnea_duration' }
      ]
    }
  },
  computed: {
    ...mapGetters('observation', ['observation'])
  },
  methods: {
    ...mapActions('observation', ['updateObservation']),
    async refreshObservation () {
      this.loading = true
      this.search = ''
      await this.updateObservation()
      this.loading = false
    },
    clickRow (observation) {
      this.$router.push(`/observation/${observation.id}`)
    }
  },
  async created () {
    this.refreshObservation()
  }
}
</script>
