<template>
  
  <level_oneVue />
</template>

<script setup >
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
import level from '../components/level.vue';
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
      data: ['Show', 'Click', 'Visit', 'Inquiry', 'Order']
    },
    series: [
      {
        name: 'Funnel',
        type: 'funnel',
        data: [
          { value: 60, name: 'Visit' },
          { value: 30, name: 'Inquiry' },
          { value: 10, name: 'Order' },
          { value: 80, name: 'Click' },
          { value: 100, name: 'Show' },
          { value: 100, name: 'Click' }
        ]
      }
    ]
  };
  option && myChart.setOption(option);
});
</script>

<style>
#main{
  width: 400px; 
  height: 400px;

}
</style>