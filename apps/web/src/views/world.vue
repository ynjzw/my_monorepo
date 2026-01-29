<template>
  <div id="main" ></div>
</template>

<script setup >
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
import {getWorld} from '../api';
import { useRouter } from 'vue-router';

// 将初始化逻辑包装在 onMounted 中
onMounted(async() => {
  const router=useRouter()
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  const world = await getWorld();
  // console.log(world)
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
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 10],
                    edgeLabel: {
                        fontSize: 20
                    },
                    data: world,
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
  myChart.on('click', function (params) {
    // console.log(params.data.value)
    const value=params.data.value
    router.push(value)
  });
});
</script>

<style>
#main{
  width: 800px; 
  height: 800px;

}
</style>