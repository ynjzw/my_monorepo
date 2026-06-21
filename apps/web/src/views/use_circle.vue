<template>
  
    <input v-model="ss"/>
    <button @click="test()">ss</button>
    
    <circle :data="circleData"></circle>
</template>
<script setup>
import circle from '@/components/circle.vue';
import { onMounted,ref } from 'vue';
import axios from 'axios';
const ss=ref('')
const circleData=ref(null)

const test = async () => {
  const path='http://localhost:5173' + ss.value + '?t=1782032371436'
  
  const response = await axios.get(path)
  circleData.value = response.data;
  console.log(circleData.value)
}
</script>