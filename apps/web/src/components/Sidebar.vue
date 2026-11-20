<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const props = defineProps({
  context: {
    type: String,
    required: true,
    validator: (value) => ['person', 'world'].includes(value)
  }
})
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'jack',
  password: '',
  database: 'graph',
  waitForConnections: true,
  connectionLimit: 10,
});

// 查询
async function getSubjects() {
  const [rows] = await pool.query('SELECT * FROM subjects');
  return rows;
}
async function getIndustry() {
  const [rows] = await pool.query('SELECT * FROM industry where type="门类"');
  return rows;
}
const route = useRoute()

const sections = computed(() => props.context === 'person'
  ? [
      { label: '总览', route: 'person' },
      { label: '人际网络/各元素占比', route: 'person' },
      { label: '生理' },
      { label: '心理' },
      { label: '收入/支出/储蓄' }
    ]
  : [
      { label: '总览', route: 'world', icon: '⌂' },
      { label: '人类足迹', route: 'world' },
      { label: '产业' },
      { label: '专业' },
      { label: '社会通识', route: '' },
      { label: '供应链分析', route: 'supply_chain', icon: '⇄' },
      { label: '知识图谱', route: 'dynamic_graph', icon: '◉' },
      { label: '资金流向', route: 'cash_flow', icon: '↗' },
      { label: '行业板块', route: 'stock_sector', icon: '▦' },
      { label: '资源与愿望', route: 'skill_resource_wish', icon: '◇' },
      { label: '推演工作台', route: 'scenario_simulation', icon: '🎭' }
    ])

const selected = ref('')

const selectSection = (section) => {
  selected.value = section.label
}

watch(() => props.context, () => {
  selected.value = ''
}, { immediate: true })
</script>

<template>
  <aside class="context-sidebar" aria-label="页面侧边栏">
    <nav>
      <section v-for="section in sections" :key="section.label" class="sidebar-section">
        <RouterLink
          v-if="section.route"
          class="section-button"
          :class="{ 'is-selected': route.name === section.route }"
          :to="{ name: section.route }"
        >
          <span>{{ section.label }}</span>
        </RouterLink>
        <button
          v-else
          class="section-button"
          :class="{ 'is-selected': selected === section.label }"
          type="button"
          @click="selectSection(section)"
        >
          <span>{{ section.label }}</span>
        </button>
      </section>
    </nav>
  </aside>
</template>

<style scoped>
.context-sidebar {
  box-sizing: border-box;
  flex: 0 0 220px;
  width: 220px;
  max-height: calc(100dvh - 34px);
  overflow: auto;
  padding: 22px 12px;
  border-right: 1px solid #e8edf3;
  background: #fff;
  color: #334155;
}

.sidebar-section + .sidebar-section {
  margin-top: 8px;
}

.section-button {
  display: flex;
  width: 100%;
  align-items: center;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font: inherit;
  text-align: left;
  text-decoration: none;
  min-height: 40px;
  gap: 10px;
  padding: 0 10px;
  font-size: 14px;
  font-weight: 600;
}

.section-button:hover {
  background: #f1f5f9;
  color: #1d4ed8;
}

.section-button.is-selected {
  background: #eff6ff;
  color: #1d4ed8;
}

.section-icon {
  display: inline-grid;
  width: 20px;
  place-items: center;
  color: #64748b;
  font-size: 16px;
}

@media (max-width: 600px) {
  .context-sidebar {
    flex-basis: 160px;
    width: 160px;
    padding-right: 8px;
    padding-left: 8px;
  }
}
</style>
