<template>
  <div class="circle-packing-container">
    <!-- 图表容器 -->
    <div ref="chartContainer" class="chart-container"></div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 错误状态 -->
    <div v-if="error" class="error-overlay">
      <p>{{ error }}</p>
      <button @click="retryLoad">重试</button>
    </div>
    
    <!-- 控制面板 -->
    <div class="control-panel">
      <button @click="resetView" class="control-btn">
        重置视图
      </button>
      <span class="depth-indicator">当前深度: {{ currentDepth }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import * as d3 from 'd3-hierarchy'

// Props 定义
const props = defineProps({
  // 可以传入自定义数据
  data: {
    type: Object,
    default: null
  },
  // 图表高度
  height: {
    type: [String, Number],
    default: '100%'
  },
  // 是否自动加载
  autoLoad: {
    type: Boolean,
    default: true
  },
  // 主题颜色
  theme: {
    type: String,
    default: 'dark'
  }
})

// Emits 定义
const emit = defineEmits([
  'chart-ready',
  'node-click',
  'data-loaded',
  'error'
])

// DOM 引用
const chartContainer = ref(null)

// 状态变量
let myChart = null
const loading = ref(false)
const error = ref(null)
const currentDepth = ref(0)
const seriesData = ref([])
const maxDepth = ref(0)
let displayRoot = null

const Chart = {
  "$count":50,
  "Option1": {
    "$count":10,
  },
  "Option2": {
    "$count":10,
  },
  "Option3": {
    "$count":10,
  }
}
const data = {
  "$count":50,
  Chart,
  "Chart1": { 
    "$count":10,
  },
  "Component": {
    "$count":10,
  },
  "Option1": {
    "$count":10,
  },
  "Option2": {
    "$count":10,
  },
  "Option3": {
    "$count":10,
  }
}

// 准备数据
const prepareData = (rawData) => {
  const data = []
  let depth = 0
  
  const convert = (source, basePath, currentDepth) => {
    if (source == null) return
    if (depth > 5) return
    
    depth = Math.max(currentDepth, depth)
    
    data.push({
      id: basePath,
      value: source.$count || 0,
      depth: currentDepth,
      index: data.length
    })
    
    for (const key in source) {
      if (source.hasOwnProperty(key) && !key.match(/^\$/)) {
        const path = basePath + '.' + key
        convert(source[key], path, currentDepth + 1)
      }
    }
  }
  
  convert(rawData, 'root', 0)
  
  return {
    seriesData: data,
    maxDepth: depth
  }
}

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return
  
  try {
    // 如果已存在图表实例，先销毁
    if (myChart) {
      myChart.dispose()
    }
    
    // 创建新图表实例
    myChart = echarts.init(chartContainer.value, props.theme)
    
    // 创建层级结构
    displayRoot = stratifyData()
    
    // 设置图表选项
    const option = createChartOption()
    myChart.setOption(option)
    
    // 绑定事件
    bindEvents()
    
    // 触发就绪事件
    emit('chart-ready', myChart)
    
  } catch (err) {
    console.error('图表初始化失败:', err)
    error.value = '图表初始化失败'
    emit('error', err)
  }
}

// 创建层级数据
const stratifyData = () => {
  return d3
    .stratify()
    .parentId((d) => {
      const lastDotIndex = d.id.lastIndexOf('.')
      return lastDotIndex > 0 ? d.id.substring(0, lastDotIndex) : null
    })(seriesData.value)
    .sum((d) => d.value || 0)
    .sort((a, b) => b.value - a.value)
}

// 创建图表配置
const createChartOption = () => {
  const overallLayout = (params, api) => {
    const context = params.context
    d3
      .pack()
      .size([api.getWidth() - 2, api.getHeight() - 2])
      .padding(3)(displayRoot)
    
    context.nodes = {}
    displayRoot.descendants().forEach((node) => {
      context.nodes[node.id] = node
    })
  }
  
  const renderItem = (params, api) => {
    const context = params.context
    
    if (!context.layout) {
      context.layout = true
      overallLayout(params, api)
    }
    
    const nodePath = api.value('id')
    const node = context.nodes[nodePath]
    
    if (!node) return
    
    const isLeaf = !node.children || !node.children.length
    const focus = new Uint32Array(
      node.descendants().map((n) => n.data.index)
    )
    
    const nodeName = isLeaf
      ? nodePath
          .slice(nodePath.lastIndexOf('.') + 1)
          .split(/(?=[A-Z][^A-Z])/g)
          .join('\n')
      : ''
    
    const z2 = api.value('depth') * 2
    
    return {
      type: 'circle',
      focus: focus,
      shape: {
        cx: node.x,
        cy: node.y,
        r: node.r
      },
      transition: ['shape'],
      z2: z2,
      textContent: {
        type: 'text',
        style: {
          text: nodeName,
          fontFamily: 'Arial',
          width: node.r * 1.3,
          overflow: 'truncate',
          fontSize: node.r / 3
        },
        emphasis: {
          style: {
            overflow: null,
            fontSize: Math.max(node.r / 3, 12)
          }
        }
      },
      textConfig: {
        position: 'inside'
      },
      style: {
        fill: api.visual('color')
      },
      emphasis: {
        style: {
          fontFamily: 'Arial',
          fontSize: 12,
          shadowBlur: 20,
          shadowOffsetX: 3,
          shadowOffsetY: 5,
          shadowColor: 'rgba(0,0,0,0.3)'
        }
      }
    }
  }
  
  return {
    dataset: {
      source: seriesData.value
    },
    tooltip: {},
    visualMap: [
      {
        show: false,
        min: 0,
        max: maxDepth.value,
        dimension: 'depth',
        inRange: {
          color: ['red', 'yellow']
        }
      }
    ],
    hoverLayerThreshold: Infinity,
    series: {
      type: 'custom',
      renderItem: renderItem,
      progressive: 0,
      coordinateSystem: 'none',
      encode: {
        tooltip: 'value',
        itemName: 'id'
      }
    }
  }
}

// 绑定事件
const bindEvents = () => {
  if (!myChart) return
  
  // 节点点击事件
  myChart.on('click', { seriesIndex: 0 }, (params) => {
    drillDown(params.data.id)
    emit('node-click', params)
  })
  
  // 空白区域点击（重置）
  myChart.getZr().on('click', (event) => {
    if (!event.target) {
      resetView()
    }
  })
}

// 下钻功能
const drillDown = (targetNodeId) => {
  displayRoot = stratifyData()
  
  if (targetNodeId) {
    displayRoot = displayRoot.descendants().find(
      (node) => node.data.id === targetNodeId
    )
  }
  
  if (displayRoot) {
    displayRoot.parent = null
    
    // 更新当前深度
    currentDepth.value = displayRoot.depth
    
    // 刷新图表
    myChart.setOption({
      dataset: {
        source: seriesData.value
      }
    })
  }
}

// 重置视图
const resetView = () => {
  displayRoot = stratifyData()
  currentDepth.value = 0
  
  myChart.setOption({
    dataset: {
      source: seriesData.value
    }
  })
}

// 加载数据
const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    let rawData
    
    if (props.data) {
      // 使用传入的数据
      rawData = props.data
    } else {
      // 使用模拟数据
      rawData = data
      // 模拟异步加载
      await new Promise(resolve => setTimeout(resolve, 500))
    }
    
    const result = prepareData(rawData)
    seriesData.value = result.seriesData
    maxDepth.value = result.maxDepth
    
    emit('data-loaded', result)
    
    // 等待 DOM 更新后初始化图表
    await nextTick()
    initChart()
    
  } catch (err) {
    console.error('数据加载失败:', err)
    error.value = '数据加载失败: ' + err.message
    emit('error', err)
  } finally {
    loading.value = false
  }
}

// 重试加载
const retryLoad = () => {
  loadData()
}

// 更新图表尺寸
const handleResize = () => {
  if (myChart) {
    myChart.resize()
  }
}

// 监听容器尺寸变化
const setupResizeObserver = () => {
  if (!chartContainer.value) return
  
  const resizeObserver = new ResizeObserver(() => {
    handleResize()
  })
  
  resizeObserver.observe(chartContainer.value)
  return resizeObserver
}

// 生命周期钩子
onMounted(() => {
  if (props.autoLoad) {
    loadData()
  }
  
  // 设置窗口大小变化监听
  window.addEventListener('resize', handleResize)
  
  // 设置 ResizeObserver
  const observer = setupResizeObserver()
  
  // 清理函数
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
    if (observer) {
      observer.disconnect()
    }
    if (myChart) {
      myChart.dispose()
      myChart = null
    }
  })
})

// 监听数据变化
watch(() => props.data, (newData) => {
  if (newData) {
    loadData()
  }
}, { deep: true })

// 监听主题变化
watch(() => props.theme, () => {
  if (myChart && seriesData.value.length > 0) {
    initChart()
  }
})

// 暴露方法给父组件
defineExpose({
  resetView,
  loadData,
  getChart: () => myChart,
  getCurrentDepth: () => currentDepth.value
})
</script>

<style scoped>
.circle-packing-container {
  position: relative;
  width: 1000px;
  height: v-bind(height);
  min-height: 400px;
}

.chart-container {
  width: 100%;
  height: 100%;
}

.loading-overlay,
.error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  z-index: 10;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-overlay button {
  margin-top: 10px;
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-overlay button:hover {
  background: #2980b9;
}

.control-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 10px;
  background: blueviolet;
  padding: 8px 12px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 5;
}

.control-btn {
  padding: 4px 8px;
  background: burlywood;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.control-btn:hover {
  background: burlywood;
}

.depth-indicator {
  font-size: 12px;
  color: black;
  line-height: 24px;
}
</style>