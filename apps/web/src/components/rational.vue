<template>
  <div class="chart-wrapper">
    <div 
      ref="chartContainer" 
      class="chart-container"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup >
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import * as echarts from 'echarts';

const chartContainer = ref(null)
let myChart = null
const loading = ref(false)
const error = ref(null)
const data = [
          {"name": "原因", "value": "原因"},
          {"name": "手段", "value": "手段"},
          {"name": "目的", "value": "目的"},
          {"name": "问题", "value": "问题"},
          {"name": "效果", "value": "效果"}
        ];
const link = [
          {"source": "原因", "target": "问题"},
          {"source": "原因", "target": "效果"},
          {"source": "手段", "target": "目的"},
          {"source": "手段", "target": "效果"},
          {"source": "目的", "target": "问题"},
        ]

const emit = defineEmits([
  'chart-ready',
  'error'
])
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
      layout: 'force',
      draggable:true,    
      symbolSize: 50,
      roam: true,
      label: {
        show: true
      },
      data: data,  // 使用传入的数据
      links: link,  // 可以根据需要从props传入
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0
      },
      force: {
        initLayout: 'circular',
        gravity: 0.1,
        repulsion: 1000
      }
    }],
    toolbox: {
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    title: {
      text: '逻辑-左脑',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        color: 'white',
        fontWeight: 'normal'
      }
    }
  }
  
  myChart.setOption(option)
}
// 组件挂载后初始化
onMounted(() => {
  initChart()
})

// 处理窗口大小变化
const handleResize = () => {
  myChart?.resize()
}

defineExpose({
  getChart: () => myChart,
  updateChart: updateChartOptions
})
</script>

<style>
.loading {
  text-align: center;
  padding: 20px;
}
.error {
  color: red;
}
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px; /* 设置最小高度 */
  min-width: 400px; 
}
</style>