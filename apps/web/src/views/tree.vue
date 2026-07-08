<template>
  <div ref="chartContainer" style="width: 100%; height: 600px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import * as d3 from 'd3-hierarchy'

const chartContainer = ref(null)

onMounted(() => {
  const chart = echarts.init(chartContainer.value)
  
  // 树形数据
  const treeData = {
    name: '我',
    children: [
      { name: '爸爸', value: 10 , children: [
        { name: '爷爷', value: 10 },
        { name: '奶奶', value: 10 }
      ]},
      { name: '妈妈', value: 10, children: [
        { name: '外公', value: 10 },
        { name: '外婆', value: 10 }
      ]}
    ]
  }
  const option = {
    tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
      },
    title: {
      text: 'ttt'
    },
    series: [
      {
        type: 'tree',
        data: treeData,
        top: '1%',
        left: '7%',
        bottom: '1%',
        right: '20%',
        symbolSize: 7,
        label: {
            position: 'left',
            verticalAlign: 'middle',
            align: 'right',
            fontSize: 9
          },
          leaves: {
            label: {
              position: 'right',
              verticalAlign: 'middle',
              align: 'left'
            }
          },
          emphasis: {
            focus: 'descendant'
          },
          expandAndCollapse: true,
          animationDuration: 550,
          animationDurationUpdate: 750
      }
    ]
  }
  
  option && chart.setOption(option)
})
</script>