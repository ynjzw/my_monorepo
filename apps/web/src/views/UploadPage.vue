<template>
  <div class="upload-page">
    <h1>File Upload</h1>
    <UploadForm @file-uploaded="handleFileUploaded" />
  </div>
</template>

<script >
import { defineComponent } from 'vue';
import UploadForm from '../components/UploadForm.vue';

export default defineComponent({
  name: 'UploadPage',
  components: {
    UploadForm,
  },
  methods: {
    handleFileUploaded() {
      // Handle the response after file upload
      console.log('File uploaded successfully:', response);
    },
  },
});
</script>

<style scoped>
.upload-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}
</style>