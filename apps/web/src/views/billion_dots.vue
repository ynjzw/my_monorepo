<template>
  <div class="map" >      
     <div ref="mapRef" class="map-container" ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

// 预定义颜色池
const colorPalette = [
    '#5470c6', '#fac858', '#ee6666', '#73c0de', '#73cede', 
    '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc','#7ec0de'
];      

const mapRef = ref(null);
let chart = null;        // 存储图表实例
let intervalId = null;   // 存储定时器ID
let nodes = [];          // 存储节点数据，供定时器使用
let links = [];          // 存储连线数据

for (let i = 0; i < 845; i++) {
    nodes.push({
        id: `${i}`,
        name: `Node ${i}`,
        symbolSize: 10 * Math.random(), // 随机大小
        symbol:'circle',
        itemStyle: {
            color: colorPalette[Math.floor(Math.random() * colorPalette.length)]
        }
    });
}

onMounted(() => {
    // 初始化图表
    chart = echarts.init(mapRef.value);
    
    links = [];
    
    // 设置图表配置
    chart.setOption({
        series: [
            {
            type: 'graph',
            layout: 'force',
            data: nodes,
            links: links,
            roam: true,
            draggable:true,
            force: {
                // initLayout: 'circular'
                // gravity: 0
                repulsion: 100,
                // edgeLength: 5
            },
        }
        ]
    });
    
});

// 组件销毁时清理定时器和图表
onUnmounted(() => {
    if (intervalId) {
        clearInterval(intervalId);
    }
    if (chart) {
        chart.dispose();
        chart = null;
    }
});
</script>

<style scoped> 
.map{
    width: 1000px;
    height: 600px;
}
.map-container{
    width: 1000px;
    height: 600px;
}
</style>