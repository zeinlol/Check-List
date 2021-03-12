<template>
  <div id="lists" class="col-12">
    <div class="card checklist-item" v-for="checklist in lists" :key="checklist.id">
      <div class="card-body list-group text-center">
        <h2 class="card-title checklist-title">
          <i class="fa fa-check" aria-hidden="true" v-if="checklist.completed"
             @click="changeListState(checklist, false)"></i>
          <a href="#a" v-else @click="changeListState(checklist, true)"><i class="fa fa-square-o"
                                                                           aria-hidden="true"></i></a>
          <a :href="'/list/' + checklist.id">{{ checklist.name }}</a>
        </h2>
        <p class="card-subtitle text-muted">Created: {{ checklist.date }}</p>
        <p class="card-text list-description">{{ checklist.description }}</p>
        <button type="button" class="btn btn-outline-danger" data-toggle="modal"
                :data-target="'#check-modal-' + checklist.id">Delete List
        </button>


        <div class="modal" :id="'check-modal-' + checklist.id" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Delete List</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <p>Are you sure to delete list "{{ checklist.name }}"?</p>
                <p>If yes - click 'Delete'</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-danger" @click="deleteList(checklist)">Delete</button>
              </div>
            </div>
          </div>
        </div>

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
    changeListState(list, state) {
      console.log(list.toString(), state.toString())
      this.$store.dispatch('changeListState', {list, state})
    },
  },
  beforeMount() {
    this.$store.dispatch('getLists', 'getItems')

  },
}

</script>

<style>
header {
  margin-top: 50px;
}

.card-body {
  padding-right: 0;
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


</style>
