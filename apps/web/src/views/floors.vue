<template>
    <div>
        <button  @click="insert()">xxx</button>
        <br>
        <div class="map" >      
            <div ref="mapRef" class="map-container" ></div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import {insert_nodes, insert_links} from '@/api/simple_api'
import * as echarts from 'echarts';

// 预定义颜色池
const colorPalette = [
    '#5470c6', '#fac858', '#ee6666','#73cede', '#3ba272', 
    '#fc8452', '#9a60b4', '#ea7ccc','#73c0de','#7ec0de'
];      

const mapRef = ref(null);
let chart = null;        // 存储图表实例
let intervalId = null;   // 存储定时器ID
let nodes = [];          // 存储节点数据，供定时器使用
let links = [];          // 存储连线数据
const size = [50, 10];
const imageList=['image:///src/images/商.png?t=*','image:///src/images/工.png?t=*']
const nameList=['商', '工']
// 生成节点
for (let j = 1; j <= 2; j++) {
    for (let i = 1; i <= Math.pow(10, j); i++) {
        // ★ 核心改动：节点大小 = 基础大小 + change（随时间递增）
        const baseSize = size[j - 1] || 10;
        nodes.push({
            id: `${j * 100 + i}`,
            name: nameList[j - 1],
            x: (i % 10) * 100 + Math.random() * 100,
            y: j * 100 + Math.random() * (i % 10) * 10,
            symbolSize: baseSize , // ✅ 关键改动
            symbol: imageList[j - 1] ,
        });
    }
}

// 中心节点
nodes.push({
    id: '1001',
    name: '士',
    x: 500,
    y: -200,
    value: '士',
    symbolSize: 101 , // ✅ 也同步变大
    symbol: 'image:///src/images/士.png?t=*',
});

for (let i = 0; i < Math.pow(10, 2); i++) {
    links.push({
        source: `${200 + i}`,
        target: `${100 + (i % 10)}`,
        symbol: ['none', 'arrow'],
        symbolSize: 10
    });
    links.push({
        source: '1001',
        target: `${200 + i}`,
        symbol: ['none', 'arrow'],
        symbolSize: 10
    });
}
for (let i = 1; i <= 10; i++) {
    links.push({
        source: `${200 + i * 10}`,
        target: '110',
        symbol: ['none', 'arrow'],
        symbolSize: 10
    });
}
for (let i = 0; i < 10; i++) {
    links.push({
        source: nodes[i].id,
        target: '1001',
        symbol: ['none', 'arrow'],
        symbolSize: 10
    });
    links.push({
        source: '1001',
        target: nodes[i].id,
        symbol: ['none', 'arrow'],
        symbolSize: 10,
    });
}

const insert = async () => {
    const payload = {
        nodes: nodes.map(node => ({
            id: node.id,
            name: node.name,
            x: node.x,
            y: node.y,
            symbol: node.symbol,
            symbolSize: node.symbolSize
        }))
    };
    
    // await insert_nodes(payload)
    //     .then(response => {
    //         console.log('Nodes inserted successfully:', response.data);
    //     })
    //     .catch(error => {
    //         console.error('Error inserting nodes:', error);
    //     });

    const linkPayload = {
        links: links.map(link => ({
            id: `${link.source}-${link.target}`, // 生成唯一ID
            source: link.source,
            target: link.target,
            type: 'floor'
        }))
    };
    await insert_links(linkPayload)
        .then(response => { 
            console.log('Links inserted successfully:', response.data);
        })
        .catch(error => {
            console.error('Error inserting links:', error);
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