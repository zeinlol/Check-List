<template>
  <div id="app">

    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="text-center">
            <h2>Create note</h2>
          </div>
        </div>
        <div class="col-12">
          <create-list></create-list>
        </div>
        <div class="col-12 text-center">
          <h2>List of notes</h2>
        </div>

        <div class="col-12">
          <lists-list></lists-list>
        </div>
        <div class="col-12 text-center">
          <h2>List of ListItems</h2>
        </div>

        <div class="col-12">
          <list-view></list-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CreateList from './components/CreateList'
import CheckList from './components/CheckList'
import ListView from '@/components/ListView'

export default {
  name: 'App',
  components: {
    'create-list': CreateList,
    'lists-list': CheckList,
    'list-view': ListView,
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
