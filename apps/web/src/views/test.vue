<template>
    <div class="test1" ref="chartContainer1" >
        <div class="test2" ref="chartContainer2" ></div>
    </div>
    
    <graph :data="nodesData" :layout="layout" ></graph>
</template>
<script setup>
import data from '@/data/self.json'
import data1 from '@/data/graph.json'
import { onMounted,ref,nextTick } from 'vue';
import { getWorld,getNodes } from '@/api/simple_api'
import graph from '../components/graph.vue';
import * as echarts from 'echarts';
const chartContainer1 = ref(null)
const chartContainer2 = ref(null)
const layout = ref('force')
let myChart1 = null
let myChart2 = null
const nodesData=ref(null)
const graphData=ref(null)
onMounted(async()=>{
    // console.log(data['pay']['$count']-data['income']['$count'])
    graphData.value=await getWorld()
    nodesData.value=await getNodes()
    // data1['series'][0]['data']=graphData.value
    // data1['series'][1]['data']=nodesData.value
    // console.log(data1)
    myChart1 = echarts.init(chartContainer1.value)
    myChart2 = echarts.init(chartContainer2.value)
    const option = {
    title: {
      text: 'ttt',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    toolbox: {
      top:10,
      left:10
      
    },
    series: [{
      type: 'graph',
      layout: 'force',
      draggable:true,    
      symbolSize: 100,
      roam: true,
      label: {
        show: true
      },
      data: nodesData.value,  // 使用传入的数据
      // data:[{name:'xxx',value:'xxx',symbolSize:10,Symbol:'rect'}],
    //   links: props.link,  // 可以根据需要从props传入
      links:[],
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0
      },
      force: {
        initLayout: 'circular',
        gravity: 0.1,
        repulsion: 1000
      }
    }],
  }
  
  // 设置选项并立即渲染
  myChart1.setOption(option)
  myChart2.setOption(option)
})
</script>

<style>
.test1{
    width: 800px;
    height: 400px;
    background-color: yellow;
    border-radius: 50%;
    display: flex;
    justify-content: center;  /* 水平居中 */
    align-items: center; 
}
.test2{
    width: 600px;
    height: 100px;
    background-color: pink;
    border-radius: 50%;
    /* mix-blend-mode:screen; */
    /* padding:10px; */
    /* top:10px */
}
</style>