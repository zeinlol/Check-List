<template>

  <div id="lists" class="col-12">
    <div class="card checklist-item" v-for="item in items" :key="item.id">
      <div class="card-body list-group text-center">
        <h2 class="card-title checklist-title">
          <i class="fa fa-check" aria-hidden="true" v-if="item.completed" @click="changeItemState(item, false)"></i>
          <a href="#a" v-else @click="changeItemState(item, true)"><i class="fa fa-square-o" aria-hidden="true"></i></a>
          <a :href="'/list/' + item.id">{{ item.title }}</a>
        </h2>
        <p class="card-subtitle text-muted">Created: {{ item.date }}</p>
        <button type="button" class="btn btn-outline-danger" @click="deleteItem(item)">Delete Item</button>
      </div>
    </div>
  </div>


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
    deleteItem(item) {
      this.$store.dispatch('deleteItem', item)
    },
  },
  beforeMount() {
    console.log(this.$store.dispatch('getItems'))
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