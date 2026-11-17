<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DesktopPet from './components/DesktopPet.vue'
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'

const route = useRoute()
const showNavbar = computed(() => route.name !== 'login')
const showSidebar = computed(() => route.name !== 'home' && route.name !== 'login')
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
    <div class="app-layout" :class="{ 'has-navbar': showNavbar }">
      <Sidebar v-if="showSidebar" />
      <main class="app-content">
        <router-view />
      </main>
    </div>
    <DesktopPet />
  </div>
</template>

<style>
.app-shell {
  min-height: 100vh;
}

.app-layout {
  display: flex;
  min-height: 100vh;
}

.app-layout.has-navbar {
  padding-top: 34px;
}

.app-content {
  flex: 1;
  min-width: 0;
}
</style>
