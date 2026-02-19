<script setup>
import { onMounted, ref } from 'vue';
import { getFamily,getLinks,getWorld } from '@/api';
import * as echarts from 'echarts';
import level from '@/components/level.vue';
const node = ref([])
const world = ref([])
onMounted(async()=>{
    node.value = await getFamily();
    world.value = await getWorld();
})
</script>

<template>
    
    <level :data="node" ></level>
    <level :data="world"></level>
</template>