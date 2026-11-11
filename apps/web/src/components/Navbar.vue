<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  sidebarCollapsed: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggle-sidebar'])
</script>

<template>
  <header class="navbar">
    <button
      class="menu-toggle"
      type="button"
      aria-label="展开或收起侧边栏"
      :aria-expanded="!sidebarCollapsed"
      @click="emit('toggle-sidebar')"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>

    <RouterLink class="brand" :to="{ name: 'home' }">
      <span class="brand-mark" aria-hidden="true">天</span>
      <span class="brand-name">天人图</span>
    </RouterLink>

    <nav class="top-links" aria-label="顶部导航">
      <RouterLink :to="{ name: 'home' }">首页</RouterLink>
      <RouterLink :to="{ name: 'supply_chain' }">供应链分析</RouterLink>
      <RouterLink :to="{ name: 'dynamic_graph' }">知识图谱</RouterLink>
    </nav>

    <div class="navbar-status">
      <span class="status-dot"></span>
      <span>数据工作台</span>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  height: 68px;
  padding: 0 28px;
  border-bottom: 1px solid #e8edf3;
  background: #fff;
  color: #172033;
}

.menu-toggle {
  display: grid;
  gap: 4px;
  width: 36px;
  height: 36px;
  margin-right: 16px;
  padding: 10px 9px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
}

.menu-toggle:hover {
  background: #f1f5f9;
}

.menu-toggle span {
  display: block;
  height: 2px;
  border-radius: 2px;
  background: #526174;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: inherit;
  font-size: 17px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
}

.brand-mark {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
  font-size: 16px;
}

.top-links {
  display: flex;
  align-items: center;
  gap: 30px;
  height: 100%;
  margin-left: 52px;
}

.top-links a {
  display: inline-flex;
  align-items: center;
  height: 100%;
  border-bottom: 2px solid transparent;
  color: #64748b;
  font-size: 14px;
  text-decoration: none;
  transition: color 0.18s ease, border-color 0.18s ease;
}

.top-links a:hover,
.top-links a.router-link-active {
  border-bottom-color: #2563eb;
  color: #1d4ed8;
}

.navbar-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  color: #64748b;
  font-size: 13px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 3px #dcfce7;
}

@media (max-width: 700px) {
  .navbar {
    height: 60px;
    padding: 0 14px;
  }

  .menu-toggle {
    margin-right: 10px;
  }

  .top-links,
  .navbar-status {
    display: none;
  }
}
</style>
