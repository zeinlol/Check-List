<template>
  <div id="lists" class="col-12">
    <div class="card checklist-item" v-for="checklist in lists" :key="checklist.id">
      <div class="card-body list-group text-center">
        <h2 class="card-title checklist-title">
          <i class="fa fa-check" aria-hidden="true" v-if="checklist.done"
             @click="changeListState(checklist, false)"></i>
          <i class="fa fa-square-o" aria-hidden="true" v-else @click="changeListState(checklist, true)"></i>
          {{ checklist.name }}
        </h2>
        <p class="card-subtitle text-muted">Created: {{ checklist.date }}</p>
        <p class="card-text list-description">{{ checklist.description }}</p>
        <list-view></list-view>
        <form class="form-horizontal" type="submit" @submit="submitForm">
          <label class="form-label">Title</label>
          <input class="form-input" type="text" v-model="name" placeholder="Type checklist title...">
          <input class="form-input" type="hidden" v-model="related_list">
          <button class="btn btn-primary" type="submit" @click="createItem(related_list=checklist.id)">Create</button>
        </form>

        <button type="button" class="btn btn-outline-danger" data-toggle="modal"
                :data-target="'#delete-list' + checklist.id">Delete List
        </button>
        <div class="modal" :id="'delete-list' + checklist.id" tabindex="-1" aria-hidden="true">
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
import ListView from "@/components/ListView";

export default {
  name: 'lists-list',
  components: {ListView},
  data() {
    return {
      name: '',
      related_list: null,
    }
  },
  computed: mapGetters(['lists']),
  comments: {
    'list-view': ListView,
  },

  methods: {
    convertDateToTimeAgo(date) {
      return prettydate.format(new Date(date))
    },
    deleteList(list) {
      this.$store.dispatch('deleteList', list)
    },
    changeListState(list, state) {
      this.$store.dispatch('changeCheckListState', {list, state})
    },
    submitForm(event) {
      this.createItem()
      this.name = ''
      this.related_list = null
      event.preventDefault()
    },
    createItem() {
      this.$store.dispatch('createItem', {name: this.name, related_list: this.related_list})
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

i {
  cursor: pointer;
}
</style>
