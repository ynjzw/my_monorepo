<script setup>
import { onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  data: {
    type: Array,
    default: () => []  // 提供默认值
  },
  link: {
    type: Array,
    default: () => []  // 提供默认值
  }
})

const emit = defineEmits([
  'chart-ready',
  'error'
])

const chartContainer = ref(null)
let myChart = null
const loading = ref(false)
const error = ref(null)

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return
  
  try {
    // 如果已存在图表实例，先销毁
    if (myChart) {
      myChart.dispose()
    }
    
    // 创建新图表实例
    myChart = echarts.init(chartContainer.value)
    
    // 设置基本选项
    updateChartOptions()
    
    // 监听窗口大小变化
    window.addEventListener('resize', handleResize)
    
    emit('chart-ready', myChart)
    
  } catch (err) {
    console.error('图表初始化失败:', err)
    error.value = '图表初始化失败'
    emit('error', err)
  }
}

// 更新图表选项
const updateChartOptions = () => {
  if (!myChart) return
  
  const option = {
    series: [{
      type: 'graph',
      layout: 'none',
      symbolSize: 50,
      roam: true,
      label: {
        show: true
      },
      data: props.data,  // 使用传入的数据
      links: props.link,  // 可以根据需要从props传入
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0
      }
    }]
  }
  
  myChart.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  myChart?.resize()
}

// 监听数据变化，更新图表
watch(() => props.data, (newData) => {
  if (newData && newData.length > 0 && myChart) {
    updateChartOptions()
  }
}, { deep: true })

// 组件挂载后初始化
onMounted(() => {
  initChart()
})


defineExpose({
  getChart: () => myChart,
  updateChart: updateChartOptions
})
</script>

<template>
  <div 
    ref="chartContainer" 
    class="chart-container"
  ></div>
  <div v-if="loading" class="loading">加载中...</div>
  <div v-if="error" class="error">{{ error }}</div>
</template>

<style scoped>
.loading, .error {
  text-align: center;
  padding: 20px;
}
.error {
  color: red;
}
.chart-container {
  width: 1000px;
  height: 400px;
}
</style>