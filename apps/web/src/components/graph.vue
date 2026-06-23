<script setup>
import { onMounted, ref, watch, nextTick } from 'vue';
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

const emit = defineEmits([
  'chart-ready',
  'error'
])

const chartContainer = ref(null)
let myChart = null
const loading = ref(false)
const error = ref(null)

// 检查容器尺寸
const checkContainerSize = () => {
  if (!chartContainer.value) return false
  
  const { clientWidth, clientHeight } = chartContainer.value
  // console.log('容器尺寸:', clientWidth, clientHeight) // 调试用
  
  return clientWidth > 0 && clientHeight > 0
}

// 初始化图表
const initChart = async () => {
  if (!chartContainer.value) return
  
  try {
    // 等待DOM完全渲染
    await nextTick()
    
    // 检查容器尺寸，如果为0则等待一段时间再试
    if (!checkContainerSize()) {
      console.log('容器尺寸为0，等待重试...')
      setTimeout(initChart, 100) // 100ms后重试
      return
    }
    
    // 如果已存在图表实例，先销毁
    if (myChart) {
      myChart.dispose()
    }
    
    // 创建新图表实例
    myChart = echarts.init(chartContainer.value)
    
    // 设置基本选项
    await updateChartOptions()
    
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
const updateChartOptions = async () => {
  if (!myChart) return
  
  // 确保容器有尺寸
  if (!checkContainerSize()) {
    console.warn('容器尺寸为0，无法更新图表')
    return
  }
  
  // 准备数据
  const seriesData = []
  
  // 添加主要的关系图
  seriesData.push({
    type: 'graph',
    layout: props.layout,
    roam: true,
    draggable:true,    
    label: {
      show: true,
      position: 'bottom',
      fontSize: 12
    },
    edgeLabel: {
      fontSize: 10
    },
    data: props.data.map(item => ({
      ...item,
      symbolSize: item.symbol_size ,
      itemStyle: item.itemStyle
      // 确保每个节点有名称
      // name: item.name || item.id || '未知'
    })),
    links: props.link.map(item => ({
      ...item,
      symbol: item.symbol || 'arrow'
      // 确保连接有源和目标
      // source: link.source || link.from,
      // target: link.target || link.to
    })),
    // links:[{source: '1', target: '2'}],
    force: {
      initLayout: 'circular',
      gravity: 0.1,
      repulsion: 100,
      layoutAnimation: true
    },
    lineStyle: {
      color: 'blue',
      curveness: 0.3,
      width: 2
    },
    // emphasis: {
    //   focus: 'adjacency'
    // }
  })
  
  // 如果数据为空，显示空状态
  if (props.data.length === 0) {
    seriesData.push({
      type: 'graph',
      data: [],
      links: [],
      label: {
        show: false
      }
    })
  }
  
  const option = {
    title: {
      text: 'ttt',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          return `节点: ${params.name}<br/>${params.value ? `值: ${params.value}` : ''}`
        } else {
          return `关系: ${params.data.source || ''} → ${params.data.target || ''}`
        }
      }
    },
    toolbox: {
      top:10,
      left:'center',
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    series: seriesData,
    animation: true,
    animationDuration: 500,
    animationEasing: 'cubicOut'
  }
  
  // 设置选项并立即渲染
  myChart.setOption(option, { 
    notMerge: false,
    lazyUpdate: false
  })
  
  // 确保图表渲染完成
  await nextTick()
}

// 处理窗口大小变化
const handleResize = () => {
  if (myChart && checkContainerSize()) {
    myChart.resize()
  }
}

// 监听数据变化，更新图表
watch(() => props.data, async (newData) => {
  if (myChart) {
    await nextTick()
    updateChartOptions()
  }
}, { deep: true })

// 监听布局变化
watch(() => props.layout, async () => {
  if (myChart) {
    await nextTick()
    updateChartOptions()
  }
})

// 组件挂载后初始化
onMounted(async () => {
  // 等待DOM完全渲染
  await nextTick()
  // 给容器一点时间获取尺寸
  setTimeout(() => {
    initChart()
  }, 50)
})

defineExpose({
  getChart: () => myChart,
  updateChart: updateChartOptions,
  resize: () => myChart?.resize()
})
</script>

<template>
  <div class="chart-wrapper">
    <div 
      ref="chartContainer" 
      class="chart-container"
      :style="{ width: '100%', height: '100%' }"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px; /* 设置最小高度 */
  background-color: aliceblue;
  /* border-radius: 50%; */
}

.loading, .error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  z-index: 10;
}

.error {
  color: #f56c6c;
  border: 1px solid #f56c6c;
}

.loading {
  color: #909399;
  border: 1px solid #909399;
}
</style>