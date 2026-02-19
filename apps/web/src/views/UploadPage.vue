<template>
  <div class="upload-page">
    <UploadForm @file-uploaded="handleFileUploaded" />    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import UploadForm from '@/components/UploadForm.vue';

const handleFileUploaded = () => {
    // Handle the response after file upload
    console.log('File uploaded successfully:', response);
  }
</script>

<style scoped>
.upload-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}
</style>