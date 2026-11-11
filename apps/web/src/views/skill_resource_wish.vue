<template>
  <div class="skill-resource">
    <h1>技能与资源</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <span>技能(请填写您掌握的技能)：</span>
        <textarea
          id="skills"
          v-model="skill"
          placeholder="请输入您的技能，例如：编程、设计、写作等"
          rows="4"
        ></textarea>
      </div>
      <div class="form-group">
        <span>资源(请填写您愿意提供的资源)：</span>
        <textarea
          id="resource"
          v-model="resource"
          placeholder="请输入您愿意提供的资源，例如：土地，空间，金钱等"
          rows="4"
        ></textarea>
      </div>
      <div class="form-group">
        <span>愿望(请许下你的愿望)：</span>
        <textarea
          id="wish"
          v-model="wish"
          placeholder=""
          rows="4"
        ></textarea>
      </div>      
      <button type="submit" class="submit-btn">提交</button>
    </form>
  </div>
</template>

<script setup>
import { ref ,onMounted} from 'vue'
import { get_personal_data,update_personal_data } from '@/api/simple_api'

// 响应式数据
const skill = ref('')
const resource = ref('')
const wish = ref('')
const response = ref(null)

// 提交表单
const submitForm = async () => {
  // 这里可以添加提交逻辑，比如发送到服务器
  
  try {
    response.value = await update_personal_data({
      skill: skill.value,
      resource: resource.value,
      wish: wish.value,
      user_id: '1'
    })
    console.log('提交成功:', response.value)
  } catch (error) {
    console.error('提交失败:', error)
  }
}
onMounted(async () => {
  try {
    response.value = await get_personal_data()
    skill.value = response.value.skill
    resource.value = response.value.resource
    wish.value = response.value.wish
  } catch (error) {
    console.error('获取个人数据失败:', error)
  }
})
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