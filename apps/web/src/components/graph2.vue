<template>
  <div class="chart-wrapper">
    <div 
      ref="chartContainer" 
      class="chart-container"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    
    <!-- 可复用的Dialog组件 -->
    <NodeDialog 
      v-model:visible="dialogVisible"
      :node-data="selectedNode"
      @close="handleDialogClose"
    />
  </div>
</template>

<script setup >
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import * as echarts from 'echarts';
import NodeDialog from './dialog.vue'; // 导入Dialog组件

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  link: {
    type: Array,
    default: () => []
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
const dialogVisible = ref(false)
const selectedNode = ref(null)

const emit = defineEmits([
  'chart-ready',
  'error',
  'node-click'  // 新增节点点击事件
])

const initChart = () => {
  if (!chartContainer.value) return
  
  try {
    if (myChart) {
      myChart.dispose()
    }
    
    myChart = echarts.init(chartContainer.value)
    
    // 添加点击事件监听
    myChart.off('click') // 移除之前的监听器避免重复
    myChart.on('click', handleChartClick)
    
    updateChartOptions()
    
    window.addEventListener('resize', handleResize)
    
    emit('chart-ready', myChart)
    
  } catch (err) {
    console.error('图表初始化失败:', err)
    error.value = '图表初始化失败'
    emit('error', err)
  }
}

// 处理图表点击事件
const handleChartClick = (params) => {
  // 检查是否点击的是节点（seriesName 为 'graph' 且 dataType 为 'node'）
  if (params.componentType === 'series' && params.seriesName === 'graph' && params.dataType === 'node') {
    const nodeData = params.data
    selectedNode.value = {
      name: nodeData.name,
      value: nodeData.value,
      category: nodeData.category,
      symbolSize: nodeData.symbolSize,
      itemStyle: nodeData.itemStyle,
      // 可以添加更多你需要的数据
      ...nodeData
    }
    dialogVisible.value = true
    emit('node-click', nodeData)
  }
}

// 关闭Dialog
const handleDialogClose = () => {
  dialogVisible.value = false
  selectedNode.value = null
}

watch(
  () => [props.data, props.link, props.layout],
  () => {
    if (myChart && (props.data.length > 0 || props.link.length > 0)) {
      updateChartOptions()
      // 重新绑定点击事件（因为图表重新渲染后需要重新绑定）
      myChart.off('click')
      myChart.on('click', handleChartClick)
    }
  },
  { deep: true, immediate: true }
)

const updateChartOptions = () => {
  if (!myChart) return
  
  const option = {
    series: [{
      type: 'graph',
      layout: props.layout,
      draggable: true,    
      symbolSize: 50,
      roam: true,
      label: {
        show: true,
        position: 'right',
        formatter: '{b}'
      },
      data: props.data,
      links: props.link,
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0,
        color: '#333'
      },
      force: {
        initLayout: 'circular',
        gravity: 0.1,
        repulsion: 1000
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          width: 3
        }
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
      text: '生命周期关系图',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        color: '#333',
        fontWeight: 'normal'
      }
    }
  }
  
  myChart.setOption(option)
}

onMounted(() => {
  initChart()
  if (props.data.length > 0 || props.link.length > 0) {
    nextTick(() => {
      updateChartOptions()
    })
  }
})

// 清理事件监听
onBeforeUnmount(() => {
  if (myChart) {
    myChart.off('click')
    myChart.dispose()
  }
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  myChart?.resize()
}

defineExpose({
  getChart: () => myChart,
  updateChart: updateChartOptions
})
</script>

<style scoped>
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
  height: 600px;
  min-height: 400px;
  min-width: 400px; 
  background-color: #f5f5f5;
}
</style>