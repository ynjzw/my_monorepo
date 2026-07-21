<template>
    <button @click="eraseLink">eraseLink</button>
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
    // 初始化图表
    chart = echarts.init(mapRef.value);
    const diff=['xxx','yyy','zzz','xzy']
    // 生成100个节点
    nodes = [];
    nodes = [
        {
            id: '1001',
            name: '电子',
            x:400,
            y:400,
            value: '电子',
            symbolSize: 10,
            symbol:'circle'
        },
        {
            id: '1002',
            name: '原子核',
            x:600,
            y:400,
            value: '原子核',
            symbolSize: 10,
            symbol:'circle'
        },
        {
            id: '1101',
            name: '原子',
            x:500,
            y:350,
            value: '原子',
            symbolSize: 10,
            symbol:'circle'
        },
        {
            id: '1102',
            name: '离子',
            x:400,
            y:350,
            value: '离子',
            symbolSize: 10,
            symbol:'circle'
        },
        {
            id: '1150',
            name: '元素',
            x:500,
            y:300,
            value: '元素',
            symbolSize: 50,
            symbol:'image:///src/images/element.jpeg?t=*'
        },
        {
            id: '1201',
            name: '分子',
            x:500,
            y:200,
            value: '分子',
            symbolSize: 50,
            symbol:'image:///src/images/molecule.png?t=*'
        },
        {
            id: '1301',
            name: '细胞',
            x:500,
            y:150,
            value: '细胞',
            symbolSize: 50,
            symbol:'image:///src/images/cell.png?t=*'
        },
        {
            id: '1351',
            name: '组织',
            x:400,
            y:100,
            value: '组织',
            symbolSize: 50,
            symbol:'image:///src/images/tissue.png?t=*'
        },
        {
            id: '1352',
            name: '器官',
            x:600,
            y:100,
            value: '器官',
            symbolSize: 50,
            symbol:'image:///src/images/organ.png?t=*'
        },
        {
            id: '1373',
            name: '系统',
            x:500,
            y:80,
            value: '系统',
            symbolSize: 10,
            symbol:'circle'
        },
        {
            id: '1401',
            name: '生命',
            x:500,
            y:50,
            value: '生命',
            symbolSize: 10,
            symbol:'circle'
        },
        {
            id: '1501',
            name: '社会',
            x:500,
            y:10,
            value: '社会',
            symbolSize: 10,
            symbol:'circle'
        }
    ]
    links = [];
    links = [
        { 
            source: '1001', 
            target: '1101',
            label:{
                show:true,
                formatter:'构成'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1002', 
            target: '1101',
            label:{
                show:true,
                formatter:'构成'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1101', 
            target: '1102',
            label:{
                show:true,
                formatter:'得失电子'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1101', 
            target: '1150',
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1150', 
            target: '1201',
            label:{
                show:true,
                formatter:'组合'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1201', 
            target: '1301',
            label:{
                show:true,
                formatter:'组装'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1301', 
            target: '1351',
            label:{
                show:true,
                formatter:'增殖分化'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1301', 
            target: '1352',
            label:{
                show:true,
                formatter:'增殖分化'
            },
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1351', 
            target: '1373',
            label:{
                show:true,
                formatter:'协作'
            },
            lineStyle: {
                width: 2,
                type:'dotted'
            }
        },
        { 
            source: '1352', 
            target: '1373',
            label:{
                show:true,
                formatter:'协作'
            },
            lineStyle: {
                width: 2,
                type:'dotted'
            }
        },
        { 
            source: '1373', 
            target: '1401',
            lineStyle: {
                width: 2
            }
        },
        { 
            source: '1401', 
            target: '1501',
            lineStyle: {
                width: 2
            }
        }
    ]
    // 设置图表配置
    chart.setOption({
        title: { 
            text: 'molecule2social' ,
            textStyle: {
                color: 'pink'
            }
        },
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