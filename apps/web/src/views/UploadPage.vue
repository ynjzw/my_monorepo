<template>
  <div class="upload-page">
    <h1>File Upload</h1>
    <UploadForm @file-uploaded="handleFileUploaded" :msg="jjsdjd"/>
    <p>{{ msg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import UploadForm from '../components/UploadForm.vue';

const msg=ref('wdhuwdhj')
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