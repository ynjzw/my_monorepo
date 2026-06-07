<template>
    <div>
        <graph :data="data" :link="link" :layout="layout"></graph>
    </div>
</template>

<script setup>
import { ref ,onMounted} from 'vue';
import graph from '../components/graph.vue';
import {getLiveCycle,getLink} from '@/api/simple_api'

const data=ref([])
const link=ref([])
const layout=ref('circular')
// 定义图表配置
onMounted(async () => {
    data.value=await getLiveCycle()
    // link.value=await getLink()
    // console.log(data.value);
})
</script>