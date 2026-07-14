<template>
    <div class="test1">
        <div class="test2"></div>
    </div>
    <graph :data="graphData" :link="[]"></graph>
</template>
<script setup>
import data from '@/data/self.json'
import data1 from '@/data/graph.json'
import { onMounted,ref } from 'vue';
import { getWorld,getNodes } from '@/api/simple_api'
import graph from '../components/graph.vue';

const nodesData=ref(null)
const graphData=ref(null)
onMounted(async()=>{
    // console.log(data['pay']['$count']-data['income']['$count'])
    graphData.value=await getWorld()
    nodesData.value=await getNodes()
    data1['series'][0]['data']=graphData.value
    // data1['series'][1]['data']=nodesData.value
    // console.log(data1)
})
</script>

<style>
.test1{
    width: 200px;
    height: 200px;
    background-color: yellow;
    border-radius: 50%;
}
.test2{
    width: 200px;
    height: 50px;
    background-color: pink;
    border-radius: 50%;
    mix-blend-mode:screen;
    padding:10px;
    top:10px
}
</style>