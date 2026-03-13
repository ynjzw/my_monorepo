<template>
  <div class="skill-resource">
    <h1>技能与资源</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <textarea
          id="skills"
          v-model="skills"
          placeholder="请输入您的技能，例如：编程、设计、写作等"
          rows="4"
        ></textarea>
      </div>
      <div class="form-group">
        <textarea
          id="resource"
          v-model="resource"
          placeholder="请输入您愿意提供的资源，例如：土地，空间，金钱等"
          rows="4"
        ></textarea>
      </div>
      <div class="form-group">
        <textarea
          id="wish"
          v-model="wish"
          placeholder="请许下你的愿望"
          rows="4"
        ></textarea>
      </div>      
      <button type="submit" class="submit-btn">提交</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 响应式数据
const skills = ref('')
const resource = ref('')
const wish = ref('')

// 提交表单
const submitForm = () => {
  console.log('技能:', skills.value)
  console.log('资源', resource.value)
  console.log('愿望', wish.value)
  // 这里可以添加提交逻辑，比如发送到服务器
  alert('信息已提交！')
}
</script>

<style scoped>
.skill-resource {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: greenyellow;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  resize: vertical;
  transition: border-color 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 5px rgba(74, 144, 226, 0.3);
}

.submit-btn {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #357abd;
}
</style>