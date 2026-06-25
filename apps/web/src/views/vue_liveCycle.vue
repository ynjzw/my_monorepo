<template>
    <div class="xxx">
        <xxx :data="data" :link="link" :layout="layout" :title="test"></xxx>
    </div>
</template>

<script setup>
import { ref ,onMounted} from 'vue';
import xxx from '../components/graph.vue';
import {getLiveCycle,getLink} from '@/api/simple_api'

const data=ref([])
const link=ref([])
const layout=ref('circular')
// 定义图表配置

onMounted(async () => {
    data.value=await getLiveCycle()
    link.value=await getLink()
    // alert('xxx')
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