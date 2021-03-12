import {HTTP_GET_ITEMS, HTTP_GET_LISTS} from './common'

export const CheckList = {
  create(config) {
    console.log('CREATE LIST')
    return HTTP_GET_LISTS.post('', config).then(response => {
      return response.data
    })
  },
  delete(checklist) {
    return HTTP_GET_LISTS.delete(`${checklist.id}/`)
  },
  list() {
    return HTTP_GET_LISTS.get('').then(response => {
      console.log(response.data)
      return response.data
    })
  },
  changeState(listdata) {
    console.log(listdata)
    return HTTP_GET_LISTS.patch(`${listdata.list.id}/`, listdata.list.completed = listdata.state)
  },
  goTo(config) {
    return HTTP_GET_ITEMS.get('', config).then(response => {
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

