
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


<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import * as echarts from 'echarts';
import * as d3 from 'd3-hierarchy';

// props & emits
const data = {
                "$count": 100,
                "happy": { "$count": 50 },
                "angry": { "$count": 50 },
                "fear": { "$count": 20 },
                "sad": { "$count": 20 }
              };
const happy = {                
                "ss": { "$count": 40 },
                "dd": { "$count": 35 },
                "aa": { "$count": 35 },
                "zz": { "$count": 40 }
              };
const angry = {                
                "ss": { "$count": 40 },
                "dd": { "$count": 35 },
                "aa": { "$count": 35 },
                "zz": { "$count": 40 }
              };
const fear = {                
                "ss": { "$count": 40 },
                "dd": { "$count": 35 },
                "aa": { "$count": 35 },
                "zz": { "$count": 40 }
              };
const sad = {                
                "ss": { "$count": 40 },
                "dd": { "$count": 35 },
                "aa": { "$count": 35 },
                "zz": { "$count": 40 }
              };                           
const emit = defineEmits(['chart-ready','data-loaded', 'error', 'node-click']);

// 响应式变量
const chartContainer = ref(null);
const myChart = ref(null);
const seriesData = ref([]);
const maxDepth = ref(0);
const displayRoot = ref(null);
const currentDepth = ref(0);
const error = ref(null);
const loading = ref(false);
// 准备数据
const prepareData = (rawData) => {
  const dataArr = [];
  let depth = 0;
  const convert = (source, basePath, currentDepth) => {
    if (source == null) return;
    if (depth > 5) return;
    depth = Math.max(currentDepth, depth);
      if (basePath=='root'){
        dataArr.push({
          id: basePath,
          value: source.$count ,
          depth: currentDepth,
          index: dataArr.length
        });
    } else {
      dataArr.push({
        id: basePath,
        value: source.$count + 5,
        depth: currentDepth,
        index: dataArr.length
      });
    }
    
    for (const key in source) {
      if (Object.prototype.hasOwnProperty.call(source, key) && !key.match(/^\$/)) {
        const path = basePath + '.' + key;
        convert(source[key], path, currentDepth + 1);
      }
    }
  };
  convert(rawData, 'root', 0);
  // console.log(dataArr,depth)
  return {
    seriesData: dataArr,
    maxDepth: depth
  };
};

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return;
  try {
    // 如果已存在图表实例，先销毁
    if (myChart.value) {
      myChart.value.dispose();
    }
    // 创建新图表实例
    myChart.value = echarts.init(chartContainer.value);
    // 创建层级结构
    displayRoot.value = stratifyData();
    // 设置图表选项
    const option = createChartOption();
    myChart.value.setOption(option);
    bindEvents();
    emit('chart-ready', myChart)
  } catch (err) {
    console.error('图表初始化失败:', err);
    error.value = '图表初始化失败';
    emit('error', err);
  }
};

// 创建层级数据
const stratifyData = () => {
  return d3
    .stratify()
    .parentId((d) => {
      const lastDotIndex = d.id.lastIndexOf('.')
      return lastDotIndex > 0 ? d.id.substring(0, lastDotIndex) : null
    })(seriesData.value)
    .sum((d) => d.value || 0)
    .sort((a, b) => b.value - a.value);
};

// 创建图表配置
const createChartOption = () => {
  const overallLayout = (params, api) => {
    const context = params.context;
    d3
      .pack()
      .size([api.getWidth() - 2, api.getHeight() - 2])
      .padding(3)(displayRoot.value);
    context.nodes = {};
    displayRoot.value.descendants().forEach((node) => {
      context.nodes[node.id] = node;
    });
  };
  const renderItem = (params, api) => {
    const context = params.context;
    if (!context.layout) {
      context.layout = true;
      overallLayout(params, api);
    }
    const nodePath = api.value('id');
    // console.log(params, api)
    const node = context.nodes[nodePath];
    if (!node) return;
    const isLeaf = !node.children || !node.children.length;
    const focus = new Uint32Array(
      node.descendants().map((n) => n.data.index)
    );
    const nodeName = isLeaf
      ? nodePath
          .slice(nodePath.lastIndexOf('.') + 1)
          .split(/(?=[A-Z][^A-Z])/g)
          .join('\n')
      : '';
    const z2 = api.value('depth') * 2;
    return {
      type: 'circle',
      focus: focus,
      shape: {
        cx: node.x,
        cy: node.y,
        r: node.r
      },
      transition: ['shape', 'style'],
      z2: z2,
      textContent: {
        type: 'text',
        style: {
          text: nodeName,
          fontFamily: 'Arial',
          width: node.r * 1.3,
          overflow: 'truncate',
          fontSize: 15
        },
        emphasis: {
          style: {
            overflow: null,
            fontSize: 20
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
          fontSize: 20
          // fill: api.visual('color', { emphasis: true })
        },
        focus: 'self'
      }
    };
  };
  return {
    dataset: {
      source: seriesData.value
    },
    toolbox: {
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    visualMap: [
      {
        show: true,
        min: 0,
        max: maxDepth.value,
        dimension: 'depth'
      }
    ],
    hoverLayerThreshold: Infinity,
    title: {
      text: '情绪-右脑',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        color: 'white',
        fontWeight: 'normal'
      }
    },
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
  };
};

// 绑定事件
const bindEvents = () => {
  if (!myChart.value) return;
  // 节点点击事件
  myChart.value.on('click', { seriesIndex: 0 }, (params) => {
    drillDown(params.data.id);
    emit('node-click', params);
  });
  // 空白区域点击（重置）
  myChart.value.getZr().on('click', (event) => {
    if (!event.target) {
      resetView();
    }
  });
};

// 下钻功能
const drillDown = (targetNodeId) => {
  displayRoot.value = stratifyData();
  
  let rawData;
  rawData = happy;
  const result = prepareData(rawData);
  seriesData.value = result.seriesData;
  maxDepth.value = result.maxDepth;
  emit('data-loaded', result);
  
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
};

// 重置视图
const resetView = () => {
  displayRoot.value = stratifyData();
  currentDepth.value = 0;
  myChart.value.setOption({
    dataset: {
      source: seriesData.value
    }
  });
};

// 加载数据
const loadData = async () => {
  loading.value = true;
  error.value = null;
  try {
    let rawData;
    rawData = data;
    await new Promise(resolve => setTimeout(resolve, 500));
    const result = prepareData(rawData);
    seriesData.value = result.seriesData;
    maxDepth.value = result.maxDepth;
    emit('data-loaded', result);
    await nextTick();
    initChart();
  } catch (err) {
    console.error('数据加载失败:', err);
    error.value = '数据加载失败: ' + err.message;
    emit('error', err);
  } finally {
    loading.value = false;
  }
};

// 重试加载
const retryLoad = () => {
  loadData();
};

// 更新图表尺寸
const handleResize = () => {
  if (myChart.value) {
    myChart.value.resize();
  }
};

// 监听容器尺寸变化
const setupResizeObserver = () => {
  if (!chartContainer.value) return;
  const resizeObserver = new ResizeObserver(() => {
    handleResize();
  });
  resizeObserver.observe(chartContainer.value);
  return resizeObserver;
};

// 定时器引用
let intervalId = null;

// 内圆动画参数
let direction = 1; // 1: 增大, -1: 减小
let innerValue = 20;

onMounted(() => {
  loadData();
  window.addEventListener('resize', handleResize);
  const observer = setupResizeObserver();
  console.log(eval(Object.keys(data)[2]));
  
  // 动画：一级节点 value 在 20~50 之间来回变化
  intervalId = setInterval(() => {
    
    if (seriesData.value && seriesData.value.length > 0) {
      // 只调整 depth === 1 的节点
      if (direction === 1) {
        innerValue += 3;
        if (innerValue >= 50) {
          innerValue = 50;
          direction = -1;
        }
      } else {
        innerValue -= 3;
        if (innerValue <= 20) {
          innerValue = 20;
          direction = 1;
        }
      }
      seriesData.value = seriesData.value.map(item => {
        if (item.depth === 1) {
          return { ...item, value: innerValue };
        }
        return item;
      });
      if (myChart.value) {
        myChart.value.setOption({
          dataset: {
            source: seriesData.value
          }
        });
      }
    }
    // console.log(seriesData.value)
  }, 10);

  // 清理函数
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
    if (observer) {
      observer.disconnect();
    }
    if (myChart.value) {
      myChart.value.dispose();
      myChart.value = null;
    }
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  });
});

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