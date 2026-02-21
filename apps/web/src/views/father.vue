<!-- ParentComponent.vue -->
<template>
  <div class="parent-container">
    <h2>圆形打包图示例</h2>
    
    <!-- 基本使用 -->
    <CirclePackingChart 
      ref="chartRef"
      height="400px"
      @chart-ready="handleChartReady"
      @node-click="handleNodeClick"
      @data-loaded="handleDataLoaded"
      @error="handleError"
    />
    
    <!-- 显示当前状态 -->
    <div class="status-bar">
      <span>当前深度: {{ currentDepth }}</span>
      <button @click="refreshData">刷新数据</button>
      <button @click="resetChart">重置</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import CirclePackingChart from '@/components/CirclePackingChart.vue'
import { getWorld } from '../api'

const chartRef = ref(null)
const currentDepth = ref(0)
const data = ref([])
// 处理图表就绪
const handleChartReady = (chart) => {
  console.log('图表已就绪:', chart)
}

// 处理节点点击
const handleNodeClick = (params) => {
  console.log('点击了节点:', params)
  // 可以通过 ref 获取当前深度
  if (chartRef.value) {
    currentDepth.value = chartRef.value.getCurrentDepth()
  }
}

// 处理数据加载完成
const handleDataLoaded = (data) => {
  console.log('数据加载完成:', data)
}

// 处理错误
const handleError = (error) => {
  console.error('图表错误:', error)
}

// 刷新数据
const refreshData = () => {
  if (chartRef.value) {
    chartRef.value.loadData()
  }
}

// 重置图表
const resetChart = () => {
  if (chartRef.value) {
    chartRef.value.resetView()
    currentDepth.value = 0
  }
}
onMounted(async() => {
 
  data.value=await getWorld()
})
</script>

<style scoped>
.parent-container {
  padding: 20px;
}

.status-bar {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.status-bar button {
  padding: 5px 10px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.status-bar button:hover {
  background: #3aa876;
}
</style>