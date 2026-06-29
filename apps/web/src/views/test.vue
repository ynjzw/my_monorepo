<template></template>
<script setup>
import data from '@/data/self.json'
import { onMounted } from 'vue';

onMounted(()=>{
    console.log(data['pay']['$count']-data['income']['$count'])
})
</script>