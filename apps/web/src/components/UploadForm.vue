<template>
  <div class="upload-form">
    <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
      <div class="upload-icon">📁</div>
      <p>{{ props.msg }}</p>
      
      <input
        ref="fileInput"
        type="file"
        @change="onFileChange"
        class="file-input"
        :disabled="uploading"
      />
      
      <button 
        type="primary" 
        @click="triggerFileInput"
        :disabled="uploading"
      >
        选择文件
      </button>
    </div>

    <!-- 显示选择的文件 -->
    <div v-if="selectedFile" class="file-info">
      <p>已选择: {{ selectedFile.name }}</p>
      <p>大小: {{ formatFileSize(selectedFile.size) }}</p>
    </div>

    <!-- 上传按钮 -->
    <div class="actions">
      <button 
        type="success" 
        @click="handleUpload" 
        :loading="uploading"
        :disabled="!selectedFile"
      >
        {{ uploading ? '上传中...' : '开始上传' }}
      </button>
      
      <button @click="resetForm" :disabled="uploading">
        清空
      </button>
    </div>

    <!-- 提示信息 -->
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { uploadFile } from '@/api/index';

const props = defineProps({
  msg: {
    type: String,
    default: '请选择要上传的文件'
  }
});

// 状态变量
const fileInput = ref(null);
const selectedFile = ref(null);
const uploading = ref(false);
const message = ref('');
const messageType = ref('info');

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click();
};

// 文件选择变化
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    // 验证文件大小（10MB）
    if (file.size > 10 * 1024 * 1024) {
      window.alert('文件大小不能超过 10MB');
      resetForm();
      return;
    }
    
    selectedFile.value = file;
    message.value = '';
  }
};

// 处理拖拽
const handleDrop = (event) => {
  const file = event.dataTransfer.files[0];
  if (file) {
    // 更新 file input
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.value.files = dataTransfer.files;
    
    selectedFile.value = file;
    message.value = '';
  }
};

// 上传文件
const handleUpload = async () => {
  if (!selectedFile.value) {
    message.value = '请先选择文件';
    messageType.value = 'error';
    return;
  }

  uploading.value = true;
  message.value = '上传中...';
  messageType.value = 'info';

  try {
    const formData = new FormData();
    formData.append('file', selectedFile.value);
    
    const response = await uploadFile(formData);
    console.log(response)
    message.value = response.data || '上传成功';
    messageType.value = 'success';
    
    // 成功后延迟清空
    setTimeout(() => {
      resetForm();
    }, 2000);
    
  } catch (error) {
    console.error('上传失败:', error);
    message.value = error.response?.data?.message || '上传失败，请重试';
    messageType.value = 'error';
  } finally {
    uploading.value = false;
  }
};

// 重置表单
const resetForm = () => {
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  selectedFile.value = null;
  message.value = '';
};

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

defineExpose({
  resetForm
});
</script>

<style scoped>
.upload-form {
  max-width: 500px;
  margin: auto;
  padding: 30px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #fafafa;
}

.upload-area:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.file-input {
  display: none;
}

.file-info {
  margin: 20px 0;
  padding: 15px;
  background-color: #f0f9ff;
  border-radius: 4px;
  border-left: 4px solid #409eff;
}

.file-info p {
  margin: 5px 0;
  color: #333;
}

.actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.message {
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.message.info {
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.message.success {
  background-color: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.message.error {
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
  color: #f5222d;
}

.message.warning {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  color: #faad14;
}
</style>