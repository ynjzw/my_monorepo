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
            x:Math.random() * 100,
            y:Math.random() * 2,
            value: Math.random() * 100,
            symbolSize: 20,
            symbol:'circle',
            category: Math.floor(Math.random() * 3),
            itemStyle: {
                // color: colorPalette[Math.floor(Math.random() * colorPalette.length)]
            }
        });
    }
    nodes.push({
        id: '101',
        name: '101',
        x:50,
        y:-20,
        value: 101,
        symbolSize: 101,
        symbol:'circle',
        itemStyle: {
            color: 'purple',
        }
    });
    // 生成连线（稀疏连线，避免过多导致性能问题）
    // 只连接部分相邻节点，而不是全部互相连接（100个节点全连接会有4950条线）
    links = [];
    for (let i = 0; i < nodes.length; i++) {
        // 每个节点只连接后面1-3个节点
        links.push({ 
            source: nodes[i].id, 
            target: nodes[nodes.length - 1].id ,
            // symbol:['none','arrow'],
            lineStyle: {
                color: '#5470c6'
            },
            effect:{
                show: true,
                type: 'line',
                symbol: 'arrow',
                symbolSize: 8,
                color: '#ff6b6b',
                period: 2000,
                trailLength: 0.1
            }
        });
    }
    
    // 设置图表配置
    chart.setOption({
        title: { text: '动态节点颜色示例' },
        tooltip: { trigger: 'item' },
        series: [{
            type: 'graph',
            layout: 'none',
            data: nodes,
            links: links,
            roam: true,
            draggable:true,
            label: { show: false, position: 'right', fontSize: 10 },
            force: { 
                repulsion: 100, 
                edgeLength: 150,
                gravity: 0.3,
                friction: 0.1
            }
        },
//           {
//         type: 'lines',
//         coordinateSystem: 'cartesian2d',
//         zlevel: 1,
        
//         data: [
//     {
//       coords: [[100, 200], [300, 100]],
//       value: 10,
//       source: 'A',
//       target: 'B'
//     },
//     {
//       coords: [[300, 100], [500, 200]],
//       value: 20,
//       source: 'B',
//       target: 'C'
//     },
//     {
//       coords: [[500, 200], [400, 400]],
//       value: 15,
//       source: 'C',
//       target: 'D'
//     },
//     {
//       coords: [[400, 400], [200, 400]],
//       value: 25,
//       source: 'D',
//       target: 'E'
//     },
//     {
//       coords: [[200, 400], [100, 200]],
//       value: 30,
//       source: 'E',
//       target: 'A'
//     },
//     {
//       coords: [[300, 100], [400, 400]],
//       value: 18,
//       source: 'B',
//       target: 'D'
//     },
//     {
//       coords: [[500, 200], [200, 400]],
//       value: 12,
//       source: 'C',
//       target: 'E'
//     }
//   ],
        
//         // 线条样式
//         lineStyle: {
//           color: '#ff6b6b',
//           width: 3,
//           opacity: 0.8,
//           curveness: 0.2
//         },
        
//         // 流动特效
//         effect: {
//           show: true,
//           // 流动符号
//           symbol: 'circle',
//           symbolSize: 8,
//           // 流动颜色
//           color: '#ff6b6b',
//           // 轨迹长度
//           trailLength: 0.3,
//           // 循环周期
//           period: 2000,
//           // 是否循环
//           loop: true,
//           // 移动端适配
//           mobile: true
//         },
        
//         // 动画
//         animation: true,
//         animationDuration: 1000,
//         animationEasing: 'cubicOut'
//       }
        ]
    });
    
    // 每秒钟随机改变节点颜色
    // intervalId = setInterval(() => {
    //     updateChartData();
    // }, 1000);
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