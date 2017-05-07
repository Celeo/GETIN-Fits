<template lang="pug">
  section.section
    div.container(v-if="error")
      server-error
    div.container(v-if="error === false")
      nav.level
        div.level-left(v-if="fits !== null")
          b-field(label="Select a fit to edit")
            b-select(placeholder="select" v-model="selectedId")
              b-option(
                v-for="fit in fits"
                v-bind:value="fit.id"
                v-bind:key="fit.id"
              ) {{ fit.category }} - {{ fit.name }}
        div.level-right
          div.block
            button.button.is-success(v-if="selectedId" @click="save")
              b-icon(icon="floppy-o")
              span Save changes
            button.button.is-info(@click="prompt")
              b-icon(icon="plus")
              span Create new fit
      div.columns(v-if="selectedId")
        div#panel-input.column.is-half
          p.control
            textarea#entry.textarea(v-model="fitContent")
        div.column.is-half
          div#panel-output(v-html="fitRendered")
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import { renderer } from '../util'
import ServerError from '../components/ServerError'


export default {
  components: {
    ServerError
  },
  data() {
    return {
      error: null,
      fits: null,
      selectedId: null,
      fitContent: ''
    }
  },
  computed: {
    fitRendered() {
      return marked(this.fitContent, { sanitize: true, renderer })
    },
    selectedFit() {
      return this.fits.filter(e => e.id === this.selectedId)[0]
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits`)
        this.fits = response.data
        this.error = false
      } catch (error) {
        this.error = true
        console.error(error)
      }
    },
    async save() {
      try {
        await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}fits/${this.selectedFit.id}`, { content: this.fitContent })
        this.$toast.open({
          message: 'Fit saved',
          type: 'is-success'
        })
      } catch (error) {
        this.$dialog.alert({
          message: 'There was an error saving the data',
          type: 'is-danger',
          hasIcon: true
        })
        console.error(error)
      }
    },
    async prompt() {
      this.$dialog.prompt({
        message: 'New fit creation',
        maxlength: 30,
        placeholder: 'name',
        onConfirm: (value) => {
          // TODO
        }
      })
    }
  },
  async created() {
    await this.loadData()
  },
  watch: {
    selectedId(newId) {
      this.fitContent = this.selectedFit.content
    }
  }
}
</script>

<style lang="stylus" scoped>
#panel-input
  border-right 1px solid rgba(0, 0, 0, .3)

#panel-output
  height 65vh
  overflow-y scroll

#entry
  height 70vh !important
</style>
