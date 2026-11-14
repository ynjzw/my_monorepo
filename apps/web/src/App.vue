<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DesktopPet from './components/DesktopPet.vue'
import Navbar from './components/Navbar.vue'

const route = useRoute()
const showNavbar = computed(() => route.name !== 'login')
const savedTheme = localStorage.getItem('theme')
const theme = ref(
  savedTheme === 'light' || savedTheme === 'dark'
    ? savedTheme
    : window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light'
)

watch(theme, (value) => {
  document.documentElement.dataset.theme = value
  localStorage.setItem('theme', value)
}, { immediate: true })

const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
}
</script>

<template>
  <div class="app-shell">
    <Navbar v-if="showNavbar" :theme="theme" @toggle-theme="toggleTheme" />
    <main class="app-content" :class="{ 'has-navbar': showNavbar }">
      <router-view />
    </main>
    <DesktopPet />
  </div>
</template>

<style>
.app-shell {
  display: contents;
}

.app-content.has-navbar {
  padding-top: 34px;
}
</style>
