module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: 'dist',
  assetsDir: 'static',
  indexPath: 'index.html',
  productionSourceMap: false,
  devServer: {
    proxy: {
      '^/api/.*$': {
        target: process.env.VUE_APP_API_URL,
        pathRewrite: { '^/api': '' },
        changeOrigin: true
      },
      '^/pandoreweb/pandore/ilot/IlotDto.*$': {
        target: 'https://www.province-sud.nc',
        changeOrigin: true
      }
    }
  }
}
