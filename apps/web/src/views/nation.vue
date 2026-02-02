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
      data: ['亿万富翁', '千万富翁', '百万富翁', '年收入十万以上', '其他']
    },
    series: [
      {
        name: 'Funnel',
        type: 'funnel',
        sort: 'ascending',
        data: [
          { value: 1, name: '亿万富翁' },
          { value: 2, name: '千万富翁' },
          { value: 2, name: '百万富翁' },
          { value: 15, name: '年收入十万以上' },
          { value: 80, name: '其他' }
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