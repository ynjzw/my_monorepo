<template>
    <div>
        <button  @click="insert()"></button>
        <br>
        <div class="map" >      
            <div ref="mapRef" class="map-container" ></div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import {insert_nodes} from '@/api/simple_api'
import * as echarts from 'echarts';

// 预定义颜色池
const colorPalette = [
    '#5470c6', '#fac858', '#ee6666',  '#73cede', 
    '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc','#73c0de','#7ec0de'
];      

const mapRef = ref(null);
let chart = null;        // 存储图表实例
let intervalId = null;   // 存储定时器ID
let nodes = [];          // 存储节点数据，供定时器使用
let links = [];          // 存储连线数据
const diff=['xxx','yyy','zzz','xyz','zyx']
let min_x=0,max_x=0,min_y=0,max_y=0;

for (let i = 1; i <= 5; i++) {
    for (let j = 0; j <= Math.pow((6-i)*(11-i), 2); j++) {
        min_x = 500-Math.random()*(6-i)*100;
        max_x = 500+Math.random()*(6-i)*100;
        min_y = (6-i)*200-100;
        max_y = (6-i)*200+100;
        nodes.push({
            id: `${i*10000+j}`,
            name: diff[i-1],
            x:Math.floor(Math.random() * (Math.floor(max_x) - Math.ceil(min_x) + 1) + Math.ceil(min_x)),
            y:Math.floor(Math.random() * (Math.floor(max_y) - Math.ceil(min_y) + 1) + Math.ceil(min_y)),
            symbolSize: Math.pow(i,2)+Math.random()*Math.pow(2,i-1),
            symbol:'circle',
            itemStyle: {
                color: colorPalette[j%7]
            }
        });
    }
}
for (let i = 1; i <= 4; i++) {
    nodes.push({
        x:500,
        y:i*200+100,
        symbolSize: [1000,2],
        symbol:'rect',
        itemStyle: {
            color: colorPalette[9-i]
        }
    });
}

const insert = async () => {
    const payload = {
        nodes: nodes.map(node => ({
            node_id: node.id,
            name: node.name,
            x: node.x,
            y: node.y,
            symbol_size: node.symbolSize,
            symbol: node.symbol
        }))
    };
    await insert_nodes(payload)
        .then(response => {
            console.log('Nodes inserted successfully:', response.data);
        })
        .catch(error => {
            console.error('Error inserting nodes:', error);
        });
};

onMounted(() => {
    // 初始化图表
    chart = echarts.init(mapRef.value);
    
    // 设置图表配置
    chart.setOption({
        title: { 
            text: 'ttt' ,
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
                label: { show: false, position: 'bottom', fontSize: 12 },
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