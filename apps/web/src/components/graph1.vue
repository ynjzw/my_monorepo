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

const props = defineProps({
  data: {
    type: Array,
    default: () => []  // 提供默认值
  },
  link: {
    type: Array,
    default: () => []  // 提供默认值
  },
  layout: {
    type: String,
    default: 'none'
  }
})

const chartContainer = ref(null)
let myChart = null
const loading = ref(false)
const error = ref(null)

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
watch(
  () => [props.data, props.link, props.layout],
  () => {
    console.log(props.data, props.link, props.layout)
    if (myChart && (props.data.length > 0 || props.link.length > 0)) {
      updateChartOptions()
    }
  },
  { deep: true, immediate: true }  // immediate: true 让初始加载时也执行
)
// 更新图表选项
const updateChartOptions = () => {
  if (!myChart) return
  
  const option = {
    series: [{
      type: 'graph',
      layout: props.layout,
      draggable:true,    
      symbolSize: 50,
      roam: true,
      label: {
        show: true
      },
      // data: props.data,  // 使用传入的数据
      data:[{name:'xxx',value:'xxx',symbolSize:10,Symbol:'rect'}],
      // links: props.link,  // 可以根据需要从props传入
      links:[],
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
      right: 20,
      top: 10,
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    itemStyle:{
      
    },
    title: {
      text: 'test',
      left: 20,
      top: 10,
      textStyle: {
        fontSize: 14,
        color: 'black',
        fontWeight: 'normal'
      }
    }
  }
  
  myChart.setOption(option)
}
// 组件挂载后初始化
onMounted(() => {
  initChart()
  if (props.data.length > 0 || props.link.length > 0) {
    nextTick(() => {
      updateChartOptions()
    })
  }
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
  width: 800px;
  height: 600px;
  min-height: 400px; /* 设置最小高度 */
  min-width: 400px; 
  background-color: pink;
}
</style>
