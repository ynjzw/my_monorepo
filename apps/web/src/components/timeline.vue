<template>
    <div class="chart-wrapper">
        <div 
          ref="chartContainer" 
          class="chart-container"
        ></div>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-if="error" class="error">{{ error }}</div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  title_list: { type: Array },
  option_list: { type: Array }
})

const emit = defineEmits(['ready', 'data-loaded', 'error', 'click'])

const chartContainer = ref(null)
const myChart = ref(null)
const error = ref(null)
const loading = ref(false)

const buildOption = () => {
  if (!props.title_list?.length || !props.option_list?.length) {
    error.value = '暂无数据'
    return null
  }
  error.value = null
  return {
    baseOption: {
      timeline: {
        show: true,
        axisType: 'category',
        autoPlay: false,
        playInterval: 1500,
        data: props.title_list
      },
      title: { text: 'vue 生命周期举例演示' }
    },
    options: props.option_list
  }
}

const initChart = () => {
  if (!chartContainer.value) return
  if (myChart.value) myChart.value.dispose()
  myChart.value = echarts.init(chartContainer.value)

  // 绑定 click
  myChart.value.on('click', (params) => emit('click', params))

  const option = buildOption()
  if (option) {
    myChart.value.setOption(option)
    emit('ready', myChart.value)
    emit('data-loaded')
  }
}

watch(
  () => [props.title_list, props.option_list],
  () => {
    if (!myChart.value) return
    const option = buildOption()
    if (option) {
      myChart.value.setOption(option, true)
      emit('data-loaded')
    }
  },
  { deep: true }
)

const handleResize = () => myChart.value?.resize()

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  myChart.value?.dispose()
  myChart.value = null
})
</script>
<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}
.chart-container {
  width: 100%;
  height: 100%;
}
.loading, .error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.error {
  color: red;
}
</style>