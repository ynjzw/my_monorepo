
<template>
  <div class="upload-form">
    <h2>Upload File</h2>
    <form @submit.prevent="handleUpload">
      <input type="file" @change="onFileChange" />
      <button type="submit">Upload</button>
    </form>
    <div v-if="message">{{ message }}</div>
  </div>
</template>

<script >
import { ref } from 'vue';
import { getJs } from '../api/index';

export default {
  setup() {
    const file = ref(null);
    const message = ref(null);

    const onFileChange = () => {
      const x= getJs()
      console.log(x)
    };

    const handleUpload = async () => {
      if (!file.value) {
        message.value = 'Please select a file to upload.';
        return;
      }

      try {
        const response = await uploadFile(file.value);
        message.value = response.data.message;
      } catch (error) {
        message.value = 'Error uploading file.';
      }
    };

    return {
      onFileChange,
      handleUpload,
      message,
    };
  },
};
</script>

<style scoped>
.upload-form {
  max-width: 400px;
  margin: auto;
  text-align: center;
}

.upload-form input {
  margin-bottom: 10px;
}
</style>