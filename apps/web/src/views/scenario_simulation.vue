<template>
  <div>
    <h1>推演工作台</h1>
    <p>这里是推演工作台的内容。</p>
    <button @click="add_series">添加系列</button>
    <button @click="add_option">添加选项</button>
    <timeline
          ref="timeLineRef"
          :title_list="title1"
          :option_list="option"
          @click="handleNodeClick"
          @ready="onChartReady"
    />
  </div>
</template>
<script setup>
import { ref,onMounted } from 'vue';
import timeline from '@/components/timeline.vue'
const series = ref([]);
const options = ref([]);
const timeLineRef = ref(null)
const add_series = () => {
  // Implementation for adding series
  series.value.push({ name: '新系列', options: [] });
}

const add_option = () => {
  // Implementation for adding option
  options.value.push({ name: '新选项' });
}
onMounted(() => {
  // You can access the timeline component here if needed
  console.log('');
});
</script>