<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  theme: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['toggle-theme'])
</script>

<template>
  <header class="navbar">
    <RouterLink class="brand" :to="{ name: 'home' }">
      <span class="brand-mark" aria-hidden="true">天</span>
      <span class="brand-name">天人图</span>
    </RouterLink>

    <nav class="top-links" aria-label="顶部导航">
      <RouterLink :to="{ name: 'home' }">首页</RouterLink>
      <RouterLink :to="{ name: 'supply_chain' }">供应链分析</RouterLink>
      <RouterLink :to="{ name: 'dynamic_graph' }">知识图谱</RouterLink>
    </nav>

    <div class="navbar-actions">
      <button
        class="theme-toggle"
        type="button"
        :aria-pressed="theme === 'dark'"
        :aria-label="theme === 'dark' ? '切换到明亮主题' : '切换到暗色主题'"
        :title="theme === 'dark' ? '切换到明亮主题' : '切换到暗色主题'"
        @click="emit('toggle-theme')"
      >
        <span aria-hidden="true">{{ theme === 'dark' ? '☀' : '☾' }}</span>
      </button>
      <RouterLink class="login-link" :to="{ name: 'login' }">登录</RouterLink>
      <RouterLink class="register-link" :to="{ name: 'login', query: { mode: 'register' } }">
        注册
      </RouterLink>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: fixed;
  z-index: 30;
  inset: 0 0 auto;
  display: flex;
  align-items: center;
  height: 34px;
  padding: 0 20px;
  border-bottom: 1px solid #e8edf3;
  background: #fff;
  color: #172033;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: inherit;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
}

.brand-mark {
  display: grid;
  width: 24px;
  height: 24px;
  place-items: center;
  border-radius: 7px;
  background: #2563eb;
  color: #fff;
  font-size: 12px;
}

.top-links {
  display: flex;
  align-items: center;
  gap: 24px;
  height: 100%;
  margin-left: 36px;
}

.top-links a {
  display: inline-flex;
  align-items: center;
  height: 100%;
  border-bottom: 2px solid transparent;
  color: #64748b;
  font-size: 11px;
  text-decoration: none;
  transition: color 0.18s ease, border-color 0.18s ease;
}

.top-links a:hover,
.top-links a.router-link-active {
  border-bottom-color: #2563eb;
  color: #1d4ed8;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.theme-toggle {
  display: inline-grid;
  width: 26px;
  height: 26px;
  place-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: transparent;
  color: #526174;
  cursor: pointer;
  font: inherit;
  font-size: 15px;
  line-height: 1;
  transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}

.theme-toggle:hover {
  border-color: #bfdbfe;
  background: #eff6ff;
  color: #1d4ed8;
}

.login-link,
.register-link {
  display: inline-flex;
  min-height: 24px;
  align-items: center;
  justify-content: center;
  color: #526174;
  font-size: 11px;
  text-decoration: none;
}

.login-link:hover {
  color: #1d4ed8;
}

.register-link {
  min-width: 46px;
  padding: 0 10px;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  transition: background 0.18s ease;
}

.register-link:hover {
  background: #1d4ed8;
}

@media (max-width: 700px) {
  .navbar {
    padding: 0 12px;
  }

  .top-links {
    gap: 12px;
    margin-left: 16px;
  }

  .top-links a {
    font-size: 10px;
  }
}

@media (max-width: 420px) {
  .top-links {
    display: none;
  }
}

:global(:root[data-theme='dark']) .navbar {
  border-bottom-color: #303747;
  background: #171b26;
  color: #e6eaf2;
}

:global(:root[data-theme='dark']) .top-links a {
  color: #a4aec0;
}

:global(:root[data-theme='dark']) .top-links a:hover,
:global(:root[data-theme='dark']) .top-links a.router-link-active {
  border-bottom-color: #8b9cff;
  color: #b6c1ff;
}

:global(:root[data-theme='dark']) .theme-toggle {
  border-color: #3a4355;
  color: #c1c8d6;
}

:global(:root[data-theme='dark']) .theme-toggle:hover {
  border-color: #6479ea;
  background: #252d40;
  color: #b6c1ff;
}

:global(:root[data-theme='dark']) .login-link {
  color: #c1c8d6;
}

:global(:root[data-theme='dark']) .login-link:hover {
  color: #b6c1ff;
}

:global(:root[data-theme='dark']) .register-link {
  background: #5267d8;
}

:global(:root[data-theme='dark']) .register-link:hover {
  background: #6479ea;
}

</style>
