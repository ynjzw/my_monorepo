<template>
  
  <div id="main" ></div>
</template>

<script setup >
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
// 将初始化逻辑包装在 onMounted 中
onMounted(() => {
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option;
  option = {
    title: {
      text: '马斯洛需求层次理论'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c}%'
    },
    series: [
      {
        name: '马斯洛需求层次理论',
        type: 'funnel',
        sort: 'ascending',
        data: [
          { value: 5, name: '自我实现需求' },
          { value: 15, name: '尊重需求' },
          { value: 20, name: '社交需求' },
          { value: 25, name: '安全需求' },
          { value: 35, name: '生理需求' }
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