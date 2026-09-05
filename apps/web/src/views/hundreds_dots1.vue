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
    const size=[50,10]
    // 生成100个节点
    nodes = [];
    // for (let i = 1; i <= Math.pow(10,2); i++) {
    //     nodes.push({
    //         id: `${i}`,
    //         name: `${i}`,
    //         value: 'xxx',
    //         symbolSize: 10,
    //         symbol:'circle'
    //     });
    // }
    for (let j = 1; j <= 2; j++) {
        for (let i = 1; i <= Math.pow(10,j); i++) {
            nodes.push({
                id: `${j*100+i}`,
                name: diff[j-1],
                x:i%10*100 +Math.random()*100,
                y:j*100 + Math.random()*i%10*10,
                value: diff[j-1] + ':' + (Math.random() + j*10).toFixed(2),
                // symbolSize: 50- j*10,
                symbolSize:size[j-1],
                symbol:'circle',
                itemStyle: {
                    color: colorPalette[i%10]
                }
            });
        }
    }
    
    nodes.push({
        id: '1001',
        name: '国家',
        x:500,
        y:-200,
        value: '国家',
        symbolSize: 101,
        symbol:'circle',
        itemStyle: {
            color: 'purple',
        }
    });
    links = [];
    // for (let i = 0; i < 100 ; i++) {
    //     links.push({ 
    //         source: nodes[i%10].id, 
    //         target: nodes[i].id ,
    //         // symbol:['arrow','none'],
    //         label: {
    //             show: false,
    //             fontSize:20
    //         },
    //         lineStyle: {
    //             width: 2,
    //             type:'dashed'
    //         }
    //     });
    // }
    for (let i = 0; i < Math.pow(10,2); i++) {
    // 每个节点只连接后面1-3个节点
        links.push({ 
            source: `${200+i}`, 
            target: `${100+i%10}`,
            symbol:['none','arrow'],
            label: {
                show: false,
                fontSize:20
            },
            lineStyle: {
                width: 1,
                color: colorPalette[i%10]
            }
        });
    }
    for (let i = 1; i <= 10; i++) {
    // 每个节点只连接后面1-3个节点
        links.push({ 
            source: `${200+i*10}`, 
            target: `${110}`,
            symbol:['none','arrow'],
            label: {
                show: false,
                fontSize:20
            },
            lineStyle: {
                width: 2,
                color: colorPalette[0]
            }
        });
    }
        
    for (let i = 0; i < 10 ; i++) {
        // 每个节点只连接后面1-3个节点
        links.push({ 
            source: nodes[i].id, 
            target: nodes[nodes.length - 1].id ,
            symbol:['none','arrow'],
            symbolSize:20,
            label: {
                show: false,
                fontSize:20,
                color:nodes[i].itemStyle.color
            },
            lineStyle: {
                color: nodes[i].itemStyle.color,
                width: 5
            }
        });
    }
    
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