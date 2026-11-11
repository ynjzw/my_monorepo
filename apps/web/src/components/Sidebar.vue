<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  collapsed: {
    type: Boolean,
    default: false
  }
})

const navigationGroups = [
  {
    title: '工作台',
    items: [
      { label: '总览', route: 'home', icon: '⌂' },
      { label: '供应链分析', route: 'supply_chain', icon: '⇄' }
    ]
  },
  {
    title: '数据分析',
    items: [
      { label: '知识图谱', route: 'dynamic_graph', icon: '◉' },
      { label: '资金流向', route: 'cash_flow', icon: '↗' },
      { label: '行业板块', route: 'stock_sector', icon: '▦' },
      { label: '资源与愿望', route: 'skill_resource_wish', icon: '◇' }
    ]
  }
]
</script>

<template>
  <aside class="sidebar" :class="{ 'is-collapsed': collapsed }">
    <nav aria-label="侧边导航">
      <section v-for="group in navigationGroups" :key="group.title" class="nav-group">
        <h2 v-if="!collapsed" class="group-title">{{ group.title }}</h2>
        <RouterLink
          v-for="item in group.items"
          :key="item.route"
          class="nav-item"
          :to="{ name: item.route }"
          :title="collapsed ? item.label : undefined"
        >
          <span class="nav-icon" aria-hidden="true">{{ item.icon }}</span>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </section>
    </nav>

    <div v-if="!collapsed" class="sidebar-footer">
      <span class="footer-avatar">数</span>
      <span class="footer-copy">
        <strong>数据分析平台</strong>
        <small>供应链工作区</small>
      </span>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex: 0 0 236px;
  flex-direction: column;
  justify-content: space-between;
  width: 236px;
  padding: 24px 14px 16px;
  border-right: 1px solid #e8edf3;
  background: #fff;
  transition: width 0.2s ease, flex-basis 0.2s ease, padding 0.2s ease;
}

.sidebar.is-collapsed {
  flex-basis: 72px;
  width: 72px;
  padding-right: 10px;
  padding-left: 10px;
}

.nav-group + .nav-group {
  margin-top: 30px;
}

.group-title {
  margin: 0 0 10px 12px;
  color: #94a3b8;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 13px;
  min-height: 44px;
  margin: 3px 0;
  padding: 0 12px;
  border-radius: 8px;
  color: #64748b;
  font-size: 14px;
  text-decoration: none;
  transition: background 0.18s ease, color 0.18s ease;
}

.is-collapsed .nav-item {
  justify-content: center;
  padding: 0;
}

.nav-item:hover {
  background: #f5f8fc;
  color: #1d4ed8;
}

.nav-item.router-link-active {
  background: #eff6ff;
  color: #1d4ed8;
  font-weight: 600;
}

.nav-icon {
  display: inline-grid;
  flex: 0 0 20px;
  width: 20px;
  place-items: center;
  color: currentColor;
  font-size: 19px;
  line-height: 1;
}

.nav-label {
  overflow: hidden;
  white-space: nowrap;
}

.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 8px 0;
  border-top: 1px solid #eef2f6;
}

.footer-avatar {
  display: grid;
  flex: 0 0 34px;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 10px;
  background: #e0eaff;
  color: #2563eb;
  font-size: 14px;
}

.footer-copy {
  display: grid;
  gap: 2px;
  min-width: 0;
}

.footer-copy strong {
  color: #334155;
  font-size: 12px;
}

.footer-copy small {
  color: #94a3b8;
  font-size: 11px;
}

@media (max-width: 700px) {
  .sidebar {
    position: fixed;
    z-index: 4;
    top: 60px;
    bottom: 0;
    left: 0;
    width: 236px;
    box-shadow: 12px 0 24px rgb(15 23 42 / 10%);
  }

  .sidebar.is-collapsed {
    flex-basis: 0;
    width: 0;
    min-width: 0;
    padding-right: 0;
    padding-left: 0;
    border: 0;
    overflow: hidden;
  }
}
</style>
