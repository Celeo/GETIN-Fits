<template lang="pug">
  section.section
    div.container(v-if="error")
      server-error
    div.container(v-if="error === false")
      nav.level
        div.level-left(v-if="fits !== null")
          div.level-item(v-if="!refreshing")
            b-field(label="Select a fit to edit")
              b-select(placeholder="select" v-model="selectedId")
                b-option(
                  v-for="fit in fits"
                  v-bind:value="fit.id"
                  v-bind:key="fit.id"
                ) \#{{ fit.id }}: {{ fit.name }}
          div.level-item(v-if="!refreshing")
            b-field(label="Set the category")
              b-select(placeholder="select" v-model="categoryId" v-bind:disabled="selectedId === 0")
                b-option(
                  v-for="category in categories"
                  v-bind:value="category.id"
                  v-bind:key="category.id"
                ) {{ category.name }}
        div.level-right
          div.block
            button.button.is-success(v-if="selectedId" @click="save")
              b-icon(icon="floppy-o")
              span Save changes
            button.button.is-danger(v-if="selectedId" @click="promptDelete")
              b-icon(icon="trash-o")
              span Delete fit
            button.button.is-info(@click="createNew")
              b-icon(icon="plus")
              span Create new fit
      div.columns(v-if="selectedId !== 0")
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
      categories: null,
      selectedId: 0,
      categoryId: 0,
      fitContent: '',
      refreshing: false
    }
  },
  computed: {
    fitRendered() {
      return marked(this.fitContent, { sanitize: true, renderer })
    },
    selectedFit() {
      return this.fits.filter(e => e.id === this.selectedId)[0]
    },
    selectedCategory() {
      return this.categories.filter(e => e.id === this.categoryId)[0]
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits`)
        this.fits = response.data.fits
        this.categories = response.data.categories
        this.error = false
      } catch (error) {
        this.error = true
        console.error(error)
      }
    },
    async save() {
      try {
        const data = {
          content: this.fitContent,
          category_id: this.selectedCategory.id
        }
        await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}fits/${this.selectedFit.id}`, data)
        await this.loadData()
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
    async promptDelete() {
      this.$dialog.confirm({
        title: 'Delete fit',
        message: 'Are you sure that you  want to <strong>delete</strong> this fit? This cannot be undone.',
        confirmText: 'Dlete',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: async () => {
          try {
            await this.$store.getters.axios.delete(`${Vue.config.SERVER_URL}fits/${this.selectedId}`)
            await this.loadData()
            this.selectedId = 0
            this.categoryId = 0
            this.refreshing = true
            Vue.nextTick(() => {
              this.refreshing = false
            })
            this.$toast.open({
              message: 'Fit deleted',
              type: 'is-success'
            })
          } catch (error) {
            this.$dialog.alert({
              message: 'There was an error deleting that fit',
              type: 'is-danger',
              hasIcon: true
            })
          }
        }
      })
    },
    async createNew() {
      this.$dialog.prompt({
        message: 'New fit creation',
        maxlength: 30,
        placeholder: 'name',
        onConfirm: async (value) => {
          try {
            await this.$store.getters.axios.post(`${Vue.config.SERVER_URL}fits`, { name: value })
            await this.loadData()
            this.$toast.open({
              message: 'New fit added',
              type: 'is-success'
            })
          } catch (error) {
            this.$dialog.alert({
              message: 'There was an error saving the new fit',
              type: 'is-danger',
              hasIcon: true
            })
          }
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
      this.categoryId = this.selectedFit.category_id
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
