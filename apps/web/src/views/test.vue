<script setup>
import { onMounted, ref } from 'vue';
import { getFamily, getLinks, getWorld } from '@/api';
import * as echarts from 'echarts';
import level from '@/components/level.vue';

const node = ref([])
const world = ref([])
const link = ref([])
const isLoading = ref(true)

// 处理图表就绪
const handleChartReady = (chart) => {
  console.log('图表已就绪:', chart)
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
    const [familyData, worldData,linkData] = await Promise.all([
      getFamily(),
      getWorld(),
      getLinks()
    ])
    
    node.value = familyData
    world.value = worldData
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
  <div>
    <div v-if="isLoading">加载数据中...</div>
    <level 
      v-else
      :data="node" 
      :link="link"
      @chart-ready="handleChartReady" 
      @error="handleError"
    />
    <!-- 如果要显示多个，可以加key确保唯一性 -->
    <level 
      v-if="!isLoading"
      :data="world" 
      :link="link"
      @chart-ready="handleChartReady" 
      @error="handleError"
    />
  </div>
</template>