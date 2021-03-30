<template>

  <div id="lists" class="col-12">

    <div class="card checklist-item" v-for="item in items" :key="item.id">
      <div class="card-body list-group text-center">
        <h2 class="card-title checklist-title">
          <i class="fa fa-check" aria-hidden="true" v-if="item.done" @click="changeItemState(item, false)"></i>
          <i class="fa fa-square-o" aria-hidden="true" v-else @click="changeItemState(item, true)"></i>
          subtask: {{ item.title }}
        </h2>
        <p class="card-subtitle text-muted">Created: {{ item.date }}</p>
        <p v-if="item.comments.length > 0">Comments</p>
        <p v-else>No Comments</p>
<!--        <div class="card-footer text-muted" style="margin: 5px 0px 5px 0px;" v-if="item.comments.length > 0">-->
<!--          {% for comment in item.comments %}-->
<!--          <div class="comment">-->
<!--            <p class="info">-->
<!--              {{ comment.name }}-->
<!--              {{ comment.created }}-->
<!--            </p>-->
<!--            {{ comment.body }}<br>-->
<!--            {% if comment.photo %}-->
<!--            <img :src="comment.photo.url" class="img-fluid comment-photo"><br>-->
<!--            {% endif %}-->
<!--            {% if comment.file %}-->
<!--            <a :href="comment.file.url" :download="comment.file">{{ comment.file }}</a>-->
<!--            {% endif %}-->
<!--          </div>-->
<!--          {% empty %}-->
<!--          <p>There are no comments.</p>-->
<!--          {% endfor %}-->
<!--        </div>-->
        <p>
          <button class="btn btn-primary" type="button" data-toggle="collapse"
                  :data-target="'#comments_form-' + item.id"
                  aria-expanded="false" aria-controls="collapseExample">
            Add Comment
          </button>
        </p>
        <div class="collapse" :id="'comments_form-' + item.id">
          <div class="card card-body">
            {% if new_comment %}
            <h2>Your comment has been added.</h2>
            {% else %}
            <form action="#" method="post" enctype=multipart/form-data>

<!--              {% csrf_token %}-->
<!--              {{ comment_form.as_p }}-->
<!--              <input type="hidden" name="item_id" :value=" item.id ">-->
<!--              <p><input type="submit" value="Add comment"></p>-->
            </form>
            {% endif %}
          </div>
        </div>
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