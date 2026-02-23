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
      <button @click="goBack" class="control-btn" :disabled="historyStack.length <= 1">
        ← 返回上一级
      </button>
      <button @click="resetToRoot" class="control-btn">🏠 根节点</button>
      <span class="path-indicator">{{ currentPath }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import * as d3 from 'd3-hierarchy'

// 模拟数据 - 完全内部定义，不依赖外部传入
const mockData = {
  root: {
    id: 'root',
    name: '根节点',
    value: 100,
    children: [
      { id: 'chart', name: 'Chart', value: 30 },
      { id: 'component', name: 'Component', value: 40 },
      { id: 'option', name: 'Option', value: 30 }
    ]
  },
  chart: {
    id: 'chart',
    name: 'Chart',
    value: 30,
    children: [
      { id: 'chart.line', name: 'Line', value: 10 },
      { id: 'chart.bar', name: 'Bar', value: 12 },
      { id: 'chart.pie', name: 'Pie', value: 8 }
    ]
  },
  component: {
    id: 'component',
    name: 'Component',
    value: 40,
    children: [
      { id: 'component.button', name: 'Button', value: 15 },
      { id: 'component.input', name: 'Input', value: 12 },
      { id: 'component.table', name: 'Table', value: 13 }
    ]
  },
  option: {
    id: 'option',
    name: 'Option',
    value: 30,
    children: [
      { id: 'option.setting', name: 'Setting', value: 10 },
      { id: 'option.preference', name: 'Preference', value: 10 },
      { id: 'option.config', name: 'Config', value: 10 }
    ]
  },
  'chart.line': {
    id: 'chart.line',
    name: 'Line',
    value: 10,
    children: []
  },
  'chart.bar': {
    id: 'chart.bar',
    name: 'Bar',
    value: 12,
    children: []
  },
  'chart.pie': {
    id: 'chart.pie',
    name: 'Pie',
    value: 8,
    children: []
  },
  'component.button': {
    id: 'component.button',
    name: 'Button',
    value: 15,
    children: [
      { id: 'component.button.primary', name: 'Primary', value: 5 },
      { id: 'component.button.secondary', name: 'Secondary', value: 5 },
      { id: 'component.button.danger', name: 'Danger', value: 5 }
    ]
  },
  'component.input': {
    id: 'component.input',
    name: 'Input',
    value: 12,
    children: []
  },
  'component.table': {
    id: 'component.table',
    name: 'Table',
    value: 13,
    children: []
  },
  'component.button.primary': {
    id: 'component.button.primary',
    name: 'Primary',
    value: 5,
    children: []
  },
  'component.button.secondary': {
    id: 'component.button.secondary',
    name: 'Secondary',
    value: 5,
    children: []
  },
  'component.button.danger': {
    id: 'component.button.danger',
    name: 'Danger',
    value: 5,
    children: []
  },
  'option.setting': {
    id: 'option.setting',
    name: 'Setting',
    value: 10,
    children: []
  },
  'option.preference': {
    id: 'option.preference',
    name: 'Preference',
    value: 10,
    children: []
  },
  'option.config': {
    id: 'option.config',
    name: 'Config',
    value: 10,
    children: []
  }
}

// DOM 引用
const chartContainer = ref(null)

// 状态变量
let myChart = null
const loading = ref(false)
const error = ref(null)

// 导航历史栈
const historyStack = ref(['root'])
// 缓存已加载的节点数据
const nodeCache = ref(new Map())

// 当前节点ID
const currentNodeId = computed(() => {
  return historyStack.value[historyStack.value.length - 1]
})

// 当前路径显示
const currentPath = computed(() => {
  return historyStack.value.map(id => {
    const node = nodeCache.value.get(id)
    return node ? node.name : id
  }).join(' > ')
})

// 获取当前节点数据
const getCurrentNodeData = () => {
  return nodeCache.value.get(currentNodeId.value)
}

// 获取当前节点的子节点
const getCurrentChildren = () => {
  const currentNode = getCurrentNodeData()
  return currentNode?.children || []
}

// 模拟异步加载节点数据
const loadNodeData = async (nodeId) => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // 从mock数据中获取
  const nodeData = mockData[nodeId]
  if (!nodeData) {
    throw new Error(`节点 ${nodeId} 不存在`)
  }
  
  return nodeData
}

// 加载节点
const loadNode = async (nodeId) => {
  loading.value = true
  error.value = null
  
  try {
    // 检查缓存
    if (!nodeCache.value.has(nodeId)) {
      const nodeData = await loadNodeData(nodeId)
      nodeCache.value.set(nodeId, nodeData)
    }
    
    // 更新图表
    await nextTick()
    updateChart()
    
  } catch (err) {
    console.error('加载节点失败:', err)
    error.value = `加载失败: ${err.message}`
  } finally {
    loading.value = false
  }
}

// 准备当前层级的圆堆数据
const prepareCurrentLevelData = () => {
  const currentNode = getCurrentNodeData()
  if (!currentNode) return []
  
  const result = []
  
  // 添加当前节点（中心节点）- 放大显示
  result.push({
    id: currentNode.id,
    name: currentNode.name,
    value: currentNode.value || 50,
    isCurrent: true,
    depth: 0,
    type: 'current'
  })
  
  // 添加子节点
  const children = getCurrentChildren()
  children.forEach((child, index) => {
    // 从缓存获取完整数据，如果没有则使用基本信息
    const cachedChild = nodeCache.value.get(child.id) || child
    result.push({
      id: cachedChild.id,
      name: cachedChild.name,
      value: cachedChild.value || 20,
      parentId: currentNode.id,
      depth: 1,
      type: cachedChild.children?.length ? 'parent' : 'leaf',
      hasChildren: cachedChild.children?.length > 0
    })
  })
  
  return result
}

// 创建图表配置
const createChartOption = (levelData) => {
  if (!levelData.length) return {}
  
  const width = chartContainer.value?.clientWidth || 800
  const height = chartContainer.value?.clientHeight || 600
  
  // 创建层级结构
  const stratifyData = d3.stratify()
    .id(d => d.id)
    .parentId(d => d.parentId || null)(levelData)
  
  // 计算圆堆布局
  const root = d3.hierarchy(stratifyData)
    .sum(d => d.data.value)
  
  const pack = d3.pack()
    .size([width - 60, height - 60])
    .padding(8)
  
  pack(root)
  
  // 构建节点数据
  const nodes = root.descendants().map(node => {
    const data = node.data.data
    return {
      id: data.id,
      name: data.name,
      value: node.value,
      x: node.x + 30,
      y: node.y + 30,
      r: node.r,
      depth: node.depth,
      type: data.type,
      isCurrent: data.isCurrent || false,
      hasChildren: data.hasChildren || false,
      children: node.children ? node.children.map(c => c.data.data.id) : []
    }
  })
  
  return {
    tooltip: {
      formatter: (params) => {
        const data = params.data
        if (!data) return ''
        
        let info = `${data.name}<br/>`
        info += `值: ${data.value.toFixed(2)}<br/>`
        if (data.hasChildren) {
          info += `包含 ${data.children?.length || 0} 个子节点<br/>`
          info += `点击可展开`
        } else {
          info += `叶子节点`
        }
        return info
      }
    },
    series: [{
      type: 'custom',
      renderItem: (params, api) => {
        const data = params.data
        if (!data) return
        
        // 根据节点类型设置不同颜色
        let fillColor
        if (data.isCurrent) {
          fillColor = '#ff6b6b' // 当前节点 - 红色
        } else if (data.hasChildren) {
          fillColor = '#4ecdc4' // 有子节点的节点 - 青色
        } else {
          fillColor = '#95a5a6' // 叶子节点 - 灰色
        }
        
        // 计算字体大小
        const fontSize = Math.min(Math.max(data.r / 4, 10), 16)
        
        return {
          type: 'circle',
          shape: {
            cx: data.x,
            cy: data.y,
            r: data.r
          },
          style: {
            fill: fillColor,
            stroke: '#fff',
            lineWidth: data.isCurrent ? 4 : 2,
            shadowBlur: data.isCurrent ? 20 : 5,
            shadowColor: 'rgba(0,0,0,0.3)',
            transition: ['fill', 'shadowBlur']
          },
          styleEmphasis: {
            fill: data.isCurrent ? '#ff5252' : (data.hasChildren ? '#45b7d1' : '#7f8c8d'),
            shadowBlur: 20,
            scale: 1.05
          },
          textContent: {
            type: 'text',
            style: {
              text: data.name,
              fontFamily: 'Arial',
              fontSize: fontSize,
              fill: '#fff',
              fontWeight: 'bold',
              textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
              lineWidth: 0
            },
            styleEmphasis: {
              fontSize: fontSize + 2
            }
          },
          textConfig: {
            position: 'inside'
          }
        }
      },
      data: nodes,
      progressive: 0,
      coordinateSystem: 'none'
    }]
  }
}

// 更新图表
const updateChart = () => {
  if (!myChart) return
  
  const levelData = prepareCurrentLevelData()
  const option = createChartOption(levelData)
  myChart.setOption(option, { notMerge: false })
}

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return
  
  try {
    if (myChart) {
      myChart.dispose()
    }
    
    myChart = echarts.init(chartContainer.value)
    bindEvents()
    
    // 加载根节点
    loadRoot()
    
  } catch (err) {
    console.error('图表初始化失败:', err)
    error.value = '图表初始化失败'
  }
}

// 绑定事件
const bindEvents = () => {
  if (!myChart) return
  
  // 节点点击事件
  myChart.on('click', { seriesIndex: 0 }, async (params) => {
    const node = params.data
    if (!node) return
    
    // 如果是当前节点，不做处理
    if (node.isCurrent) return
    
    // 如果是可展开的节点（有子节点）
    if (node.hasChildren) {
      // 添加到历史栈
      historyStack.value.push(node.id)
      // 加载该节点
      await loadNode(node.id)
    }
  })
}

// 加载根节点
const loadRoot = async () => {
  historyStack.value = ['root']
  await loadNode('root')
}

// 返回上一级
const goBack = () => {
  if (historyStack.value.length <= 1) return
  
  historyStack.value.pop()
  loadNode(currentNodeId.value)
}

// 重置到根节点
const resetToRoot = () => {
  loadRoot()
}

// 重试加载
const retryLoad = () => {
  loadNode(currentNodeId.value)
}

// 处理窗口大小变化
const handleResize = () => {
  if (myChart) {
    myChart.resize()
    updateChart() // 重新计算布局
  }
}

// 生命周期
onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  
  // 使用 ResizeObserver 监听容器尺寸变化
  const resizeObserver = new ResizeObserver(() => {
    handleResize()
  })
  
  if (chartContainer.value) {
    resizeObserver.observe(chartContainer.value)
  }
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
    resizeObserver.disconnect()
    if (myChart) {
      myChart.dispose()
      myChart = null
    }
  })
})
</script>

<style scoped>
.circle-packing-container {
  position: relative;
  width: 1000px;
  height: 600px;
  min-height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.chart-container {
  width: 1000px;
  height: 600px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  background: rgba(255, 255, 255, 0.95);
  z-index: 10;
  backdrop-filter: blur(5px);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
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
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.error-overlay button:hover {
  background: #764ba2;
  transform: translateY(-2px);
}

.control-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 10px;
  background: rgba(255, 255, 255, 0.95);
  padding: 10px 15px;
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 5;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.control-btn {
  padding: 6px 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(102, 126, 234, 0.3);
}

.control-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
}

.control-btn:disabled {
  background: linear-gradient(135deg, #c0c0c0 0%, #a0a0a0 100%);
  cursor: not-allowed;
  opacity: 0.5;
  transform: none;
  box-shadow: none;
}

.path-indicator {
  font-size: 13px;
  color: #333;
  line-height: 30px;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 10px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
}
</style>