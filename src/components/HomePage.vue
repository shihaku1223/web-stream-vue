<template>
  <div>
    Hello
    <click-button text="Connect"
      @click="connect"
    />
    <div class="hk-label">{{ peerId }}</div>
    <video-view ref="localVideo" local="false"/>
    <video-view ref="remoteVideo"/>
  </div>
</template>

<script>

import {
  getLocalStream,
  connectToSignalingServer,
  getPeerId,
} from '@/webrtc'

import VideoView from '@/components/VideoView'
import ClickButton from '@/components/ClickButton'

export default {

  data: () => ({
    peerId: '',
    signalingServerAddress: "ws://localhost:8443"
  }),

  methods: {
    connect() {
      connectToSignalingServer(this.signalingServerAddress)
    },
  },

  created() {
    this.peerId = getPeerId()
  },

  components: {
    VideoView,
    ClickButton,
  }
}

</script>
