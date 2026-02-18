<script setup>
import { onMounted, ref } from 'vue';
import { hierarchy, tree } from 'd3-hierarchy';
import * as echarts from 'echarts';

var dom = document.getElementById('main');

var myChart = echarts.init(dom);
var app = {};
var option;

onMounted(()=>{
    // 开始检查
    checkAndInit();
})
// 创建模拟数据，因为原示例数据可能无法访问
const data = {
    "$count": 100,
    "Chart": {
        "$count": 30,
        "Basic": {
        "$count": 10,
        "Bar": { "$count": 5 },
        "Line": { "$count": 5 }
        },
        "Advanced": {
        "$count": 20,
        "Pie": { "$count": 10 },
        "Scatter": { "$count": 10 }
        }
    },
    "Component": {
        "$count": 40,
        "Grid": { "$count": 15 },
        "Legend": { "$count": 15 },
        "Tooltip": { "$count": 10 }
    },
    "Option": {
        "$count": 30,
        "Title": { "$count": 10 },
        "Toolbox": { "$count": 10 },
        "VisualMap": { "$count": 10 }
    }
    };


function prepareData(rawData) {
    const seriesData = [];
    let maxDepth = 0;
    
    function convert(source, basePath, depth) {
    if (source == null) {
        return;
    }
    if (maxDepth > 5) {
        return;
    }
    maxDepth = Math.max(depth, maxDepth);
    seriesData.push({
        id: basePath,
        value: source.$count,
        depth: depth,
        index: seriesData.length
    });
    
    for (var key in source) {
        if (source.hasOwnProperty(key) && !key.match(/^\$/)) {
        var path = basePath + '.' + key;
        convert(source[key], path, depth + 1);
        }
    }
    }
    
    convert(rawData, 'option', 0);
    return {
    seriesData: seriesData,
    maxDepth: maxDepth
    };
}

function initChart(seriesData, maxDepth) {
    var displayRoot = stratify();
    
    function stratify() {
    return d3
        .stratify()
        .parentId(function (d) {
        return d.id.substring(0, d.id.lastIndexOf('.'));
        })(seriesData)
        .sum(function (d) {
        return d.value || 0;
        })
        .sort(function (a, b) {
        return b.value - a.value;
        });
    }
    
    function overallLayout(params, api) {
    var context = params.context;
    d3
        .pack()
        .size([api.getWidth() - 2, api.getHeight() - 2])
        .padding(3)(displayRoot);
    context.nodes = {};
    displayRoot.descendants().forEach(function (node, index) {
        context.nodes[node.id] = node;
    });
    }
    
    function renderItem(params, api) {
    var context = params.context;
    // Only do that layout once in each time `setOption` called.
    if (!context.layout) {
        context.layout = true;
        overallLayout(params, api);
    }
    var nodePath = api.value('id');
    var node = context.nodes[nodePath];
    if (!node) {
        // Render nothing.
        return;
    }
    var isLeaf = !node.children || !node.children.length;
    var focus = new Uint32Array(
        node.descendants().map(function (node) {
        return node.data.index;
        })
    );
    var nodeName = isLeaf
        ? nodePath
            .slice(nodePath.lastIndexOf('.') + 1)
            .split(/(?=[A-Z][^A-Z])/g)
            .join('\n')
        : '';
    var z2 = api.value('depth') * 2;
    return {
        type: 'circle',
        focus: focus,
        shape: {
        cx: node.x,
        cy: node.y,
        r: node.r
        },
        transition: ['shape'],
        z2: z2,
        textContent: {
        type: 'text',
        style: {
            text: nodeName,
            fontFamily: 'Arial',
            width: node.r * 1.3,
            overflow: 'truncate',
            fontSize: node.r / 3
        },
        emphasis: {
            style: {
            overflow: null,
            fontSize: Math.max(node.r / 3, 12)
            }
        }
        },
        textConfig: {
        position: 'inside'
        },
        style: {
        fill: api.visual('color')
        },
        emphasis: {
        style: {
            fontFamily: 'Arial',
            fontSize: 12,
            shadowBlur: 20,
            shadowOffsetX: 3,
            shadowOffsetY: 5,
            shadowColor: 'rgba(0,0,0,0.3)'
        }
        }
    };
    }
    
    option = {
    dataset: {
        source: seriesData
    },
    tooltip: {},
    visualMap: [
        {
        show: false,
        min: 0,
        max: maxDepth,
        dimension: 'depth',
        inRange: {
            color: ['#006edd', '#e0ffff']
        }
        }
    ],
    hoverLayerThreshold: Infinity,
    series: {
        type: 'custom',
        renderItem: renderItem,
        progressive: 0,
        coordinateSystem: 'none',
        encode: {
        tooltip: 'value',
        itemName: 'id'
        }
    }
    };
    
    myChart.setOption(option);
    
    myChart.on('click', { seriesIndex: 0 }, function (params) {
    drillDown(params.data.id);
    });
    
    function drillDown(targetNodeId) {
    displayRoot = stratify();
    if (targetNodeId != null) {
        displayRoot = displayRoot.descendants().find(function (node) {
        return node.data.id === targetNodeId;
        });
    }
    // A trick to prevent d3-hierarchy from visiting parents in this algorithm.
    if (displayRoot) {
        displayRoot.parent = null;
    }
    myChart.setOption({
        dataset: {
        source: seriesData
        }
    });
    }
    
    // Reset: click on the blank area.
    myChart.getZr().on('click', function (event) {
    if (!event.target) {
        drillDown();
    }
    });
}

// 初始化图表
function init() {
    const mockData = createMockData();
    const dataWrap = prepareData(mockData);
    initChart(dataWrap.seriesData, dataWrap.maxDepth);
}

// 页面加载完成后初始化
$(document).ready(function() {
    // 确保d3加载完成
    if (typeof d3 === 'undefined') {
    console.error('D3.js not loaded properly');
    return;
    }
    init();
    
    // 监听窗口大小变化
    window.addEventListener('resize', function() {
    myChart.resize();
    });
});

// 如果直接加载d3失败，使用备用方案
function checkAndInit() {
    if (typeof d3 !== 'undefined' && d3.stratify) {
    init();
    } else {
    setTimeout(checkAndInit, 100);
    }
}


</script>

<template>
    <div id="main" style="height: 100%"></div>
</template>