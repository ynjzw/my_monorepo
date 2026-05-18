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
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';

const props = defineProps({
  data: {
    type: Array,
    default: () => []  // 提供默认值
  }
})

// 将初始化逻辑包装在 onMounted 中
onMounted(() => {
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option;
  option = {
    title: {
      text: 'Funnel',
      left: 'left',
      top: 'bottom'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c}%'
    },
    toolbox: {
      orient: 'vertical',
      top: 'center',
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: props.data.name
    },
    series: [
      {
        name: 'Funnel',
        type: 'funnel',
        data: props.data
      }
    ]
  };
  option && myChart.setOption(option);
});
</script>
<style>
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
  height: 100%;
  min-height: 400px; /* 设置最小高度 */
  min-width: 400px; 
}
</style>