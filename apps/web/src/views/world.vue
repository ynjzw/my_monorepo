
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
import { get_solar } from '../api';

const chartContainer = ref(null)
let myChart = null
const loading = ref(false)
const error = ref(null)
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
    
    
  } catch (err) {
    console.error('图表初始化失败:', err)
    error.value = '图表初始化失败'
  }
}

// 更新图表选项
const updateChartOptions = () => {
  if (!myChart) return
  
  const data = await get_solar()
  const option = {
    series: [{
      type: 'graph',
      layout: 'none',
      draggable:true,    
      symbolSize: 50,
      roam: true,
      label: {
        show: true
      },
      data: data,  // 使用传入的数据
      links: [],  // 可以根据需要从props传入
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0
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
      text: '太阳系',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
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

const bindEvents = () => {
  if (!myChart.value) return;
  myChart.on('click',(params)=>{
    s
  })
  // 节点点击事件
  myChart.value.on('click', { seriesIndex: 0 }, (params) => {
    drillDown(params.data.id);
  });
};

const drillDown=(targetNodeId)=>{
  displayRoot.value = stratifyData();
  let rawData;
  rawData = happy;
  const result = prepareData(rawData);
  seriesData.value = result.seriesData;
  maxDepth.value = result.maxDepth;
  
  initChart();
  if (targetNodeId) {
    displayRoot.value = displayRoot.value.descendants().find(
      (node) => node.data.id === targetNodeId
    );
  }
  if (displayRoot.value) {
    displayRoot.value.parent = null;
    // 更新当前深度
    currentDepth.value = displayRoot.value.depth;
    // 刷新图表
    myChart.value.setOption({
      dataset: {
        source: seriesData.value
      }
    });
  }
}
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
  min-height: 400px; /* 设置最小高度 */
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

</style>