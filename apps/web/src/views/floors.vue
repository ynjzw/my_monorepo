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
import { get_base_nodes } from '@/api/simple_api'
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

const insert = async () => {
    nodes = await get_base_nodes('floor');
    console.log('Nodes:', nodes[0]);
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