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
    name: 'Root',
    children: [
      { name: 'A', value: 30 },
      { name: 'B', value: 40, children: [
        { name: 'B1', value: 20 },
        { name: 'B2', value: 15 }
      ]},
      { name: 'C', value: 30 }
    ]
  }
  
  // 使用 D3 计算布局
  const width = 800
  const height = 600
  
  const root = d3.hierarchy(treeData)
    .sum(d => d.value || 0)
  
  const pack = d3.pack()
    .size([width - 40, height - 40])
    .padding(5)
  
  pack(root)
  
  // 准备数据
  const circles = []
  const links = []
  
  root.each(node => {
    circles.push({
      name: node.data.name,
      value: node.value,
      x: node.x + 20,
      y: node.y + 20,
      r: node.r,
      depth: node.depth,
      children: node.children ? node.children.map(c => c.data.name) : []
    })
    
    if (node.parent) {
      links.push({
        source: node.parent.data.name,
        target: node.data.name
      })
    }
  })
  
  const option = {
    title: {
      text: '自定义 Circle Packing + Graph'
    },
    series: [
      {
        type: 'custom',
        renderItem: (params, api) => {
          // 自定义渲染逻辑
          const idx = params.dataIndex
          const circle = circles[idx]
          
          if (!circle) return null
          
          return {
            type: 'circle',
            shape: {
              cx: circle.x,
              cy: circle.y,
              r: circle.r
            },
            style: {
              fill: circle.depth === 0 ? '#ff6b6b' : 
                     circle.depth === 1 ? '#4ecdc4' : '#95a5a6',
              stroke: '#fff',
              lineWidth: 2
            },
            styleEmphasis: {
              fill: circle.depth === 0 ? '#ff5252' : 
                     circle.depth === 1 ? '#45b7d1' : '#7f8c8d'
            },
            textContent: {
              type: 'text',
              style: {
                text: circle.name,
                fontFamily: 'Arial',
                fontSize: Math.min(16, circle.r / 3),
                fill: '#fff',
                fontWeight: 'bold'
              }
            },
            textConfig: {
              position: 'inside'
            }
          }
        },
        data: circles,
        encode: {
          x: 'x',
          y: 'y'
        }
      },
      {
        type: 'graph',
        layout: 'none',
        data: circles.map(c => ({
          name: c.name,
          x: c.x,
          y: c.y,
          symbolSize: c.r,
          itemStyle: { opacity: 0 },
          label: { show: false }
        })),
        links: links,
        lineStyle: {
          color: '#999',
          width: 2,
          curveness: 0,
          opacity: 0.5
        },
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 8],
        z: 2
      }
    ],
    tooltip: {
      formatter: (params) => {
        if (params.seriesType === 'custom') {
          const data = params.data
          return `${data.name}<br/>值: ${data.value}<br/>子节点: ${data.children?.length || 0}`
        }
        return ''
      }
    }
  }
  
  chart.setOption(option)
})
</script>