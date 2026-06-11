<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`节点详情 - ${nodeData?.name || '未知节点'}`"
    width="500px"
    :before-close="handleClose"
    destroy-on-close
  >
    <div class="node-dialog-content">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="节点名称">
          <el-tag type="primary">{{ nodeData?.name || '-' }}</el-tag>
        </el-descriptions-item>
        
        <el-descriptions-item label="节点值">
          <el-tag type="success">{{ nodeData?.value || '-' }}</el-tag>
        </el-descriptions-item>
        
        <el-descriptions-item label="分类" v-if="nodeData?.category">
          {{ nodeData.category }}
        </el-descriptions-item>
        
        <el-descriptions-item label="节点大小">
          {{ nodeData?.symbolSize || 50 }}
        </el-descriptions-item>
        
        <el-descriptions-item label="自定义属性" v-if="hasCustomProps">
          <div class="custom-props">
            <div 
              v-for="(value, key) in customProps" 
              :key="key"
              class="prop-item"
            >
              <span class="prop-key">{{ key }}:</span>
              <span class="prop-value">{{ formatValue(value) }}</span>
            </div>
          </div>
        </el-descriptions-item>
      </el-descriptions>
      
      <!-- 如果有更详细的信息，可以添加额外的区块 -->
      <div v-if="nodeData?.description" class="description-section">
        <h4>描述</h4>
        <p>{{ nodeData.description }}</p>
      </div>
      
      <!-- 如果有关联的链接信息，可以显示 -->
      <div v-if="relatedLinks.length > 0" class="related-links">
        <h4>关联关系</h4>
        <el-timeline>
          <el-timeline-item 
            v-for="(link, index) in relatedLinks" 
            :key="index"
            :timestamp="link.relation || '关联'"
            placement="top"
          >
            {{ link.source }} → {{ link.target }}
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handleEdit" v-if="editable">
          编辑
        </el-button>
        <el-button type="danger" @click="handleDelete" v-if="deletable">
          删除
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// Props 定义
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  nodeData: {
    type: Object,
    default: null
  },
  editable: {
    type: Boolean,
    default: false
  },
  deletable: {
    type: Boolean,
    default: false
  },
  allLinks: {
    type: Array,
    default: () => []
  }
})

// Emits 定义
const emit = defineEmits([
  'update:visible',
  'close',
  'edit',
  'delete'
])

// 本地响应式数据
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

// 计算自定义属性（排除标准字段）
const customProps = computed(() => {
  if (!props.nodeData) return {}
  
  const standardKeys = ['name', 'value', 'category', 'symbolSize', 'itemStyle', 'description']
  const custom = {}
  
  Object.keys(props.nodeData).forEach(key => {
    if (!standardKeys.includes(key) && !key.startsWith('_')) {
      custom[key] = props.nodeData[key]
    }
  })
  
  return custom
})

// 是否有自定义属性
const hasCustomProps = computed(() => {
  return Object.keys(customProps.value).length > 0
})

// 获取与当前节点相关的链接
const relatedLinks = computed(() => {
  if (!props.nodeData || !props.allLinks.length) return []
  
  const nodeName = props.nodeData.name
  return props.allLinks.filter(link => 
    link.source === nodeName || link.target === nodeName
  )
})

// 格式化显示值
const formatValue = (value) => {
  if (typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }
  return String(value)
}

// 关闭对话框
const handleClose = () => {
  emit('update:visible', false)
  emit('close')
}

// 编辑节点
const handleEdit = () => {
  emit('edit', props.nodeData)
  handleClose()
}

// 删除节点（带确认）
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除节点 "${props.nodeData?.name}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    emit('delete', props.nodeData)
    handleClose()
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}
</script>

<style scoped>
.node-dialog-content {
  max-height: 500px;
  overflow-y: auto;
}

.custom-props {
  margin-top: 8px;
}

.prop-item {
  padding: 4px 0;
  font-size: 14px;
  border-bottom: 1px dashed #eee;
}

.prop-key {
  font-weight: bold;
  color: #409eff;
  margin-right: 8px;
}

.prop-value {
  color: #666;
  word-break: break-all;
}

.description-section,
.related-links {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.description-section h4,
.related-links h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.description-section p {
  margin: 0;
  line-height: 1.6;
  color: #666;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .node-dialog-content {
    max-height: 400px;
  }
}
</style>