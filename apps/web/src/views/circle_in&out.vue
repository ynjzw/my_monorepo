<template>
    <div>
        <button @click="test">test</button>
        <div ref="mapRef1" class="map-container1"></div>
    </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const mapRef1 = ref(null);
let chart1 = null;       // 存储图表实例
let chart2 = null;       // 存储图表实例
let intervalId = null;   // 存储定时器ID
let nodes = [];          // 存储节点数据，供定时器使用
let links = []; 
var option1 = null;     // 存储图表配置项，供定时器使用 
let i=1
let j=0 
for (let i = 1; i <= 50; i++) {
    nodes.push({
        id: i,
        name: `Node ${i}`,
        itemStyle: {
            color: i <= 25 ? 'blue' : 'red', // 前25个节点为蓝色，后25个节点为红色
        },
    });
}

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
}  
let seriesData = [
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
    },
    {
        type: 'tree',
        data: [
                {
                    name: '我',  
                    value:100,
                    symbolSize: 10,
                    children: [
                        { name: '爸爸', value: 10 , children: [
                        { name: '爷爷', value: 10 },
                        { name: '奶奶', value: 10 }
                        ]},
                        { name: '妈妈', value: 10, children: [
                        { name: '外公', value: 10 },
                        { name: '外婆', value: 10 }
                        ]}
                    ]
                }
        ], // 支持多棵树
        // 布局配置
        top: '8%',
        right: '5%',
        orient: 'BT',
        edgeShape: 'polyline',
        // 节点样式
        // symbol: 'circle',
        // symbolSize: 100,
        itemStyle: {
        // color: 'pink',
        borderColor: '#fff',
        borderWidth: 2
        },
        
        // 标签配置
        label: {
        position: 'bottom',
        verticalAlign: 'middle',
        align: 'right',
        },
        
        // 叶子节点标签
        leaves: {
        label: {
            position: 'bottom',
            verticalAlign: 'middle',
            align: 'left',
            // fontSize: 12,
            // color: 'blue' 
        }
        },
        
        // 连线样式
        lineStyle: {
        // color: 'red',
        width: 2,
        curveness: 0.5
        },
        
        // 交互
        emphasis: {
        focus: 'descendant',
        lineStyle: {
            width: 3,
            color: '#5470c6'
        }
        },
        
        // 展开/折叠
        expandAndCollapse: true,
        initialTreeDepth: 2,
        
    },
    {
        type: 'tree',
        data: [
                {
                    name: 'kkk',  
                    value:100,
                    symbolSize: 10,
                    children: [
                        { name: 'ooo', value: 10 , children: [
                        { name: 'lll', value: 10 },
                        { name: 'qqq', value: 10 }
                        ]}                            
                    ]
                }
        ], // 支持多棵树
        // 布局配置
        top: '8%',
        right: '75%',
        orient: 'BT',
        edgeShape: 'polyline',
        // 节点样式
        // symbol: 'circle',
        // symbolSize: 100,
        itemStyle: {
        // color: 'pink',
        borderColor: '#fff',
        borderWidth: 2
        },
        
        // 标签配置
        label: {
        position: 'bottom',
        verticalAlign: 'middle',
        align: 'right',
        // fontSize: 12,
        // color: 'yellow' ,
        // fontWeight: 500
        },
        
        // 叶子节点标签
        leaves: {
        label: {
            position: 'bottom',
            verticalAlign: 'middle',
            align: 'left',
            // fontSize: 12,
            // color: 'blue' 
        }
        },
        
        // 连线样式
        lineStyle: {
        // color: 'red',
        width: 2,
        curveness: 0.5
        },
        
        // 交互
        emphasis: {
        focus: 'descendant',
        lineStyle: {
            width: 3,
            color: '#5470c6'
        }
        },
        
        // 展开/折叠
        expandAndCollapse: true,
        initialTreeDepth: 2,
        
    }
];     // 存储图表数据，供定时器使用


const test=()=>{
    j++
    option1={
        title: { 
            text: 'ttt' 
        },
        series: seriesData.slice(0, j)
    }
    option1 && chart1.setOption(option1);
}
onMounted(async () => {
    // 初始化图表
    chart1 = echarts.init(mapRef1.value);
    
    option1={
        title: { 
            text: 'ttt' 
        },
        series: seriesData[j]
    }
    option1 && chart1.setOption(option1);

})
</script>
<style scoped>
.map-container1{
    width: 1000px;
    height: 600px;
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