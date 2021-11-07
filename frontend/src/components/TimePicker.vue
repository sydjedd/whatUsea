<template>
<div>
  <v-dialog ref="dialogRef" v-model="show" :return-value.sync="timeLocal" persistent width="300">
    <template #activator="{ on }">
      <v-text-field type="text" :filled="filled" :disabled="disabled" readonly :value="timeFormatted" :label="label" v-on="on" :required="required || false" :rules="rules || []" prepend-inner-icon="mdi-clock"></v-text-field>
    </template>
    <v-time-picker scrollable format="24hr" v-model="timeLocal">
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="show = false">Annuler</v-btn>
      <v-btn text color="primary" @click="$refs.dialogRef.save(timeLocal)">Valider</v-btn>
    </v-time-picker>
  </v-dialog>
</div>
</template>

<script>
export default {
  name: 'TimePicker',
  props: { time: String, label: String, filled: Boolean, disabled: Boolean, rules: Array, required: Boolean },
  data () {
    return {
      show: false
    }
  },
  computed: {
    timeFormatted () {
      if (!this.timeLocal) {
        return null
      }
      const [hour, minute] = this.timeLocal.split(':')
      return hour + 'h' + minute
    },
    timeLocal: {
      get () {
        return this.time
      },
      set (value) {
        this.$emit('update:time', value)
      }
    }
  }
}
</script>
