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
import { onMounted, ref, watch } from 'vue'; // 添加 ref 导入
import * as echarts from 'echarts';

const props = defineProps({
  title_list: {
    type: Array
  },
  option_list: {
    type: Array
  }
})
const emit = defineEmits(['chart-ready','data-loaded', 'error', 'node-click']);

// 响应式变量
const chartContainer = ref(null);
const myChart = ref(null);
const error = ref(null);
const loading = ref(false);

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return;
  if (myChart.value) {
    myChart.value.dispose();
  }
  
  myChart.value = echarts.init(chartContainer.value);
  var option;
  
  // 检查是否有数据
  if (props.option_list ) {
    option = {
      baseOption: {
          timeline: {
              show: true,
              axisType: 'category',
              autoPlay: false,
              playInterval: 1500,
              data: props.title_list
          },
          title: {
              text: 'vue 生命周期举例演示'
          },
          // 其他基础配置
      },
      options: props.option_list
    }
    myChart.value.setOption(option);
    emit('data-loaded');
  } else {
    error.value = '暂无数据';
  }
}

// 监听数据变化
watch(() => props.option_list, (newData) => {
  if (newData && myChart.value) {
    myChart.value.setOption(newData, true); // true 表示不合并，完全替换
  }
}, { deep: true });

onMounted(() => {
  initChart();
});

// 窗口大小自适应
window.addEventListener('resize', () => {
  if (myChart.value) {
    myChart.value.resize();
  }
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
  height: 600px;
}
.loading, .error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.error {
  color: red;
}
</style>