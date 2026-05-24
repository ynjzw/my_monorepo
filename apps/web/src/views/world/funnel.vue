// funnel.vue - 漏斗图组件（完善版）
<template>
  <div class="funnel-wrapper">
    <div class="funnel-header">
      <h3 class="funnel-title">{{ title }}</h3>
      <div class="funnel-actions">
        <button @click="refreshData" class="refresh-btn" title="刷新数据">
          🔄
        </button>
      </div>
    </div>
    <div 
      ref="chartContainer" 
      class="funnel-container"
      :class="{ 'loading-overlay': loading }"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!hasData && !loading" class="no-data">
      <span>暂无数据</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: '数据漏斗图'
  }
});

const chartContainer = ref(null);
let chartInstance = null;
const loading = ref(false);
const error = ref('');

const hasData = computed(() => {
  return props.data && Array.isArray(props.data) && props.data.length > 0;
});

// 刷新数据
const refreshData = () => {
  if (chartInstance && hasData.value) {
    updateChart();
  }
};

// 格式化漏斗图数据
const formatData = () => {
  if (!hasData.value) return [];
  
  // 确保数据有正确的格式
  return props.data.map(item => ({
    name: item.name || '未知',
    value: typeof item.value === 'number' ? item.value : 0
  })).sort((a, b) => b.value - a.value); // 按值降序排列
};

// 更新图表配置
const updateChart = () => {
  if (!chartInstance || !hasData.value) return;
  
  const formattedData = formatData();
  const maxValue = Math.max(...formattedData.map(d => d.value), 100);
  
  const option = {
    title: {
      show: props.title ? true : false,
      text: props.title,
      left: 'center',
      top: 0,
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const percent = ((params.value / maxValue) * 100).toFixed(1);
        return `${params.name}<br/>数值：${params.value}<br/>占比：${percent}%`;
      },
      backgroundColor: 'rgba(0,0,0,0.7)',
      borderColor: '#333',
      borderWidth: 0,
      textStyle: {
        color: '#fff'
      }
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: formattedData.map(item => item.name),
      textStyle: {
        fontSize: 12
      },
      formatter: (name) => {
        const item = formattedData.find(d => d.name === name);
        return `${name} : ${item?.value || 0}`;
      }
    },
    series: [
      {
        name: '漏斗图',
        type: 'funnel',
        left: '15%',
        width: '70%',
        sort: 'descending', // 降序排列
        gap: 2, // 间距
        label: {
          show: true,
          position: 'inside',
          formatter: '{b} : {d}%',
          fontSize: 12,
          fontWeight: 'bold'
        },
        labelLine: {
          length: 10,
          lineStyle: {
            width: 1,
            type: 'solid'
          }
        },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 1,
          borderRadius: 8
        },
        emphasis: {
          label: {
            fontSize: 14,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        data: formattedData
      }
    ],
    color: ['#5470c6', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
    graphic: !hasData.value ? [
      {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: '暂无数据',
          fill: '#999',
          fontSize: 14
        }
      }
    ] : []
  };
  
  chartInstance.setOption(option, true);
};

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return;
  
  if (chartInstance) {
    chartInstance.dispose();
  }
  
  chartInstance = echarts.init(chartContainer.value);
  
  if (hasData.value) {
    updateChart();
  } else {
    // 显示空状态
    chartInstance.setOption({
      title: {
        show: true,
        text: props.title,
        left: 'center',
        top: 0
      },
      graphic: [
        {
          type: 'text',
          left: 'center',
          top: 'middle',
          style: {
            text: '暂无数据',
            fill: '#999',
            fontSize: 14
          }
        }
      ]
    });
  }
};

// 监听数据变化
watch(() => props.data, (newData, oldData) => {
  if (chartInstance) {
    if (newData && newData.length > 0) {
      updateChart();
      error.value = '';
    } else {
      // 清空图表显示空状态
      chartInstance.setOption({
        series: [{ data: [] }],
        graphic: [
          {
            type: 'text',
            left: 'center',
            top: 'middle',
            style: {
              text: '暂无数据',
              fill: '#999',
              fontSize: 14
            }
          }
        ]
      });
    }
  }
}, { deep: true });

// 监听标题变化
watch(() => props.title, () => {
  if (chartInstance && hasData.value) {
    updateChart();
  }
});

// 窗口适配
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};

onMounted(() => {
  initChart();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.funnel-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
}

.funnel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e9ecef;
  background: #fafbfc;
}

.funnel-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.funnel-actions {
  display: flex;
  gap: 8px;
}

.refresh-btn {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.refresh-btn:hover {
  background: #f0f0f0;
  opacity: 1;
  transform: rotate(180deg);
}

.funnel-container {
  flex: 1;
  width: 100%;
  min-height: 400px;
  transition: opacity 0.3s ease;
}

.funnel-container.loading-overlay {
  opacity: 0.6;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  z-index: 10;
  font-size: 14px;
}

.error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(220, 53, 69, 0.9);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  z-index: 10;
  font-size: 14px;
}

.no-data {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #adb5bd;
  font-size: 14px;
  background: #f8f9fa;
  padding: 20px 30px;
  border-radius: 8px;
  text-align: center;
}
</style>