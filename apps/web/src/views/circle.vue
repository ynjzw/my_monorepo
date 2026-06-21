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
    <!-- <div class="control-panel">
      <button @click="goBack" class="control-btn" :disabled="historyStack.length <= 1">
        ← 返回上一级
      </button>
      <button @click="resetToRoot" class="control-btn">🏠 根节点</button>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import test1 from '@/data/test1.json'

// 模拟数据 - 树形结构
const mockData = {
  name: "11节点",
  value:11,
  children: [
    {
      name: "Chart",
      value: 30,
      children: [
        { name: "Line", value: 10 },
        { name: "Bar", value: 12 },
        { name: "Pie", value: 1 }
      ]
    },
    {
      name: "Component",
      value: 40,
      children: [
        { 
          name: "Button", 
          value: 15,
          children: [
            { name: "Primary", value: 5 },
            { name: "Secondary", value: 5 },
            { name: "Danger", value: 5 }
          ]
        },
        { name: "Table", value: 13 }
      ]
    },
    {
      name: "Option",
      value: 30,
      children: [
        { name: "Setting", value: 10 },
        { name: "Preference", value: 10 },
        { name: "Config", value: 10 }
      ]
    },
    {
      name: "Option222",
      value: 10,
      children: [
        { name: "Setting", value: 10 },
        { name: "Preference", value: 10 },
        { name: "Config", value: 10 }
      ]
    }
  ]
}

// DOM 引用
const chartContainer = ref(null)

// 状态变量
let myChart = null
const loading = ref(false)
const error = ref(null)

// 导航历史栈
const historyStack = ref([mockData])
// 缓存已加载的节点数据
const nodeCache = ref(new Map())

// 当前节点
const currentNode = computed(() => {
  return historyStack.value[historyStack.value.length - 1]
})

// 准备当前层级的圆堆数据
const prepareCurrentLevelData = () => {
  const currentNodeData = currentNode.value
  if (!currentNodeData) return { data: [], root: null }
  
  // 创建层级结构数据
  const nodes = []
  const edges = []
  
  // 添加当前节点
  const rootId = 'root'
  nodes.push({
    id: rootId,
    name: currentNodeData.name,
    value: currentNodeData.value || 50,
    isCurrent: true,
    depth: 0
  })
  
  // 添加子节点
  if (currentNodeData.children) {
    currentNodeData.children.forEach((child, index) => {
      const childId = `child_${index}_${Date.now()}_${Math.random()}`
      nodes.push({
        id: childId,
        name: child.name,
        value: child.value || 20,
        parentId: rootId,
        depth: 1,
        hasChildren: child.children && child.children.length > 0
      })
      
      edges.push({
        source: rootId,
        target: childId
      })
    })
  }
  
  return { nodes, edges, root: { id: rootId, ...currentNodeData } }
}

// 创建图表配置
const createChartOption = (nodes, edges, root) => {
  const width = chartContainer.value?.clientWidth || 800
  const height = chartContainer.value?.clientHeight || 600
  
  // 计算圆形布局位置
  const centerX = width / 2
  const centerY = height / 2
  const rootRadius = Math.min(width, height) * 0.25
  
  // 为每个节点计算位置
  const positionedNodes = nodes.map(node => {
    if (node.isCurrent) {
      // 根节点放在中心
      return {
        ...node,
        x: centerX,
        y: centerY,
        r: rootRadius
      }
    } else {
      // 子节点围绕根节点分布
      const childNodes = nodes.filter(n => n.parentId === node.parentId)
      const index = childNodes.findIndex(n => n.id === node.id)
      const total = childNodes.length
      
      // 计算角度
      const angle = (index / total) * Math.PI * 2
      // 计算位置（距离中心 rootRadius + 一些间距）
      const distance = rootRadius + 50 + (node.hasChildren ? 30 : 0)
      
      return {
        ...node,
        x: centerX + Math.cos(angle) * distance,
        y: centerY + Math.sin(angle) * distance,
        r: node.hasChildren ? 40 : 30
      }
    }
  })
  
  return {
    tooltip: {
      formatter: (params) => {
        const data = params.data
        if (!data) return ''
        
        let info = `${data.name}<br/>`
        info += `值: ${data.value}<br/>`
        if (data.hasChildren) {
          info += `点击可展开`
        } else {
          info += `叶子节点`
        }
        return info
      }
    },
    toolbox: {
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {backgroundColor:'pillow'}
      }
    },
    series: [
      {
      type: 'graph',
      symbolSize: (value, params) => {
        return params.data.isCurrent ? 80 : (params.data.hasChildren ? 60 : 40)
      },
      roam: true,
      label: {
        show: true,
        position: 'inside',
        fontSize: 12,
        color: '#fff',
        fontWeight: 'bold',
        formatter: (params) => {
          return params.data.name
        }
      },
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: [0, 10],
      lineStyle: {
        color: '#fff',
        width: 2,
        curveness: 0.2,
        opacity: 0.5
      },
      data: positionedNodes.map(node => ({
        ...node
      })),
      edges: edges
    }]
  }
}

// 更新图表
const updateChart = () => {
  if (!myChart) return
  
  const { nodes, edges, root } = prepareCurrentLevelData()
  const option = createChartOption(nodes, edges, root)
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
    
    // 更新图表
    updateChart()
    
  } catch (err) {
    console.error('图表初始化失败:', err)
    error.value = '图表初始化失败'
  }
}

// 绑定事件
const bindEvents = () => {
  if (!myChart) return
  
  // 节点点击事件
  myChart.on('click', (params) => {
    const node = params.data
    if (!node) return
    
    // 如果是当前节点，不做处理
    if (node.isCurrent) return
    
    // 查找对应的子节点数据
    const findChildNode = (parent, childName) => {
      if (!parent.children) return null
      return parent.children.find(child => child.name === childName)
    }
    
    const childNode = findChildNode(currentNode.value, node.name)
    
    // 如果是可展开的节点（有子节点）
    if (childNode && childNode.children && childNode.children.length > 0) {
      // 添加到历史栈
      historyStack.value.push(childNode)
      // 更新图表
      updateChart()
    }
  })
}

// 返回上一级
const goBack = () => {
  if (historyStack.value.length <= 1) return
  
  historyStack.value.pop()
  updateChart()
}

// 重置到根节点
const resetToRoot = () => {
  historyStack.value = [mockData]
  updateChart()
}

// 重试加载
const retryLoad = () => {
  updateChart()
}

// 处理窗口大小变化
const handleResize = () => {
  if (myChart) {
    myChart.resize()
    updateChart()
  }
}

// 生命周期
onMounted(() => {
  // 等待DOM渲染完成
  nextTick(() => {
    initChart()
  })
  
  window.addEventListener('resize', handleResize)
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
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
  height: 400px;
  min-height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.chart-container {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #666eea 0%, #c0c1c0 100%);
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
  background: pillow;
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
  background: linear-gradient(135deg, #c0c0c0 0%, #c0c0c0 100%);
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