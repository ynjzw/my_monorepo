<template>
    <div ref="mapRef1" class="map-container1">
        <div ref="mapRef2" class="map-container2"></div>
    </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const mapRef1 = ref(null);
const mapRef2 = ref(null);
let chart1 = null;       // 存储图表实例
let chart2 = null;       // 存储图表实例
let intervalId = null;   // 存储定时器ID
let nodes = [];          // 存储节点数据，供定时器使用
let links = [];     

onMounted(async () => {
    // 初始化图表
    chart1 = echarts.init(mapRef1.value);
    chart2 = echarts.init(mapRef2.value);
    // 生成100个节点
    nodes = [];
    for (let i = 1; i <= 50; i++) {
        nodes.push({
            id: i,
            name: `Node ${i}`,
            itemStyle: {
                color: i <= 25 ? 'blue' : 'red', // 前25个节点为蓝色，后25个节点为红色
            },
        });
    }
    let i=1
    let j=50
    while(i<=25){
        links.push({
            source: i,
            target: 50-i+1,
        });
        links.push({
            source: i,
            target: i+1,
        });
        links.push({
            source: 50-i+1,
            target: 50-i,
        });
        i++
        j--
    }
    var option1={
        title: { 
            text: 'ttt' 
        },
        series: [
            {
            type: 'graph',
            layout: 'force',
            data: nodes,
            links: links,
            roam: true,
            draggable:true,
            label: { show: false, position: 'bottom', fontSize: 12 },
            force: { 
                repulsion: 100, 
                edgeLength: 150,
                gravity: 0.3,
                friction: 0.1
            }
        },
        {
            type: 'graph',
            layout: 'force',
            data: nodes,
            links: [],
            roam: true,
            draggable:true,
            label: { show: false, position: 'bottom', fontSize: 12 },
            force: {
              initLayout: 'circular',
              gravity: 0.1,
              repulsion: 1000
            }
        }
        ]
    }
    option1 && chart1.setOption(option1);

    var option2={
        title: { 
            text: 'ttt' 
        },
        series: [
            {
            type: 'graph',
            layout: 'circular',
            data: nodes,
            links: [],
            roam: true,
            draggable:true
        }
        ]
    }
    option2 && chart2.setOption(option2);
})
</script>
<style scoped>
.map-container1{
    width: 600px;
    height: 600px;
    background-color: yellow;
    border-radius: 50%;
    display: flex;
    justify-content: center;  /* 水平居中 */
    align-items: center; 
}
.map-container2{
    width: 200px;
    height: 200px;
    background-color: pink;
    border-radius: 50%;
    /* mix-blend-mode:screen; */
    /* padding:10px; */
    /* top:10px */
}
</style>