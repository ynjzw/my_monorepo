// funnel.vue - 添加 loading prop
<script setup>
import { onMounted,ref,computed,watch,onUnmounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
// 在 props 中添加 loading
const loading = ref(false)
const props = defineProps({
  data: {
    type: Array,
    default: () => [{name:'hhhh'}]
  },
  title: {
    type: String,
    default: '数据漏斗图'
  },
  loading: {  // 添加 loading prop
    type: Boolean,
    default: false
  }
});

// 在模板中使用 loading 状态
// 注意：需要在 template 中使用 props.loading 而不是本地的 loading
const chartContainer = ref(null);
let chartInstance = null;
const error = ref(null)

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
  return props.data
};

// 更新图表配置
const updateChart = () => {
  if (!chartInstance || !hasData.value) return;
  
  const formattedData = formatData();
  // const maxValue = Math.max(...formattedData.map(d => d.value), 100);
  
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
    // tooltip: {
    //   trigger: 'item',
    //   // formatter: (params) => {
    //   //   const percent = ((params.value / maxValue) * 100).toFixed(1);
    //   //   return `${params.name}<br/>数值：${params.value}<br/>占比：${percent}%`;
    //   // },
    //   backgroundColor: 'rgba(0,0,0,0.7)',
    //   borderColor: '#333',
    //   borderWidth: 0,
    //   textStyle: {
    //     color: '#fff'
    //   }
    // },
    // legend: {
    //   orient: 'vertical',
    //   left: 'left',
    //   data: formattedData.map(item => item.name),
    //   textStyle: {
    //     fontSize: 12
    //   },
    //   formatter: (name) => {
    //     const item = formattedData.find(d => d.name === name);
    //     return `${name} : ${item?.value || 0}`;
    //   }
    // },
    series: [
      {
        name: '漏斗图',
        type: 'funnel',
        // left: '15%',
        width: '50%',
        sort: 'none', // 降序排列
        // gap: 2, // 间距
        label: {
          show: true,
          position: 'inside',
          formatter: '{b} : {d}%',
          fontSize: 12,
          fontWeight: 'bold'
        },
        // labelLine: {
        //   length: 10,
        //   lineStyle: {
        //     width: 1,
        //     type: 'solid'
        //   }
        // },
        // itemStyle: {
        //   borderColor: '#fff',
        //   borderWidth: 1,
        //   borderRadius: 8
        // },
        // emphasis: {
        //   label: {
        //     fontSize: 14,
        //     fontWeight: 'bold'
        //   },
        //   itemStyle: {
        //     shadowBlur: 10,
        //     shadowOffsetX: 0,
        //     shadowColor: 'rgba(0, 0, 0, 0.5)'
        //   }
        // },
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

onMounted(async() => {
  initChart();
  window.addEventListener('resize', handleResize);
  await console.log(props.data)
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  window.removeEventListener('resize', handleResize);
});
</script>

<template>
  <p>xxx</p>
  <div class="funnel-wrapper">
    <div class="funnel-header">
      <h3 class="funnel-title">{{ title }}</h3>
    </div>
    <p>xxx</p>
    <div 
      ref="chartContainer" 
      class="funnel-container"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">error</div>
  </div>
</template>

<style>
.loading {
  text-align: center;
  padding: 20px;
}
.error {
  color: red;
}
.funnel-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.funnel-container {
  width: 200px;
  height: 300px;
}
</style>