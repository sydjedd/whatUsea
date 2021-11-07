<template>
<div>
  <v-dialog ref="dialogRef" v-model="modal" :return-value.sync="dateLocal" persistent width="300">
    <template #activator="{ on, attrs }">
      <v-text-field type="text" :filled="filled" readonly :value="dateLocal" :label="label" v-bind="attrs" v-on="on" :required="required || false" :rules="rules || []" prepend-inner-icon="mdi-calendar"></v-text-field>
    </template>
    <v-date-picker locale="fr-fr" first-day-of-week="1" v-model="dateLocal">
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="modal = false">Annuler</v-btn>
      <v-btn text color="primary" @click="$refs.dialogRef.save(dateLocal)">Valider</v-btn>
    </v-date-picker>
  </v-dialog>
</div>
</template>

<script>
export default {
  name: 'DatePicker',
  props: { date: String, label: String, filled: Boolean, disabled: Boolean, rules: Array, required: Boolean },
  data () {
    return {
      modal: false
    }
  },
  computed: {
    dateFormatted () {
      if (!this.dateLocal) {
        return null
      }
      const [year, month, day] = this.dateLocal.split('-')
      return day + '/' + month + '/' + year
    },
    dateLocal: {
      get () {
        return this.date
      },
      set (value) {
        console.log(this.date + ' ' + value)
        this.$emit('update:date', value)
      }
    }
  }
}
</script>
