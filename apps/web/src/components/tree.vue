<template>
  <div class="chart-wrapper">
    <div 
      ref="chartContainer" 
      class="chart-container"      
    >
  </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick, computed } from 'vue'
import * as echarts from 'echarts'

// ============ Props ============
const props = defineProps({
  // 树形数据
  data: {
    type: Object,
    default: () => null
  },
  // 主题
  theme: {
    type: String,
    default: 'auto' // 'light' | 'dark' | 'default'
  }
})

// ============ Emits ============
const emit = defineEmits(['click', 'ready', 'resize'])

// ============ Refs ============
const chartContainer = ref(null)
let chartInstance = null
let resizeObserver = null


// ============ 默认树形数据 ============
const getDefaultTreeData = () => ({
  name: '根节点',
  children: [
    { 
      name: '分支A', 
      value: 30,
      children: [
        { name: 'A1', value: 15 },
        { name: 'A2', value: 15 }
      ]
    },
    { 
      name: '分支B', 
      value: 40,
      children: [
        { name: 'B1', value: 20 },
        { name: 'B2', value: 15 },
        { name: 'B3', value: 5 }
      ]
    },
    { name: '分支C', value: 30 }
  ]
})

// ============ 构建树配置 ============
const buildTreeOption = (data) => {
  const treeData = data || getDefaultTreeData()
  
  // 基础配置
  const baseOption = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
      formatter: (params) => {
        const { name, value } = params.data
        return `<strong>${name}</strong><br/>值：${value || '--'}`
      }
    },
    title: {
      text: '树形结构图',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#fff'
      }
    },
    series: [
      {
        type: 'tree',
        draggable:true,
        data: [treeData],
        // 布局配置
        top: '8%',
        left: '7%',
        bottom: '5%',
        right: '20%',
        orient: 'BT',
        // 节点样式
        // symbol: 'circle',
        // symbolSize: 100,
        itemStyle: {
          color: 'pink',
          borderColor: '#fff',
          borderWidth: 2
        },
        
        // 标签配置
        label: {
          position: 'left',
          verticalAlign: 'middle',
          align: 'right',
          fontSize: 12,
          color: 'yellow' ,
          fontWeight: 500
        },
        
        // 叶子节点标签
        leaves: {
          label: {
            position: 'right',
            verticalAlign: 'middle',
            align: 'left',
            fontSize: 12,
            color: 'blue' 
          }
        },
        
        // 连线样式
        lineStyle: {
          color: 'red',
          width: 2,
          curveness: 0.5
        },
        
        // 交互
        emphasis: {
          focus: 'descendant',
          lineStyle: {
            width: 3,
            color: '#5470c6'
          }
        },
        
        // 展开/折叠
        expandAndCollapse: true,
        initialTreeDepth: 2,
        
        // 动画
        animationDuration: 550,
        animationDurationUpdate: 750,
        animationEasing: 'cubicOut',
        animationEasingUpdate: 'cubicOut',
        
        // 标签布局（防止重叠）
        labelLayout: {
          hideOverlap: true
        }
      }
    ]
  }
  
  // 合并自定义配置（深度合并）
  return baseOption
}

// ============ 初始化图表 ============
const initChart = async () => {
  if (!chartContainer.value) return
  
  await nextTick()
  
  try {
    // 销毁旧实例
    if (chartInstance) {
      chartInstance.dispose()
      chartInstance = null
    }
    
    // 创建新实例
    chartInstance = echarts.init(chartContainer.value, props.theme)
    
    // 构建配置并渲染
    const option = buildTreeOption(props.data)
    chartInstance.setOption(option, true)
    
    // 触发ready事件
    emit('ready', chartInstance)
    
    // 设置响应式
    if (props.responsive) {
      setupResizeObserver()
    }
    
    // 绑定点击事件
    chartInstance.on('click', (params) => {
      emit('click', params)
    })
    
  } catch (error) {
    console.error('ECharts 初始化失败:', error)
  }
}

// ============ 响应式处理 ============
const setupResizeObserver = () => {
  // 使用 ResizeObserver（更精确）
  if (window.ResizeObserver && chartContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      handleResize()
    })
    resizeObserver.observe(chartContainer.value)
  } else {
    // 降级方案：监听窗口变化
    window.addEventListener('resize', handleResize)
  }
}

const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
    emit('resize')
  }
}

// ============ 数据更新 ============
const updateData = (data) => {
  if (!chartInstance) return
  
  try {
    const option = buildTreeOption(data)
    chartInstance.setOption(option, true)
  } catch (error) {
    console.error('更新数据失败:', error)
  }
}

// ============ 导出实例 ============
const getChartInstance = () => chartInstance

// ============ 暴露方法 ============
defineExpose({
  updateData,
  getChartInstance,
  resize: handleResize,
  dispose: () => {
    if (chartInstance) {
      chartInstance.dispose()
      chartInstance = null
    }
  }
})

// ============ 生命周期 ============
onMounted(() => {
  initChart()
})

// 监听数据变化
watch(() => props.data, (newData) => {
  updateData(newData)
}, { deep: true })

// 监听主题变化
watch(() => props.theme, () => {
  initChart()
})

onBeforeUnmount(() => {
  // 清理ResizeObserver
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  
  // 移除窗口事件
  window.removeEventListener('resize', handleResize)
  
  // 销毁图表
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-width: 400px;
  min-height: 400px; /* 设置最小高度 */
  background-color: white; 
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