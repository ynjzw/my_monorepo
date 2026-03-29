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
  // 为节点添加不同颜色
  const colors = ['#ff7f50', '#87cefa', '#daa520', '#32cd32', '#ba55d3', '#ff69b4', '#20b2aa', '#ff6347', '#00ced1', '#dc143c'];
  base_nodes.forEach((node, index) => {
    node.itemStyle = {
      color: colors[index % colors.length]
    };
  });
  // console.log(world)
  const option = {
    series: [
                {
                  type: 'graph',
                  layout: 'force',
                  roam: true,
                  symbolSize: 20,
                  label: {
                    show: true,
                    position: 'bottom',
                    fontSize: 12
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
                    gravity: 0.5,
                    repulsion: 1000,
                    edgeLength: 100,
                    layoutAnimation: true
                  }
                }
            ]
  };
  myChart.setOption(option);
  myChart.on('click', function (params) {
    console.log(params.data.value)
    // const value=params.data.value
    // router.push(value)
  });
});
</script>

<style>
#main{
  width: 1280px; 
  height: 400px;

}
</style>