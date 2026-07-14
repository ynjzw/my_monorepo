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

// 数据更新函数 - 更新节点颜色
const updateChartData = () => {
    if (!chart) return;
    
    // 随机分配颜色池中的颜色
    const updatedNodes = nodes.map((node) => ({
        ...node,
        itemStyle: {
            color: colorPalette[Math.floor(Math.random() * colorPalette.length)]
        }
    }));
    
    chart.setOption({
        series: [{
            data: updatedNodes,
            animation: true,
            animationDuration: 500
        }]
    });
};

onMounted(() => {
    // 初始化图表
    chart = echarts.init(mapRef.value);
    const diff=['xxx','yyy','zzz','xzy']
    // 生成100个节点
    nodes = [];
    
    nodes.push({
        id: `1000`,
        name: 'self',
        x:500,
        y:-500,
        value: 10000,
        symbolSize: 10000,
        symbol:'circle',
        itemStyle: {
            color: colorPalette[0]
        }
    });
    
    nodes.push({
        id: '1001',
        name: 'mask_now',
        x:500,
        y:3000,
        value: 0.001,
        symbolSize: 0.001,
        symbol:'circle',
        itemStyle: {
            color: 'purple',
        }
    });
    nodes.push({
        id: '1002',
        name: 'mask_original',
        x:500,
        y:1000,
        value: 0.22,
        symbolSize: 0.22,
        symbol:'circle',
        itemStyle: {
            color: colorPalette[1],
        }
    });

    links = [];
    
    // 设置图表配置
    chart.setOption({
        title: { text: 'rrr',color:'red' },
        // tooltip: { trigger: 'item' },
        series: [
            {
            type: 'graph',
            layout: 'none',
            data: nodes,
            links: links,
            roam: true,
            draggable:true,
            label: { show: true, position: 'bottom', fontSize: 12 },
            force: { 
                repulsion: 100, 
                edgeLength: 150,
                gravity: 0.3,
                friction: 0.1
            }
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