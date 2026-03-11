<template>
  <div id="main" ></div>
</template>

<script setup >
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
import {get_base_nodes} from '@/api';
import { useRouter } from 'vue-router';

// 将初始化逻辑包装在 onMounted 中
onMounted(async() => {
  const router=useRouter()
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  const base_nodes = await get_base_nodes();
  // console.log(world)
  const option = {
    series: [
                  {
                    type: 'graph',
                    layout: 'force',
                    roam: true,
                    label: {
                        show: true
                    },
                    // edgeSymbol: ['circle', 'arrow'],
                    // edgeSymbolSize: [4, 10],
                    // edgeLabel: {
                    //     fontSize: 20
                    // },
                    data: base_nodes,
                    links: [],
                    // links: links,
                    force: {
                      initLayout: 'circular',
                      gravity: 0.2,
                      repulsion: 30
                    }
                  }
            ]
  };
  myChart.setOption(option);
  myChart.on('click', function (params) {
    // console.log(params.data.value)
    const value=params.data.value
    router.push(value)
  });
});
</script>

<style>
#main{
  width: 1280px; 
  height: 400px;

}
</style>