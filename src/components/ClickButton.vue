<template>
  <button class="hk-button--secondary"
    @click="onClick"
  >
    {{ text }}
  </button>
</template>

<style scoped>

</style>

<script>

export default {
  name: 'click-button',

  props: {
    text: String,
  },

  methods: {
    onClick(e) {
      this.$emit('click')
      e.preventDefault()
    }
  }
}

</script>
