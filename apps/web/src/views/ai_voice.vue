<template>
  <div class="voice-visualizer">
    <canvas ref="canvasRef" width="800" height="400"></canvas>
    <button 
      @click="startMicrophone" 
      :disabled="isActive"
      class="start-btn"
    >
      {{ isActive ? '🎤 已激活' : '🎤 启动麦克风' }}
    </button>
    <button @click="">stop</button>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'

// 响应式状态
const canvasRef = ref(null)
const isActive = ref(false)

// 音频相关变量
let audioContext = null
let analyser = null
let dataArray = null
let bufferLength = 0
let animationFrame = null

// 启动麦克风
const startMicrophone = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 256
    
    const source = audioContext.createMediaStreamSource(stream)
    source.connect(analyser)
    
    bufferLength = analyser.frequencyBinCount
    dataArray = new Uint8Array(bufferLength)
    
    isActive.value = true
    drawVisualizer()
    
  } catch (error) {
    console.error('无法访问麦克风:', error)
    alert('无法访问麦克风，请确保已授予权限')
  }
}

// 绘制可视化效果
const drawVisualizer = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  
  const draw = () => {
    analyser.getByteFrequencyData(dataArray)
    
    ctx.fillStyle = 'rgb(0, 0, 0)'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    const barWidth = (canvas.width / bufferLength) * 2.5
    let x = 0
    
    for (let i = 0; i < bufferLength; i++) {
      const barHeight = dataArray[i] / 2
      
      // 动态颜色 - 可以根据频率范围变化
      const hue = (i / bufferLength) * 360 // 色相随频率变化
      ctx.fillStyle = `hsl(${hue}, 80%, 60%)`
      
      ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)
      
      x += barWidth + 1
    }
    
    animationFrame = requestAnimationFrame(draw)
  }
  
  draw()
}

// 清理资源
onBeforeUnmount(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
  if (audioContext) {
    audioContext.close()
  }
})
</script>

<style scoped>
.voice-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

canvas {
  border: 2px solid #333;
  border-radius: 8px;
  background: #000;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  height: auto;
}

.start-btn {
  padding: 12px 24px;
  font-size: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.start-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.start-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
}
</style>