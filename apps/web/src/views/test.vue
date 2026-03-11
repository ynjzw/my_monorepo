<script setup>
import { onMounted, ref } from 'vue';
import { get_old_structure, get_new_structure, getLink } from '@/api';
import structure from '@/components/structure.vue';

const old_structure = ref([])
const new_structure = ref([])
const link = ref([])
const isLoading = ref(true)

// 处理图表就绪
const handleChartReady = (chart) => {
  console.log('图表已就绪:', chart)
  // 可以在这里对图表进行额外配置
}

// 处理错误
const handleError = (error) => {
  console.error('图表错误:', error)
}

// 加载数据
const loadData = async () => {
  isLoading.value = true
  try {
    // 并行加载数据
    const [old_structureData, new_structureData, linkData] = await Promise.all([
      get_old_structure(),
      get_new_structure(),
      getLink()
    ])
    
    old_structure.value = old_structureData
    new_structure.value = new_structureData
    link.value = linkData
    
  } catch (error) {
    console.error('数据加载失败:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="container">
    <div v-if="isLoading" class="loading">加载数据中...</div>
    <div v-else class="charts-wrapper">
      <div class="chart-item">
        <structure 
          :data="old_structure" 
          :link="link"
          layout="none"
          @chart-ready="handleChartReady" 
          @error="handleError"
        />
      </div>
      <div class="chart-item">
        <structure 
          :data="new_structure" 
          :link="link"
          layout="force"
          @chart-ready="handleChartReady" 
          @error="handleError"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.loading {
  padding: 40px;
  text-align: center;
  font-size: 16px;
  color: #909399;
}

.charts-wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 两列等宽，完美并列 */
  gap: 24px;
}

.chart-item {
  flex: 1 1 calc(50% - 10px); /* 计算宽度，减去gap的一半 */
  min-width: 300px;
  height: 500px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .chart-item {
    flex: 1 1 100%;
    height: 400px;
  }
}
</style>