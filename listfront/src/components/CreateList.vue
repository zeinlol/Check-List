<template lang="pug">
  form.form-horizontal(@submit="submitForm")
    .form-group
      .col-3
        label.form-label Title
      .col-9
        input.form-input(type="text" v-model="name" placeholder="Type checklist title...")
    .form-group
      .col-3
        label.form-label Body
      .col-9
        textarea.form-input(v-model="description" rows=8 placeholder="Type description...")
    .form-group
      .col-3
      .col-9
        button.btn.btn-primary(type="submit") Create





</template>

<script>
export default {
  name: 'create-list',
  data() {
    return {
      'name': '',
      'description': '',
    }
  },
  methods: {
    submitForm(event) {
      this.createList()
      this.name = ''
      this.description = ''
      event.preventDefault()
    },
    createList() {
      this.$store.dispatch('createList', {name: this.name, description: this.description})
    },
  },
}
</script>

<style>
</style>


