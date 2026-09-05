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

const eraseLink = () => {
    if (!chart) return;
    chart.setOption({
        series: [{
            links: [] // 清空连线数据
        }]
    });
};

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
    chart = echarts.init(mapRef.value);
    let idx = 1;
    
    // 初始化中心节点
    const data = [{
        id: '0',
        x: chart.getWidth() / 2,
        y: chart.getHeight() / 2,
        symbolSize: 20,
        itemStyle: { color: colorPalette[0] }
    }];
    
    // 初始 option
    const option = {
        series: [{
            type: 'graph',
            layout: 'none',
            data: data,
            links: []  // 初始无连线
        }]
    };
    chart.setOption(option);
    
    // 启动定时器
    intervalId = setInterval(() => {
        const currentData = chart.getOption().series[0].data;
        
        // 1. 添加新节点（每轮增加10个）
        for (let j = 1; j <= idx*10; j++) {
            currentData.push({
                id: `node_${Date.now()}_${j}`,
                x: (Math.random() * 2 - 1)*100 + chart.getWidth()/2,
                y: chart.getHeight() / 2 + 30 + Math.random() * 10,
                symbolSize: 3,
                
            });
        }
        
        
        if(idx % 3 === 0) {
            // 2. 更新所有节点的位置（下沉效果）
            currentData.forEach((node, index) => {
                if(index < idx / 3 * 10){
                    node.y = node.y - 50;
                    node.symbolSize = node.symbolSize + 3;
                    if (node.y < chart.getHeight() / 4 && node.itemStyle == null) {
                        node.itemStyle = {
                            color: colorPalette[Math.floor(Math.random() * colorPalette.length)]    
                        }
                    }
                } 
                
            });
        }
        // 3. 只更新 data，不重置整个 option
        chart.setOption({
            series: [{ data: currentData }]
        });
        idx++;
    }, 3000);
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