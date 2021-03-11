import {HTTP_GET_ITEMS, HTTP_GET_LISTS} from './common'

export const CheckList = {
  create(config) {
    return HTTP_GET_LISTS.post('/lists/', config).then(response => {
      return response.data
    })
  },
  delete(checklist) {
    return HTTP_GET_LISTS.delete(`/lists/${checklist.id}/`)
  },
  list() {
    return HTTP_GET_LISTS.get('/lists/').then(response => {
      return response.data
    })
  },
}

export const ListItems = {
  create(config) {
    return HTTP_GET_ITEMS.post('', config).then(response => {
      return response.data
    })
  },
  delete(list_item) {
    return HTTP_GET_ITEMS.delete(`${list_item.id}/`)
  },
  items() {
    return HTTP_GET_ITEMS.get('').then(response => {
      return response.data
    })
  },
}

