<template>
  <div>
    <notes-nav
        selected="v-checklists"
        :project-id="$route.params.id"
        :project-name="$route.params.projectName"
    />
    <div class="show-support-content">
      <div class="container">
        <div class="row">
          <div class="col col-12">
            <div class="support-ticket">
              <div class="row">
                <div class="col col-12">
                  <h3 class="subtitle">
                    Checklists
                  </h3>
                  <p class="subdescription">
                    New Checklists system.
                  </p>
                  <!-- if checklist exist -->
                  <div v-if="checklists.length > 0">
                    <div v-for="checklist in checklists">
                      <b-card :id="'checklist-data' + checklist.id" bg-variant="light">
                        <h5 slot="header">
                          <i class="fa fa-check" aria-hidden="true" v-if="checklist.done"
                             @click="updateChecklistData(checklist, 'changeStateChecklist',false)"></i>
                          <i class="fa fa-square-o" aria-hidden="true" v-else
                             @click="updateChecklistData(checklist, 'changeStateChecklist',true)"></i>
                          <span @click="showHideChecklistDetails(checklist.id)">{{ checklist.name }}</span>
                          <a href="javascript:void(0)"
                             title="Edit Checklist"
                             @click="showChecklistEditor(checklist.id)"
                          >
                            <i class="fa fa-edit"></i>
                          </a>
                        </h5>
                        <b-card-body :id="'checklist-body' + checklist.id" class="hidden-card">
                          <b-card-text>
                            <p v-html="checklist.description">
                              {{ checklist.description }}
                            </p>
                            <hr>
                          </b-card-text>
                          <div v-if="checklist.list_items.length > 0">
                            <b-card :id="'item' + checklist.id + item.id" v-for="item in checklist.list_items">
                              <b-card-text class="item-name">
                                <p v-if="item.done">
                                  <i class="fa fa-check" aria-hidden="true"
                                     @click="updateChecklistData(item,'changeStateItem',false)"></i>
                                  <span class="completed">{{ item.title }}</span>

                                  <i class="fa fa-times" aria-hidden="true"
                                     @click="deleteItem(item.id, checklist.id)"></i>
                                </p>
                                <p v-else>
                                  <i class="fa fa-square-o" aria-hidden="true"
                                     @click="updateChecklistData(item,'changeStateItem',true)"></i>
                                  {{ item.title }}

                                  <i class="fa fa-times" aria-hidden="true"
                                     @click="deleteItem(item.id, checklist.id)"></i>
                                </p>
                              </b-card-text>
                              <!--  Comments  -->
                              <a href="javascript:void(0)"
                                 :id="'show-comment-btn-' + item.id"
                                 title="Show Comments"
                                 @click="showItemsComments(item.id)"><i>show details</i></a>
                              <div :id="'item-comment-' + item.id" class="hidden-card">
                                <a href="javascript:void(0)"
                                   title="Hide Comments"
                                   @click="hideItemsComments(item.id)"><i>hide details</i></a>
                                <div v-if="item.comments.length > 0">
                                  <b-card v-for="comment in item.comments">
                                    <p class="info">
                                      {{ comment.user }}
                                      {{ comment.created }}
                                    </p>
                                    {{ comment.body }}<br>
                                  </b-card>
                                </div>
                                <b-card v-else>
                                  <p>No comments yet</p>
                                </b-card>
                              </div>
                            </b-card>
                          </div>
                          <b-card-text v-else><p>Checklist is empty!</p></b-card-text>
                          <!-- add new item to the checklist --> <!-- ADD 2 Elements (why?)!!!!!! -->
                          <b-form @submit.prevent="newListItem(checklist.id)">
                            <b-form-group
                                label="Write new Item to Checklist"
                                :label-for="'new-item-name' + checklist.id"
                            >
                              <input
                                  :id="'new-item-name' + checklist.id"
                                  v-on:keyup.enter="newListItem(checklist.id)"
                                  v-model="newListItemName"></input>
                            </b-form-group>
                          </b-form>
                        </b-card-body>
                      </b-card>
                      <!-- edit checklist form -->   <!-- NOT FINISHED!!!!!! -->
                      <b-card :id="'checklist-editor' + checklist.id" class="hidden-card">
                        <b-form @submit.prevent="updateChecklistData(checklist, 'update')">
                          <b-form-group
                              :label="'Edit checklist info for: ' + checklist.name"
                              label-for="checklist-name-input">
                            <input label="Name" :placeholder="checklist.name" v-model="checklistNewName">
                          </b-form-group>
                          <b-form-group
                              id="note-grp"
                              label="Description"
                              label-for="checklist-description-edit"
                          >

                            <quill-editor
                                id="checklist-description-edit"
                                ref="notesEditor"
                                :name="'description-edit' + checklist.id"
                                v-model="EditDescription"
                                :options="quillOpts"
                            />
                          </b-form-group>
                          <b-form-group
                              id="is-done-radio"
                              label="Change Status"
                              label-for="attack-is-done"
                          >
                            <b-form-radio-group
                                v-model="isDoneStatus"
                                :options="isDoneOpts"
                                buttons
                                size="sm"
                                name="is-done-radios-btn-group"
                            />
                          </b-form-group>
                          <input type="hidden" :value="checklist.id" :name="'checklistId'">
                          <hr>
                          <div
                              v-if="!submitInProgress"
                              aria-label="Form controls toolbar"
                          >
                            <b-button
                                @click="hideChecklistEditor(checklist.id)"
                            >
                              Undo
                            </b-button>
                            <b-button
                                type="submit"
                                variant="primary"
                            >
                              Update Checklist
                            </b-button>
                            <!--<b-button
                                variant="danger"
                                @click="showDeleteChecklistModal(checklist.id)"
                            >
                              Delete
                            </b-button>-->
                          </div>
                          <b-button-toolbar v-else>
                            <b-button-group size="sm">
                              <b-button variant="primary" disabled>
                                <b-spinner small />
                                Updating...
                              </b-button>
                            </b-button-group>
                          </b-button-toolbar>
                          <hr>
                          <!--<b-form-group size="sm" class="mx-1">
                            //[notes_report_generate]-[BEGIN]
                            <audit-scope-i-create-report-i-button :note-id="noteId" button-text="Export checklist" />
                            //[notes_report_generate]-[END]
                          </b-form-group>-->
                        </b-form>
                      </b-card>
                    </div>
                  </div>
                  <!--                  <b-card v-else><h5>No Checklists</h5></b-card>-->
                  <!-- if no checklists -->
                  <b-card id="attack-checklist" bg-variant="light" v-else><h5>No checklists yet</h5></b-card>
                  <!-- Create new checklist -->
                  <b-card>
                    <h3 class="subtitle">
                      Create new Checklist
                    </h3>
                    <b-form @submit.prevent="createChecklist">
                      <b-form-group
                          label="Checklist name"
                          label-for="checklist-name-input"
                      >
                        <input
                            id="checklist-name-input"
                            ref="notesEditor"
                            v-model="checklistName"
                        />
                      </b-form-group>
                      <b-form-group
                          label="Checklist description"
                          label-for="checklist-edit-description-input"
                      >
                        <quill-editor
                            id="checklist-edit-description-input"
                            ref="notesEditor"
                            v-model="checklistDescription"
                            :options="quillOpts"
                        />
                      </b-form-group>
                      <b-form-group
                          label="Chooze Status"
                          label-for="attack-is-done"
                      >
                        <b-form-radio-group
                            v-model="isDoneStatus"
                            :options="isDoneOpts"
                            buttons
                            size="sm"
                            name="is-done-radios-btn-group"
                        />
                      </b-form-group>
                      <hr>
                      <b-button-toolbar
                          v-if="!submitInProgress"
                          aria-label="Form controls toolbar"
                      >
                        <b-button
                            type="submit"
                            variant="primary"
                            @submit="createChecklist"
                        >
                          Create Checklist
                        </b-button>
                      </b-button-toolbar>
                      <b-button-toolbar v-else>
                        <b-button-group size="sm">
                          <b-button variant="primary" disabled>
                            <b-spinner small />
                            Updating...
                          </b-button>
                        </b-button-group>
                      </b-button-toolbar>
                    </b-form>

                  </b-card>
                  <!-- Delete modal -->
                  <b-modal id="modal-delete"
                           ref='deleteCheckListModal'
                           hide-footer
                           hide-header
                  >
                    <div class="modal-heading">
                      <h4>Delete this checklist</h4>
                      <button class="close-modal" @click="hideDeleteChecklistModal"></button>
                    </div>
                    <div class="modal-controls">
                      <p>Are you sure you want to delete this checklist?</p>
                      <div class="show-btns">
                        <button class="red-btn" @click="deleteChecklist">
                          Yes
                        </button>
                        <button class="blue-btn" @click="hideDeleteChecklistModal">
                          No
                        </button>
                      </div>
                    </div>
                  </b-modal>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>{

<script>
import {waitFor} from 'vue-wait'
import {showToast, VARIANT} from '~/components/audit/misc/unloggable-notifications'
import notesMixin from '~/mixins/notes-mixin'
import {UserIAvatar, UserIName} from '@/components/user'

const SUBMIT_DATA = 'SUBMIT_DATA'

export default {
  name: 'v-checklists',
  mixins: [notesMixin],
  params: {
    id: {
      type: [Number, String],
    },
    projectName: {
      type: String,
    },
  },
  user: {
    avatar: [UserIAvatar],
    name: [UserIName],
  },
  data: () => {
    return {
      isDoneValue: null,
      checklistDescription: null,
      EditDescription: 'test remaking',
      checklistName: null,
      checklistNewName: null,
      newListItemName: null,
      listId: null,
      templateId: 0,
      isDoneOpts: [
        {value: true, text: 'Done'},
        {value: false, text: 'In work'},
      ],
    }
  },
  computed: {
    checklists() {
      return this.$store.getters['notes/getCheckLists']
    },
    isDoneStatus: {
      get: function () {
        return this.checklists.done
      },
      set: function (newValue) {
        if (newValue !== null) {
          this.isDoneValue = newValue
        } else {
          this.isDoneValue = this.checklists.done
        }
      },
    },
    templates() {
      return this.$store.getters['notes/TemplateCheckLists']
    },
    selectSize() {
      if (this.templates.length <= 7) {
        return this.templates.length
      } else {
        return 7
      }
    },
    template() {
      console.log(this.templates.find(el => el.id === this.templateId))
      return this.templates.find(el => el.id === this.templateId)
    },
  },
  methods: {
    makeChecklistUpdateData() {
      return {
        name: this.checklistNewName,
        description: this.EditDescription,
        parent_project: this.$route.params.id,
        done: this.isDoneValue,
      }
    },
    async updateChecklistData(target, action, data = '') {
      let targetId = target.id
      if (action === 'update')
        data = this.makeChecklistUpdateData()
      target.name = data.name
      target.description = data.description
      target.done = data.done
      try {
        this.submitInProgress = true
        console.log('here update list data')
        console.log({targetId, action, data})
        let resp = await this.$store.dispatch('notes/updateCheckListData', {targetId, action, data})
        target.name = resp.name
        target.description = resp.description
        if (action === 'changeStateChecklist' || action === 'changeStateItem')
          console.log('change state')
        console.log(target)
        console.log(data)
        target.done = data
        this.makeNotification(resp)
        this.submitInProgress = false
        // console.info('[ALL OK]', resp)
      } catch (err) {
        this.makeNotification()
        console.error('[UPDATE CHECKLIST ERROR]', err)
        this.submitInProgress = false
      }
    },
    makeFormNewChecklist() {
      return {
        name: this.checklistName,
        description: this.checklistDescription,
        parent_project: this.$route.params.id,
        done: this.isDoneValue,
        list_items: [],
      }
    },
    createChecklist: waitFor(SUBMIT_DATA, async function () {
      let data = this.makeFormNewChecklist()
      try {
        this.submitInProgress = true
        console.log('create checklist data: ')
        console.log(data)
        const resp = await this.$store.dispatch('notes/createNewChecklist', {payload: data})
        this.makeNotification(resp)
        this.submitInProgress = false
        console.info('[ALL OK]', resp)
      } catch (err) {
        this.makeNotification()
        console.error('[CREATE CHECKLIST ERROR]', err)
        this.submitInProgress = false
      }
    }),
    prepareFormData() {
      return {
        name: this.checklistName,
        description: this.checklistDescription,
        parent_project: this.$route.params.id,
        done: this.isDoneValue,
      }
    },
    createTemplateChecklist: waitFor(SUBMIT_DATA, async function () {
      let data = this.prepareFormData()
      // [post_request]-[BEGIN]
      try {
        this.submitInProgress = true // disable buttons
        const resp = await this.$store.dispatch('notes/createTemplateChecklist', {payload: data})
        if (this.files) {
          await this.submitAttachments(resp)
        }
        this.resetFilesAndForm()
        this.submitInProgress = false // enable buttons
        return resp
      } catch (err) {
        this.makeNotification()
        console.error('[ERROR SUBMIT NOTE] ', err)
        this.submitInProgress = false
      }
      // [post_request]-[END]
    }),
    newListItemForm() {
      return {
        title: this.newListItemName,
      }
    },
    async newListItem(listId) {
      console.log('Add new Checklist Item')
      let data = {
        title: this.newListItemName,
        related_list: listId,
        'comments': [],
      }
      try {
        this.submitInProgress = true
        console.log('create ListItem data: ')
        console.log(data)
        const resp = await this.$store.dispatch('notes/createListItem', {payload: data})
        console.log('newItem')
        console.log(this.checklists.find(el => el.id === listId))
        this.checklists.find(el => el.id === listId).list_items.push(resp)
        this.makeNotification(resp)
        this.submitInProgress = false
        console.info('[ALL OK]', resp)
      } catch (err) {
        this.makeNotification()
        console.error('[CREATE LIST ITEM ERROR]', err)
        this.submitInProgress = false
      }
    },
    async deleteItem(itemId, listId) {
      try {
        this.submitInProgress = true
        document.getElementById('item' + listId + itemId).remove()
        const resp = await this.$store.dispatch('notes/deleteItem', itemId)
        // this.makeNotification(resp)
        this.submitInProgress = false
            // console.info('[ALL OK]', resp)
            / console.info('[DELETE SUCCESS]')

      } catch (err) {
        this.makeNotification()
        console.error('[DELETE LIST ITEM ERROR]', err)
        // this.submitInProgress = false
      }
    },
    async deleteChecklist(listId) {
      let payload = {
        action: 'delete',
        listId: listId,
      }
      try {
        this.submitInProgress = true
        // document.getElementById('item' + listId + itemId).remove()
        await this.$store.dispatch('notes/deleteChecklist', payload)
        // this.makeNotification(resp)
        this.submitInProgress = false
            // console.info('[ALL OK]', resp)
            / console.info('[DELETE SUCCESS]')

      } catch (err) {
        this.makeNotification()
        console.error('[DELETE CHECKLIST ERROR]', err)
        // this.submitInProgress = false
      }
    },
    makeNotification(resp = null) {
      let opts = {}
      if (resp === null) {
        opts.title = 'Error creating note'
        opts.variant = VARIANT.DANGER
        opts.msg = 'Please try again later'
        opts.autoHideDelay = 5000
      } else {
        let linkData = {}
        let target = {
          name: 'notes-id-projectName-notes-noteId',
          params: {noteId: resp.id, projectName: this.$route.params.projectName},
        }
        linkData.href = $nuxt.$router.resolve(target).href
        opts.title = `Note "${resp.name}" created successfully`
        opts.variant = VARIANT.SUCCESS
        opts.msg = `Go to note "${resp.name}"`
        opts.autoHideDelay = 5000
        opts.linkData = linkData
        opts.role = true
      }
      showToast(opts)
    },
    showDeleteChecklistModal(id) {
      // document.getElementById('deleteCheckListModal' + id).show()
      this.$refs.deleteCheckListModal.show()
      // this.$emit('remove', this.item.id);
    },
    hideDeleteChecklistModal(id) {
      // document.getElementById('deleteCheckListModal' + id).hide()
      this.$refs.deleteCheckListModal.hide()
    },
    showChecklistEditor(listId) {
      let cardEl = document.getElementById('checklist-data' + listId)
      let cardEditorEl = document.getElementById('checklist-editor' + listId)

      if (!cardEl.classList.contains('hidden-card') && cardEditorEl.classList.contains('hidden-card')) {
        console.info('Hide description')
        cardEl.classList.add('hidden-card')
        cardEditorEl.classList.remove('hidden-card')
      }
    },
    hideChecklistEditor(listId) {
      let cardEl = document.getElementById('checklist-data' + listId)
      let cardEditorEl = document.getElementById('checklist-editor' + listId)

      if (cardEl.classList.contains('hidden-card') && !cardEditorEl.classList.contains('hidden-card')) {
        console.info('Show description')
        cardEl.classList.remove('hidden-card')
        cardEditorEl.classList.add('hidden-card')
      }
    },
    showItemsComments(itemId) {
      let commentsEl = document.getElementById('item-comment-' + itemId)
      let btnEl = document.getElementById('show-comment-btn-' + itemId)
      if (commentsEl.classList.contains('hidden-card')) {
        commentsEl.classList.remove('hidden-card')
        btnEl.classList.add('hidden-card')
      }
    },
    hideItemsComments(itemId) {
      let commentsEl = document.getElementById('item-comment-' + itemId)
      let btnEl = document.getElementById('show-comment-btn-' + itemId)
      if (!commentsEl.classList.contains('hidden-card')) {
        commentsEl.classList.add('hidden-card')
        btnEl.classList.remove('hidden-card')
      }
    },
    showHideChecklistDetails(itemId) {
      let detailsEl = document.getElementById('checklist-body' + itemId)
      if (detailsEl.classList.contains('hidden-card')) {
        detailsEl.classList.remove('hidden-card')
      } else if (!detailsEl.classList.contains('hidden-card')) {
        detailsEl.classList.add('hidden-card')
      }
    },
  },
  async fetch({store, params}) {
    let projectId = params.id
    await store.dispatch('notes/fetchWeaknesses')
    await store.dispatch('notes/getCheckLists', projectId)
    await store.dispatch('notes/TemplateCheckLists')
  },
}

</script>

<style scoped>
/deep/ div.quill-editor div.ql-toolbar.ql-snow {
  border-radius: 0.25rem .25rem 0 0;
}

/deep/ div.quill-editor div.ql-container.ql-snow {
  border-radius: 0 0 .25rem .25rem;
}

.hidden-card {
  display: none;
}

i.fa {
  cursor: pointer;
}

.completed {
  text-decoration: line-through;
}
</style>
