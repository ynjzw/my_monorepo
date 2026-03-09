<template>
    <div id='main'></div>
</template>

<script setup>
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
import { get_base_nodes,get_maslow_needs } from '../api/index';
onMounted(() => {
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option;
  option = {
        xAxis:{
            type:'time',
            axisLabel:{
                formatter:'{yyyy}-{MM}-{dd}'
            }
        },
        yAxis:{
            type:'value'
        },
        series:[{
            type:'line',
            data:[
                [new Date('2022-01-01'),10],
                [new Date('2022-01-02'),20],
                [new Date('2022-01-03'),30],
                [new Date('2022-01-04'),40],
                [new Date('2022-01-05'),50],
                [new Date('2022-01-06'),60]
            ]
        }]
    };
  option && myChart.setOption(option);
});
</script>