<script setup>
import { onMounted, ref } from 'vue';
import * as echarts from 'echarts';

const props=defineProps({
    data:Array,
    msg:String
})
onMounted(async ()=>{
    const chartDom = document.getElementById('main');
  console.log(props.data)
    // 增加逻辑判断防止报错
    if (!chartDom) return;

    const myChart = echarts.init(chartDom);
    
    const option = {
                series: [
                    {
                    type: 'graph',
                    layout: 'none',
                    symbolSize: 50,
                    roam: true,
                    label: {
                        show: true
                    },
                    data: props.data,
                    links: [],
                    // links: links,
                    lineStyle: {
                        opacity: 0.9,
                        width: 2,
                        curveness: 0
                    }
                    }
                ]
    };

    myChart.setOption(option);
})
</script>

<template>
    <div id="main" ></div>
    <p>{{ props.msg }}</p>
</template>