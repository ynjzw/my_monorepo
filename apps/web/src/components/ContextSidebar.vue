<script setup>
import { onMounted, ref } from 'vue'
import { getGraphSidebarOptions } from '../api/simple_api'

const props = defineProps({
  context: {
    type: String,
    required: true,
    validator: (value) => ['person', 'world'].includes(value)
  }
})

const sections = props.context === 'person'
  ? [{ label: '生理' }, { label: '心理' }]
  : [
      { label: '人类足迹' },
      { label: '产业', key: 'industries' },
      { label: '专业', key: 'subjects' },
      { label: '推演场' }
    ]

const expanded = ref(new Set(['产业', '专业', '推演场']))
const selected = ref('')
const options = ref({ industries: [], subjects: [], scenarios: [] })
const loading = ref(false)
const loadError = ref('')

const toggleSection = (label) => {
  const next = new Set(expanded.value)
  if (next.has(label)) next.delete(label)
  else next.add(label)
  expanded.value = next
}

const selectSection = (section) => {
  selected.value = section.label
  if (section.key) toggleSection(section.label)
}

const loadOptions = async () => {
  if (props.context !== 'world') return
  loading.value = true
  loadError.value = ''
  try {
    options.value = await getGraphSidebarOptions()
  } catch {
    loadError.value = '选项加载失败，请重试。'
  } finally {
    loading.value = false
  }
}

onMounted(loadOptions)
</script>

<template>
  <aside class="context-sidebar" aria-label="页面侧边栏">
    <nav>
      <section v-for="section in sections" :key="section.label" class="sidebar-section">
        <button
          class="section-button"
          :class="{ 'is-selected': selected === section.label }"
          type="button"
          :aria-expanded="section.key ? expanded.has(section.label) : undefined"
          @click="selectSection(section)"
        >
          <span class="section-icon" aria-hidden="true">{{ section.icon }}</span>
          <span>{{ section.label }}</span>
          <span v-if="section.key" class="section-chevron" aria-hidden="true">
            {{ expanded.has(section.label) ? '⌄' : '›' }}
          </span>
        </button>

        <div v-if="section.key && expanded.has(section.label)" class="section-options">
          <p v-if="loading" class="sidebar-message">加载中…</p>
          <template v-else-if="loadError">
            <p class="sidebar-message error-message">{{ loadError }}</p>
            <button class="retry-button" type="button" @click="loadOptions">重试</button>
          </template>
          <button
            v-else
            v-for="name in options[section.key]"
            :key="name"
            class="option-button"
            :class="{ 'is-selected': selected === name }"
            type="button"
            @click="selected = name"
          >
            {{ name }}
          </button>
          <p v-if="!loading && !loadError && options[section.key].length === 0" class="sidebar-message">
            暂无选项
          </p>
        </div>
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

.section-button,
.option-button {
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
}

.section-button {
  min-height: 40px;
  gap: 10px;
  padding: 0 10px;
  font-size: 14px;
  font-weight: 600;
}

.section-button:hover,
.option-button:hover {
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

.section-chevron {
  margin-left: auto;
  color: #94a3b8;
}

.section-options {
  margin: 3px 0 8px 20px;
  padding-left: 10px;
  border-left: 1px solid #e2e8f0;
}

.option-button {
  min-height: 32px;
  padding: 5px 9px;
  color: #64748b;
  font-size: 12px;
  line-height: 1.4;
  overflow-wrap: anywhere;
}

.option-button.is-selected {
  background: #eff6ff;
  color: #1d4ed8;
  font-weight: 600;
}

.sidebar-message {
  margin: 8px 5px;
  color: #94a3b8;
  font-size: 12px;
}

.error-message {
  color: #b91c1c;
}

.retry-button {
  margin: 0 5px 8px;
  padding: 4px 8px;
  border: 0;
  border-radius: 5px;
  background: #eff6ff;
  color: #1d4ed8;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
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
