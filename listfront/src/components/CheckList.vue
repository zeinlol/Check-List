<template>
  <div id="lists" class="col-12">
    <div class="card checklist-item" v-for="checklist in lists" :key="checklist.id">
      <div class="card-body list-group text-center"><a :href="'/list/' + checklist.id">
        <h2 class="card-title checklist-title">{{ checklist.name }}</h2></a>
        <p class="card-subtitle text-muted">Created: {{ checklist.date }}</p>
        <p class="card-text list-description">{{ checklist.description }}</p>
        <button type="button" class="btn btn-outline-danger" @click="deleteList(checklist)">Delete List</button>
      </div>
    </div>
  </div>
</template>


<script>
import {mapGetters} from 'vuex'
import prettydate from 'pretty-date'

export default {
  name: 'lists-list',
  computed: mapGetters(['lists']),
  methods: {
    convertDateToTimeAgo(date) {
      return prettydate.format(new Date(date))
    },
    deleteList(list) {
      this.$store.dispatch('deleteList', list)
    },
  },
  beforeMount() {
    this.$store.dispatch('getLists')

  },
}

</script>

<style>
header {
  margin-top: 50px;
}

.checklist-item {
  word-wrap: break-word;
}

span.completed {
  text-decoration: line-through;
}

.category_name {
  padding-left: 15px;
  pointer-events: none;
}

.category_name:hover {
  padding-left: 15px;
  pointer-events: none;
}

.list-description {
  font-size: 1.5em;
}

.checklist-title {
  background-color: #e2e2e2;
}

.checklist-title:focus-within {
  background-color: #ff0000;
  font-size: larger;
}


</style>
