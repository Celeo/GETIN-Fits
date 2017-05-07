<template lang="pug">
  section.section
    div.container
      div(v-if="!error")
        nav.nav.has-deep-shadow
          div.nav-center
            category-tab(
              v-for="category in data"
              v-bind:key='category'
              v-bind:data='category'
            )
        nav.nav.has-deep-shadow
          div.nav-center(
            v-for="category in data"
            v-if="$store.getters.category === category.name"
          )
            ship-tab(
              v-if="category.ships.length > 0"
              v-for="ship in category.ships"
              v-bind:name="ship.name"
              v-bind:key="ship.name"
            )
            div(v-if="category.ships.length === 0")
              a.nav-item No fits in this category
        section.section
          div(v-html="markdown(ship.fit)")
      div(v-else)
        server-error
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import { renderer } from '../util'
import CategoryTab from '../components/CategoryTab'
import ShipTab from '../components/ShipTab'
import ServerError from '../components/ServerError'


export default {
  components: {
    CategoryTab,
    ShipTab,
    ServerError
  },
  data() {
    return {
      data: [],
      error: false
    }
  },
  computed: {
    ship() {
      for (let category of this.data) {
        for (let ship of category.ships) {
          if (ship.name === this.$store.getters.ship) {
            return ship
          }
        }
      }
      return { fit: '' }
    }
  },
  methods: {
    markdown(s) {
      return marked(s, { sanitize: true, renderer })
    },
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}categories`)
        this.data = response.data
        this.error = false
      } catch (error) {
        this.error = true
        console.error(error)
      }
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>
