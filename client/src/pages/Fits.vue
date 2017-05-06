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
            div(v-if="category.ships.length > 0")
              ship-tab(v-for="ship in category.ships" v-bind:name="ship.name" v-bind:key="ship.name")
            div(v-else)
              a.nav-item No fits in this category
        section.section
          div(v-html="markdown(ship.fit)")
      div(v-else)
        server-error
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import CategoryTab from '../components/CategoryTab'
import ShipTab from '../components/ShipTab'
import ServerError from '../components/ServerError'


const renderer = new marked.Renderer()
renderer.heading = (text, level) => {
  return `<h${level} class="title is-${level}">${text}</h${level}>`
}

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
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits`)
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

<style lang="stylus" scoped>
a.nav-item.is-tab.big
  font-size 30px
  padding-left 100px
  padding-right 100px

.has-deep-shadow
  box-shadow 0 0 10px 2px rgba(10, 10, 10, 0.1)
</style>
