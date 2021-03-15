import axios from 'axios'

export const HTTP_GET_LISTS = axios.create({
  baseURL: 'http://127.0.0.1:8000/lists/',
})

export const HTTP_GET_ITEMS = axios.create({
  baseURL: 'http://127.0.0.1:8000/items/',
})