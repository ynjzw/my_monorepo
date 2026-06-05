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
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';

const props = defineProps({
  data: {
    type: Array,
    default: () => []  // 提供默认值
  }
})
const emit = defineEmits(['chart-ready','data-loaded', 'error', 'node-click']);

// 响应式变量
const chartContainer = ref(null);
const myChart = ref(null);
const seriesData = ref([]);
const error = ref(null);
const loading = ref(false);
onMounted(() => {
  if (!chartContainer.value) return;
  if (myChart.value) {
    myChart.value.dispose();
  }
    // 创建新图表实例
  myChart.value = echarts.init(chartContainer.value);
  var option;
  option = {
      baseOption: {
          timeline: {
              show: true,
              axisType: 'category',
              autoPlay: false,
              playInterval: 1500,
              data: ['当地人口结构','人口类型分布']
          },
          title: {
              text: '地区生活水平重点指标',
              subtext: '2021.5.30'
          },
          // 其他基础配置
      },
      options: props.data
  };
  option && myChart.setOption(option);
});
</script>