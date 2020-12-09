<template>

  <div class="container chat-main bg-purple">
    <div class="side-menu">
      sidemenu
    </div>
    <div class="dialog-view">
      dialog
    </div>
  </div>

</template>

<style>

.chat-main {
  width: 100%;
  height: 100%;
  position: fixed;
  display: flex;
}

.side-menu {
  right: 0px;
  height: 100vh;
  max-width: 15%;
  flex: 0;
  display: flex;
  background: white;
  position: relative;
}

.dialog-view {
  flex-grow: 1;
}

</style>

<script>

</script>
