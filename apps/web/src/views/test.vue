<template>
    <div  class="color-wheel">
        <div class="circle test1"  ></div>
        <div class="circle test2"  ></div>
        <div class="circle test3"  ></div>
    </div>
    
</template>
<script setup>
import data from '@/data/self.json'
import data1 from '@/data/graph.json'
import { onMounted,ref,nextTick } from 'vue';
import { getWorld,getNodes } from '@/api/simple_api'
import graph from '../components/graph.vue';
import * as echarts from 'echarts';
const layout = ref('force')
let myChart1 = null
let myChart2 = null
let nodesData=ref(null)
let graphData=ref(null)
let nodes = []
onMounted(async()=>{
    // console.log(data['pay']['$count']-data['income']['$count'])
    graphData.value=await getWorld()
    nodesData.value=await getNodes()
    for (let j = 1; j <= 2; j++) {
        nodes.push({
            id: j,
            name: `Node ${j}`,
        });
    }
    // data1['series'][0]['data']=graphData.value
    // data1['series'][1]['data']=nodesData.value
    // console.log(data1)
  //   myChart1 = echarts.init(chartContainer1.value)
  //   myChart2 = echarts.init(chartContainer2.value)
  //   const option = {
  //   title: {
  //     text: 'ttt',
  //     left: 'center',
  //     top: 10,
  //     textStyle: {
  //       fontSize: 14,
  //       fontWeight: 'normal'
  //     }
  //   },
  //   toolbox: {
  //     top:10,
  //     left:10
      
  //   },
  //   series: [{
  //     type: 'graph',
  //     layout: 'force',
  //     draggable:true,    
  //     symbolSize: 100,
  //     roam: true,
  //     label: {
  //       show: true
  //     },
  //     data: [],  // 使用传入的数据
  //     // data:[{name:'xxx',value:'xxx',symbolSize:10,Symbol:'rect'}],
  //   //   links: props.link,  // 可以根据需要从props传入
  //     links:[],
  //     lineStyle: {
  //       opacity: 0.9,
  //       width: 2,
  //       curveness: 0
  //     },
  //     force: {
  //       initLayout: 'circular',
  //       gravity: 0.1,
  //       repulsion: 1000
  //     }
  //   }],
  // }
  
  // 设置选项并立即渲染
  // myChart1.setOption(option)
  // myChart2.setOption(option)
})
</script>

<style>
.color-wheel {
    position: relative;
    width: 400px;
    height: 350px;
    /* 关键点：混合模式需要一个纯黑的底色作为“发光”的基础 */
    background-color: #000; 
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 基础圆形样式 */
.circle {
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    /* 核心属性：滤色模式（加光混合） */
    mix-blend-mode: screen; 
}
.test1{
    background-color: red;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
}
.test2{
    bottom: 20px;
    left: 20px;
    background-color: green;
}
.test3{
    bottom: 20px;
    right: 20px;
    background-color: blue;
}
</style>