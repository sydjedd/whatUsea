<template>
  <v-app>
    <v-app-bar color="primary" dense dark app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ this.$store.state.common.appName }}</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list dense nav>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="text-h6 pb-1">
              {{ this.$store.state.common.appName }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item to="/home" link router>
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Accueil</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/observation/list" link router>
          <v-list-item-icon>
            <v-icon>mdi-fish</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Liste des observations</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/observation/add" link router>
          <v-list-item-icon>
            <v-icon>mdi-jellyfish</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Nouvelle observation</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/map" link router>
          <v-list-item-icon>
            <v-icon>mdi-map</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Carte</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="grey lighten-3">
      <v-container>
        <router-view :key="$route.fullPath"></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  data () {
    return {
      drawer: true
    }
  },

  computed: {
    initial () {
      const nom = this.$store.state.user.first_name ? this.$store.state.user.first_name.charAt(0).toLocaleUpperCase() : ''
      const prenom = this.$store.state.user.last_name ? this.$store.state.user.last_name.charAt(0).toLocaleUpperCase() : ''
      return nom + prenom
    }
  },

  methods: {
    async logout () {
      await this.$store.dispatch('user/logout')
      this.$router.push('/')
    }
  }
}
</script>
