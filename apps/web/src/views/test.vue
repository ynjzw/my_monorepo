<script setup>
import { onMounted, ref } from 'vue';
import { getFamily,getLinks } from '../api';
import * as echarts from 'echarts';
import level from '../components/level.vue';

onMounted(async ()=>{
    const node = await getFamily();
    const links = await getLinks();
    
})
</script>

<template>
    
    <level :data="node" :msg="jsjjdjs"></level>
    <level :data="node"></level>
</template>