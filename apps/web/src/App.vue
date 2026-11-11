<script setup>
import DesktopPet from './components/DesktopPet.vue'
</script>

<template>
  <div class="app-shell">
    <router-view />
    <DesktopPet />
  </div>
</template>

<style>
.app-shell {
  display: contents;
}
</style>

<style scoped>

</style>
