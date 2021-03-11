<template>

</template>

<script>
import {mapGetters} from 'vuex'
import prettydate from 'pretty-date'

export default {
  name: 'ListView',
  computed: mapGetters(['items']),
  methods: {
    convertDateToTimeAgo(date) {
      return prettydate.format(new Date(date))
    },
    deleteList(list) {
      this.$store.dispatch('deleteItem', list)
    },
  },
  beforeMount() {
    this.$store.dispatch('getItems')

  },

}
</script>

<style scoped>
.comment {
  background-color: #ececec;
  margin: 0 0 10px 0;
  padding: 10px;
}

.subtask-item {
  background-color: #e4e4e4;
}

.comment-photo {
  width: 200px;
}

</style>