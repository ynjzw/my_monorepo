<script setup>
import { onMounted, ref } from 'vue';
import { getFamily,getLinks } from '../api';
import * as echarts from 'echarts';
import level from '../components/level.vue';
const node = ref([])
const msg = ref('jsjjdjs');
onMounted(async()=>{
    node.value = await getFamily();
})
</script>

<template>
    
    <level :data="node" :msg="msg"></level>
    <!-- <level :data="node"></level> -->
</template>