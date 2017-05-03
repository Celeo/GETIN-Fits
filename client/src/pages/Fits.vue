<template lang="pug">
  section.section
    div.container
      nav.nav.has-deep-shadow
        div.nav-center
          category-tab(
            v-for="category in categories"
            v-bind:key='category'
            v-bind:data='category'
          )
      nav.nav.has-deep-shadow
        div.nav-center(
          v-for="category in categories"
          v-if="$store.getters.category === category.name"
        )
          ship-tab(v-for="ship in category.ships" v-bind:name="ship.name" v-bind:key="ship.name")
      pre
        code {{ ship.fit }}
</template>

<script>
import CategoryTab from '../components/CategoryTab'
import ShipTab from '../components/ShipTab'

import testCategories from './testData'


export default {
  components: {
    CategoryTab,
    ShipTab
  },
  data() {
    return {
      categories: testCategories
    }
  },
  computed: {
    ship() {
      for (let category of this.categories) {
        for (let ship of category.ships) {
          if (ship.name === this.$store.getters.ship) {
            return ship
          }
        }
      }
      return { fit: '' }
    }
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
