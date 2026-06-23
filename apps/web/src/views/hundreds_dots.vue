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
    '#5470c6', '#fac858', '#ee6666', '#73c0de', 
    '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
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
    
    // 生成100个节点
    nodes = [];
    for (let i = 1; i <= 100; i++) {
        nodes.push({
            id: `${i}`,
            name: `${i}`,
            value: Math.random() * 100,
            symbolSize: 30,
            symbol:'rect',
            category: Math.floor(Math.random() * 3),
            itemStyle: {
                color: colorPalette[Math.floor(Math.random() * colorPalette.length)],
                borderRadius:'10%'
            }
        });
    }
    
    // 生成连线（稀疏连线，避免过多导致性能问题）
    // 只连接部分相邻节点，而不是全部互相连接（100个节点全连接会有4950条线）
    links = [];
    // for (let i = 0; i < nodes.length - 1; i++) {
    //     // 每个节点只连接后面1-3个节点
    //     const connectCount = Math.floor(Math.random() * 3) + 1;
    //     for (let j = 1; j <= connectCount && i + j < nodes.length; j++) {
    //         links.push({ 
    //             source: nodes[i].id, 
    //             target: nodes[i + j].id 
    //         });
    //     }
    // }
    
    // 设置图表配置
    chart.setOption({
        title: { text: '动态节点颜色示例' },
        tooltip: { trigger: 'item' },
        series: [{
            type: 'graph',
            layout: 'force',
            data: nodes,
            links: links,
            roam: true,
            label: { show: true, position: 'right', fontSize: 10 },
            force: { 
                repulsion: 100, 
                edgeLength: 150,
                gravity: 0.3,
                friction: 0.1
            }
        }]
    });
    
    // 每秒钟随机改变节点颜色
    intervalId = setInterval(() => {
        updateChartData();
    }, 1000);
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