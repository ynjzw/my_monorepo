<template>
    <div  class="color-wheel">
        <div class="circle test1"  ></div>
        <div class="circle test2"  ></div>
        <div class="circle test3"  ></div>
    </div>
    
</template>
<script setup>
import data from '@/data/self.json'
import data1 from '@/data/graph.json'
import { onMounted,ref,nextTick } from 'vue';
import graph from '../components/graph.vue';
import * as echarts from 'echarts';
const layout = ref('force')
let myChart1 = null
let myChart2 = null
let nodesData=ref(null)
let graphData=ref(null)
let nodes = []
onMounted(async()=>{
    
})
</script>

<style>
.color-wheel {
    position: relative;
    width: 100%;
    height: 100%;
    /* 关键点：混合模式需要一个纯黑的底色作为“发光”的基础 */
    background-color: #000; 
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 基础圆形样式 */
.circle {
    position: absolute;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    /* 核心属性：滤色模式（加光混合） */
    mix-blend-mode: screen; 
}
.test1{
    background-color: red;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
}
.test2{
    bottom: 10%;
    left: 30%;
    background-color: green;
}
.test3{
    bottom: 10%;
    right: 30%;
    background-color: blue;
}
</style>