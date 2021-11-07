export default {
  namespaced: true,
  state: {
    // TODO supprimer name et desciption du fichier .env
    appName: process.env.VUE_APP_NAME,
    appDescription: process.env.VUE_APP_DESCRIPTION
  }
}
