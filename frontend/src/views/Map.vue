<template>
        <l-map
          id="map"
          ref="map"
          :center="center"
          :options="options"
          :zoom="zoom"
          @update:zoom="zoomUpdated"
          @update:center="centerUpdated"
        >
          <l-tile-layer
            :url="url"
            :attribution="attribution"
          ></l-tile-layer>
          <l-marker v-for="element in ilot" :key="element.id" :lat-lng="element.latLng"
          >
            <l-popup>{{ element.text }}</l-popup>
          </l-marker>
        </l-map>
</template>

<style>
#map {
  height: calc(100vh - 72px);
  width: 100%;
  z-index: 0;
}
</style>

<script>
import { mapGetters } from 'vuex'
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Hack pour que les icons marker fonctionnent
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

export default {
  name: 'Map',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [-22.200024, 166.774662],
      options: {
        zoomSnap: 0.5
      },
      zoom: 7,
      markers: [
        { id: 1, coordinates: [49.11491, 6.17881] },
        { id: 2, coordinates: [49.13329, 6.15437] },
        { id: 3, coordinates: [49.10216, 6.15885] },
        { id: 4, coordinates: [49.13601, 6.19963] },
        { id: 5, coordinates: [49.105563, 6.182234] }
      ]
    }
  },
  computed: {
    ...mapGetters('referential', ['ilot'])
  },
  methods: {
    zoomUpdated (zoom) {
      this.zoom = zoom
    },
    centerUpdated (center) {
      this.center = center
    }
  }
}
</script>
