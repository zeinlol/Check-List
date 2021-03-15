import Vue from 'vue'
import Vuex from 'vuex'
import {CheckList, ListItems} from '@/api/checklists_main'
import {ADD_LIST, REMOVE_LIST, SET_LISTS, ADD_ITEM, REMOVE_ITEM, SET_ITEMS, CHANGE_STATE} from './mutation-types.js'

Vue.use(Vuex)

const state = {
  lists: {},
  items: {},
}

const getters = {
  lists: state => state.lists,
  items: state => state.items,
}

const mutations = {
  [ADD_LIST](state, list) {
    state.lists = {list, ...state.lists}
  },
  [REMOVE_LIST](state, {id}) {
    state.lists = state.lists.filter(list => {
      return list.id !== id
    })
  },
  [CHANGE_STATE](state, listdata) {
    state.list.done = listdata.state
  },
  [SET_LISTS](state, {lists}) {
    state.lists = lists
  },
  [ADD_ITEM](state, items) {
    state.items = {items, ...state.items}
  },
  [REMOVE_ITEM](state, {id}) {
    state.items = state.items.filter(items => {
      return items.id !== id
    })
  },
  [SET_ITEMS](state, {items}) {
    state.items = items
  },
}

const actions = {
  createList({commit}, listData) {
    CheckList.create(listData).then(list => {
      commit(ADD_LIST, list)
    })
  },
  deleteList({commit}, list) {
    CheckList.delete(list).then(response => {
      commit(REMOVE_LIST, list, response)
    })
  },
  getLists({commit}) {
    CheckList.list().then(lists => {
      commit(SET_LISTS, {lists})
    })
  },
  changeCheckListState({commit}, listdata) {
    CheckList.changeState(listdata).then(listdata => {
      commit(CHANGE_STATE, listdata)
    })
  },
  createItem({commit}, itemData) {
    console.log(itemData)
    ListItems.create(itemData).then(item => {
      commit(ADD_ITEM, item)
    })
  },
  deleteItem({commit}, item) {
    ListItems.delete(item).then(response => {
      commit(REMOVE_ITEM, item, response)
    })
  },
  getItems({commit}, list_id) {
    ListItems.items(list_id).then(items => {
      commit(SET_ITEMS, {items})
    })
  },
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
})
