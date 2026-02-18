
<template>
  <div class="upload-form">
    <h2>Upload File</h2>
    <form @submit.prevent="handleUpload()">
      <input type="file" @change="onFileChange(x)" /><br>
      <button type="submit" @click="uploadFile()">Upload</button>
    </form>
    <div class="mes" v-if="message">{{ message }}</div>
  </div>
  <p>{{ props.msg }}</p>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { uploadFile } from '@/api/index';

const file = ref(null);
const message = ref(null);
const props=defineProps({
  msg:String
})
const onFileChange = () => {
  console.log('aaa')
};

const handleUpload = async () => {
  if (!file.value) {
    message.value = 'Please select a file to upload.';
    return;
  }
  console.log('ccc')
  try {
    const response = await uploadFile(file.value);
    message.value = response.data.message;
  } catch (error) {
    message.value = 'Error uploading file.';
  }
};

onMounted( {
  onFileChange,
  handleUpload,
  message,
});
</script>

<style scoped>
.upload-form {
  max-width: 400px;
  margin: auto;
}
.mes {
  color: red;
}
</style>