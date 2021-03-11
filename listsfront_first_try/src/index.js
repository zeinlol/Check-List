// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ListsList from './components/ListsList.vue'

Vue.config.productionTip = false
Vue.component('hello-world')

export default {
  components: {
    ListsList,
  },
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
})
