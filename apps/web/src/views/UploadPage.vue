<template>
  <div class="upload-page">
    <h1>文件上传</h1>
    <UploadForm 
      @file-uploaded="handleFileUploaded" 
      msg="请选择要上传的文件"
    />    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import UploadForm from '@/components/UploadForm.vue';

// 处理文件上传成功
const handleFileUploaded = (response) => {
  console.log('文件上传成功:', response);
  ElMessage.success(response.message || '上传成功');
  
  // 可以在这里触发其他操作，如刷新列表
  // refreshFileList();
}
</script>

<style scoped>
.upload-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  padding: 20px;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}
</style>