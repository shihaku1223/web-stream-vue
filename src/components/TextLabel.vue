<template>
  <div class="h2 ma2 hk-label">
    {{ text }}
  </div>
</template>

<style scoped>

</style>

<script>

export default {
  name: 'text-label',

  data: () => ({
  }),

  props: {
    text: String,
  },

  computed: {
  },

  mounted() {
    console.log(this.text)
  },
}

</script>
