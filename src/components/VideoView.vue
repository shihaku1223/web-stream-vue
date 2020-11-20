<template>
  <div>
    <video ref="video" autoplay>
    </video>
  </div>
</template>

<script>

import { getLocalStream } from '@/webrtc'

export default {

  data: () => ({
  }),

  props: ['local'],

  methods: {
    setLocalStream() {
      getLocalStream().then((stream) => {
        console.log('Got local video stream.')
        this.$refs.video.srcObject = stream
      })
    }
  },

  created() {
  },

  mounted() {
    if(this.local == "true") {
      this.setLocalStream()
    }
  },
}

</script>
