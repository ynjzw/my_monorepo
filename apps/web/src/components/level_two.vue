<script setup>
import { onMounted, ref } from 'vue';
import { getFamily,getLinks } from '../api';
import * as echarts from 'echarts';

const node=ref([]);
const links=ref([])
onMounted(async ()=>{
    const node = await getFamily();
    const links = await getLinks();
    const chartDom = document.getElementById('main');
  
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
                    data: node,
                    // links: [],
                    links: links,
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
</template>