<template>
  <div class="upload-page">
    <UploadForm      
      msg="请选择要上传的文件"
    />    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import UploadForm from '@/components/UploadForm.vue';

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