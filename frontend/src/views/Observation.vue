<template>
  <div>
    <v-card :loading="loading">
      <v-card-title>
        Observation

        <v-spacer></v-spacer>

        <v-btn color="error" :fab="this.$vuetify.breakpoint.xsOnly" :small="this.$vuetify.breakpoint.xsOnly" v-if="disabled" class="mr-4" @click.stop="dialogDelete = true">
          <v-icon>mdi-delete</v-icon>
          <span v-if="!this.$vuetify.breakpoint.xsOnly">Supprimer</span>
        </v-btn>
        <v-btn color="primary" :fab="this.$vuetify.breakpoint.xsOnly" :small="this.$vuetify.breakpoint.xsOnly" v-if="disabled" @click.stop="edit">
          <v-icon>mdi-pencil</v-icon>
          <span v-if="!this.$vuetify.breakpoint.xsOnly">Modifier</span>
        </v-btn>

        <v-btn color="primary" :fab="this.$vuetify.breakpoint.xsOnly" :small="this.$vuetify.breakpoint.xsOnly" v-if="!disabled" class="mr-4" @click.stop="undo">
          <v-icon>mdi-close</v-icon>
          <span v-if="!this.$vuetify.breakpoint.xsOnly">Annuler</span>
        </v-btn>
        <v-btn color="success" :fab="this.$vuetify.breakpoint.xsOnly" :small="this.$vuetify.breakpoint.xsOnly" v-if="!disabled" @click.stop="save" type="submit" :loading="loading" :disabled="!valid">
          <v-icon>mdi-content-save</v-icon>
          <span v-if="!this.$vuetify.breakpoint.xsOnly">Enregistrer</span>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-alert :value="alert" dense text outlined rounded="xl" :type="alertType" class="mb-6">
          {{ alertMessage }}
        </v-alert>

        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
        >
          <v-row>
            <v-col cols="12" sm="6">
              <v-autocomplete label="Îlot depuis lequel l’observation a été effectuée" :filled="!disabled" :disabled="disabled" :items="ilot" v-model="observation.ilot" :rules="required" prepend-inner-icon="mdi-map-marker"></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field label="Distance du bord de l'îlot en mètre" :filled="!disabled" :disabled="disabled" type="number" v-model="observation.ilot_distance" min="1" :rules="required" prepend-inner-icon="mdi-map-marker-distance"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-dialog ref="dialogDateRef" v-model="dialogDate" :return-value.sync="observation.date" persistent width="300">
                <template #activator="{ on }">
                  <v-text-field type="text" :filled="!disabled" :disabled="disabled" readonly :value="dateFormatted(observation.date)" label="Date de l'observation" v-on="on" :rules="required" required prepend-inner-icon="mdi-calendar"></v-text-field>
                </template>
                <v-date-picker locale="fr-fr" first-day-of-week="1" v-model="observation.date">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="dialogDate = false">Annuler</v-btn>
                  <v-btn text color="primary" @click="$refs.dialogDateRef.save(observation.date)">Valider</v-btn>
                </v-date-picker>
              </v-dialog>
            </v-col>
            <v-col cols="12" sm="6">
              <v-dialog ref="dialogTimeRef" v-model="dialogTime" :return-value.sync="observation.time" persistent width="300">
                <template #activator="{ on }">
                  <v-text-field type="text" :filled="!disabled" :disabled="disabled" readonly :value="timeFormatted(observation.time)" label="Heure de l'observation" v-on="on" :rules="required" required prepend-inner-icon="mdi-clock"></v-text-field>
                </template>
                <v-time-picker scrollable format="24hr" v-model="observation.time">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="dialogTime = false">Annuler</v-btn>
                  <v-btn text color="primary" @click="$refs.dialogTimeRef.save(observation.time)">Valider</v-btn>
                </v-time-picker>
              </v-dialog>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select label="Qualité de l’identification" :filled="!disabled" :disabled="disabled" :items="quality" v-model="observation.quality" :rules="required" prepend-inner-icon="mdi-eye"></v-select>
            </v-col>
          </v-row>

          <v-row class="mt-14">
            <v-col cols="12" sm="6">
              <v-select label="Famille d'animaux" :filled="!disabled" :disabled="disabled" :items="family" v-model="observation.family" :rules="required" @change="resetAnimalField()" :prepend-inner-icon="observation.family === 1 ? 'mdi-dolphin' : 'mdi-fish'"></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select label="Espèce d'animaux" :filled="!disabled" :disabled="disabled" :items="speciesFilter" v-model="observation.species" :rules="required" :prepend-inner-icon="observation.family === 1 ? 'mdi-dolphin' : 'mdi-fish'"></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-switch label="Individu seul" :filled="!disabled" :disabled="disabled" v-if="observation.family === 2" v-model="observation.fish_single" :rules="fishSingleRules" inset></v-switch>
            </v-col>
            <v-col cols="12" sm="6">
              <v-radio-group v-if="observation.family === 2" v-model="observation.fish_single" :rules="fishSingleRules" @change="resetFishField()">
                <v-radio label="Individu seul" :filled="!disabled" :disabled="disabled" :value="true"></v-radio>
                <v-radio label="Banc de poissons" :filled="!disabled" :disabled="disabled" :value="false"></v-radio>
              </v-radio-group>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field label="Taille estimée de l’individu en cm" :filled="!disabled" :disabled="disabled" v-if="observation.family === 1 || observation.fish_single" type="number" v-model="observation.animal_length" :rules="animalLengthRules" min="1" prepend-inner-icon="mdi-arrow-expand-horizontal"></v-text-field>
              <v-text-field label="Nombre d’individus dans le banc" :filled="!disabled" :disabled="disabled" v-if="observation.family === 2 && !observation.fish_single" type="number" v-model="observation.fish_number" :rules="fishNumberRules" min="1" prepend-inner-icon="mdi-numeric"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field label="Temps d’apnée observé en minute" :filled="!disabled" :disabled="disabled" v-if="observation.family === 1" type="number" v-model="observation.mammel_apnea_duration" :rules="mammelApneaDurationRules" min="1" prepend-inner-icon="mdi-timer"></v-text-field>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialogDelete" persistent max-width="400">
      <v-card>
        <v-card-title class="justify-center headline">Confirmation de la suppression</v-card-title>
        <v-card-text class="text-center">Êtes-vous sûr de vouloir supprimer cette observation</v-card-text>
        <v-card-actions class="justify-center pb-6">
          <v-btn color="error" @click="remove" class="mr-4">
            <v-icon left>mdi-delete</v-icon>
            Supprimer
          </v-btn>
          <v-btn color="primary" @click.stop="dialogDelete = false">
            <v-icon left>mdi-close</v-icon>
            Annuler
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
  ::v-deep .theme--light.v-input--is-disabled input,
  ::v-deep .theme--light.v-select .v-select__selection.v-select__selection--comma.v-select__selection--disabled {
    color: #000;
  }

  ::v-deep .theme--dark.v-input--is-disabled input,
  ::v-deep .theme--dark.v-select .v-select__selection.v-select__selection--comma.v-select__selection--disabled {
    color: #fff;
  }
</style>

<script>
import http from '@/helpers/http.js'
import { mapGetters } from 'vuex'

export default {
  name: 'Observation',
  data () {
    return {
      dialogDate: false,
      dialogTime: false,
      dialogDelete: false,
      disabled: true,
      valid: false,
      loading: false,
      alert: false,
      alertType: 'info',
      alertMessage: '',
      required: [
        v => !!v || 'Champ obligatoire.'
      ],
      fishSingleRules: [
        v => (v !== null && this.observation.family === 2) || 'Champ obligatoire.'
      ],
      animalLengthRules: [
        v => (!!v && this.observation.family === 1) || (!!v && this.observation.family === 2 && this.observation.fish_single) || 'Champ obligatoire.'
      ],
      fishNumberRules: [
        v => (!!v && this.observation.family === 2 && !this.observation.fish_single) || 'Champ obligatoire.'
      ],
      mammelApneaDurationRules: [
        v => (!!v && this.observation.family === 1) || 'Champ obligatoire.'
      ],
      observationSave: {},
      observation: {
        family: null,
        species: null,
        ilot: null,
        ilot_distance: null,
        date: null,
        time: null,
        quality: null,
        animal_length: null,
        mammel_apnea_duration: null,
        fish_single: true,
        fish_number: null
      }
    }
  },
  computed: {
    ...mapGetters('referential', ['quality', 'family', 'species', 'ilot']),
    speciesFilter () { return this.species.filter(element => element.family === this.observation.family) }
  },
  methods: {
    dateFormatted (date) {
      if (!date) { return null }
      const [year, month, day] = date.split('-')
      return day + '/' + month + '/' + year
    },
    timeFormatted (time) {
      if (!time) { return null }
      const [hour, minute] = time.split(':')
      return hour + 'h' + minute
    },
    resetAnimalField () {
      this.observation.species = null
      this.observation.animal_length = null
      this.observation.mammel_apnea_duration = null
      this.observation.fish_single = true
      this.observation.fish_number = null
      this.$refs.form.validate()
    },
    resetFishField () {
      this.observation.animal_length = null
      this.observation.mammel_apnea_duration = null
      this.observation.fish_number = null
      this.$refs.form.validate()
    },
    edit () {
      this.observationSave = JSON.parse(JSON.stringify(this.observation))
      this.disabled = false
      this.$refs.form.validate()
    },
    undo () {
      if (!this.observation.id) {
        this.$router.push('/home')
      } else {
        this.observation = JSON.parse(JSON.stringify(this.observationSave))
        this.observationSave = null
        this.disabled = true
      }
    },
    async save () {
      if (!this.$refs.form.validate()) {
        this.snackbar = { show: true, text: 'Veuillez remplir et vérifier tous les champs', color: 'error' }
        return false
      }

      const data = new FormData()
      data.append('ilot', this.observation.ilot)
      data.append('ilot_distance', this.observation.ilot_distance)
      data.append('date_time', `${this.observation.date} ${this.observation.time}:00`)
      data.append('quality', this.observation.quality)

      data.append('species', this.observation.species)
      if (this.observation.family === 1) {
        data.append('mammel_apnea_duration', this.observation.mammel_apnea_duration)
        data.append('animal_length', this.observation.animal_length)
      }
      if (this.observation.family === 2 && this.observation.fish_single === true) {
        data.append('fish_single', 'True')
        data.append('animal_length', this.observation.animal_length)
      }
      if (this.observation.family === 2 && this.observation.fish_single === false) {
        data.append('fish_single', 'False')
        data.append('fish_number', this.observation.fish_number)
      }
      this.loading = true
      if (this.observation.id) {
        const response = await http.xhr('put', `/api/observation/${this.observation.id}`, data)
      } else {
        const response = await http.post('/api/observation/', data)
      }
      this.loading = false
      this.$router.push('/observation/list')
      return true
    },
    async remove () {
      this.loading = true
      const response = await http.xhr('delete', `/api/observation/${this.$route.params.id}`)
      this.loading = false
      if (!response) {
        this.alertType = 'error'
        this.alertMessage = 'Erreur de connexion'
        this.alert = true
      }
      if (response.status === 'error') {
        this.alertType = 'error'
        this.alertMessage = response.message
        this.alert = true
      }
      if (response.status === 'fail') {
        this.alertType = 'error'
        this.alertMessage = Object.values(response.data).join(' ')
        this.alert = true
      }
      if (response.status === 'success') {
        this.$router.push('/observation/list')
      }
    }
  },
  async created () {
    if (this.$route.params.id) {
      this.loading = true
      const response = await http.get(`/api/observation/${this.$route.params.id}`)
      this.loading = false
      if (!response) {
        this.alertType = 'error'
        this.alertMessage = 'Erreur de connexion'
        this.alert = true
      }
      if (response.status === 'error') {
        this.alertType = 'error'
        this.alertMessage = response.message
        this.alert = true
      }
      if (response.status === 'fail') {
        this.alertType = 'error'
        this.alertMessage = Object.values(response.data).join(' ')
        this.alert = true
      }
      if (response.status === 'success') {
        this.observation = response.data.observation
        const date = new Date(this.observation.date_time)
        this.observation.date = `${date.getFullYear().toString()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
        this.observation.time = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
        this.$refs.form.validate()
      }
    } else {
      this.disabled = false
    }
  }
}
</script>
