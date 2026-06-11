<template>
    <div class="xxx">
        <graph :data="data" :link="link" :layout="layout"></graph>
    </div>
</template>

<script setup>
import { ref ,onMounted} from 'vue';
import graph from '../components/graph1.vue';
import {getLiveCycle,getLink} from '@/api/simple_api'

const data=ref([])
const link=ref([])
const layout=ref('circular')
// 定义图表配置
onMounted(async () => {
    data.value=await getLiveCycle()
    link.value=await getLink()
    // console.log(data.value[0]);
    // console.log(link.value[0]);
})
</script>
<style>
.xxx{
    background-color: aqua;
    width: 1000px;
    height: 800px;
}
</style>