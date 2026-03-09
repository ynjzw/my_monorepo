<template>
  
  <div id="main" ></div>
</template>

<script setup >
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
import { get_base_nodes,get_maslow_needs } from '../api/index';
// 将初始化逻辑包装在 onMounted 中
onMounted(async() => {
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  const maslow_needs = await get_maslow_needs();
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
        data: maslow_needs
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