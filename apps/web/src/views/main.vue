<template>
  <div class="voice-visualizer">   
    <canvas ref="canvasRef" width="400" height="400"></canvas>
    <div class="button-group">
      <button 
        @click="startMicrophone" 
        :disabled="isActive"
        class="btn start-btn"
      >
        {{ isActive ? '🎤 麦克风已激活' : '🎤 启动麦克风' }}
      </button>
      
      <button 
        @click="stopMicrophone" 
        :disabled="!isActive"
        class="btn stop-btn"
      >
        ⏹️ 关闭麦克风
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { chat,speechtotext } from '@/api'
import { useRouter } from 'vue-router';

// 响应式状态
const canvasRef = ref(null)
const isActive = ref(false)
const volumeLevel = ref(0)
const visualMode = ref('circle') // 'circle' 或 'sphere'
const text = ref('')
const router=useRouter()
// 音频相关变量
let audioContext = null
let analyser = null
let dataArray = null
let bufferLength = 0
let animationFrame = null
let mediaStream = null
// 启动麦克风并导航到 ai_face
// const startMicrophoneAndNavigate = async () => {
//   try {
//     // 先启动麦克风
//     await startMicrophone()
    
    // 麦克风启动成功后，显示提示信息
    // console.log('麦克风启动成功，准备跳转到AI对话界面...')
    
    // 短暂延迟，让用户看到提示
    // setTimeout(() => {
    //   // 导航到 ai_face 视图
    //   router.push({ name: 'ai_face' })
    // }, 1500) // 1.5秒后跳转
    
//   } catch (error) {
//     console.error('启动失败:', error)
//     // 如果启动失败，重置状态
//     isActive.value = false
//   }
// }
// 启动麦克风
const startMicrophone = async () => {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const audioTracks = mediaStream.getAudioTracks();
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    if (audioContext.state === 'suspended') {
      await audioContext.resume()
      
    }    
    if (audioTracks.length > 0 && audioTracks[0].readyState === 'live') {
          alert('✅ 麦克风连接成功');
        } else {
          alert('❌ 麦克风未连接');
        }
    
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 512 // 增加FFT大小以获得更精细的数据
    analyser.smoothingTimeConstant = 0.8
    
    const source = audioContext.createMediaStreamSource(mediaStream)
    source.connect(analyser)
    
    bufferLength = analyser.frequencyBinCount
    dataArray = new Uint8Array(bufferLength)
    // text.value=await speechtotext()
    // console.log(text.value)
    isActive.value = true
    volumeLevel.value = 0
    
    drawVisualizer()
    
  } catch (error) {
    console.error('无法访问麦克风:', error)
    alert('无法访问麦克风，请确保已授予权限')
    isActive.value = false
  }
}

// 关闭麦克风
const stopMicrophone = () => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
    animationFrame = null
  }
  
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }
  
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => {
      track.stop()
    })
    mediaStream = null
  }
  
  clearCanvas()
  
  isActive.value = false
  volumeLevel.value = 0
}

// 清空画布
const clearCanvas = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = 'rgb(0, 0, 0)'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'
  ctx.font = '20px Arial'
  ctx.textAlign = 'center'
  ctx.fillText('麦克风已关闭', canvas.width / 2, canvas.height / 2)
}

// 计算音量级别
const calculateVolume = (dataArray) => {
  let sum = 0
  for (let i = 0; i < dataArray.length; i++) {
    sum += dataArray[i]
  }
  const average = sum / dataArray.length
  return Math.round((average / 255) * 100)
}

// 绘制圆形波纹效果
const drawCircleWave = (ctx, canvas, dataArray) => {
  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const maxRadius = Math.min(centerX, centerY) - 20
  
  // 清空画布并设置渐变背景
  const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
  gradient.addColorStop(0, '#0a0a2a')
  gradient.addColorStop(1, '#1a1a3a')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // 绘制外圈刻度
  for (let i = 0; i < 360; i += 30) {
    const angle = (i * Math.PI) / 180
    const x1 = centerX + Math.cos(angle) * (maxRadius + 10)
    const y1 = centerY + Math.sin(angle) * (maxRadius + 10)
    const x2 = centerX + Math.cos(angle) * (maxRadius + 20)
    const y2 = centerY + Math.sin(angle) * (maxRadius + 20)
    
    ctx.beginPath()
    ctx.strokeStyle = 'rgba(100, 150, 255, 0.3)'
    ctx.lineWidth = 2
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()
  }
  
  // 绘制多层波纹
  const layers = 8
  for (let layer = 0; layer < layers; layer++) {
    const layerOffset = (Date.now() * 0.002) % (Math.PI * 2)
    const baseRadius = (maxRadius / layers) * (layer + 1)
    
    ctx.beginPath()
    
    for (let i = 0; i <= 360; i += 5) {
      const angle = (i * Math.PI) / 180
      
      // 根据音频数据计算半径变形
      const dataIndex = Math.floor((i / 360) * bufferLength)
      const audioValue = dataArray[dataIndex] / 255
      
      // 波纹变形
      const wave1 = Math.sin(angle * 4 + layerOffset) * 5
      const wave2 = Math.sin(angle * 8 + layerOffset * 2) * 3
      const radius = baseRadius + (audioValue * 20) + wave1 + wave2
      
      const x = centerX + Math.cos(angle) * radius
      const y = centerY + Math.sin(angle) * radius
      
      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    }
    
    ctx.closePath()
    
    // 设置渐变颜色
    const opacity = 0.3 - (layer / layers) * 0.2
    const hue = (layer * 30 + Date.now() * 0.02) % 360
    
    ctx.strokeStyle = `hsla(${hue}, 80%, 60%, ${opacity})`
    ctx.lineWidth = 2
    ctx.stroke()
    
    // 填充内圈
    if (layer === 0) {
      ctx.fillStyle = `hsla(${hue}, 80%, 50%, 0.1)`
      ctx.fill()
    }
  }
  
  // 绘制中心点
  ctx.beginPath()
  ctx.arc(centerX, centerY, 10 + volumeLevel.value / 5, 0, Math.PI * 2)
  ctx.fillStyle = `hsl(${Date.now() * 0.05 % 360}, 80%, 60%)`
  ctx.shadowColor = 'rgba(0, 255, 255, 0.5)'
  ctx.shadowBlur = 20
  ctx.fill()
  ctx.shadowBlur = 0
}

// 绘制3D球体效果
const drawSphere = (ctx, canvas, dataArray) => {
  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const maxRadius = Math.min(centerX, centerY) - 30
  
  // 清空画布
  ctx.fillStyle = '#000'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // 计算平均音量
  let sum = 0
  for (let i = 0; i < dataArray.length; i++) {
    sum += dataArray[i]
  }
  const avgVolume = sum / dataArray.length / 255
  
  // 绘制球体
  for (let y = -maxRadius; y <= maxRadius; y += 2) {
    for (let x = -maxRadius; x <= maxRadius; x += 2) {
      const distance = Math.sqrt(x * x + y * y)
      if (distance <= maxRadius) {
        // 计算球体上的z坐标
        const z = Math.sqrt(maxRadius * maxRadius - distance * distance)
        
        // 根据音频数据计算颜色
        const angle = Math.atan2(y, x)
        const dataIndex = Math.floor(((angle + Math.PI) / (Math.PI * 2)) * bufferLength)
        const audioValue = dataArray[dataIndex] / 255
        
        // 3D光照效果
        const lightAngle = Date.now() * 0.002
        const lightX = Math.sin(lightAngle) * maxRadius
        const lightY = Math.cos(lightAngle) * maxRadius
        const lightZ = 0
        
        // 计算漫反射
        const nx = x / maxRadius
        const ny = y / maxRadius
        const nz = z / maxRadius
        
        const lx = (lightX - x) / maxRadius
        const ly = (lightY - y) / maxRadius
        const lz = (lightZ - z) / maxRadius
        
        const dot = nx * lx + ny * ly + nz * lz
        const brightness = Math.max(0.2, dot) * (0.7 + audioValue * 0.3)
        
        // 根据音频频率设置颜色
        const hue = (dataIndex / bufferLength) * 360
        const saturation = 70 + audioValue * 30
        
        // 绘制像素
        ctx.fillStyle = `hsl(${hue}, ${saturation}%, ${brightness * 60}%)`
        ctx.fillRect(centerX + x, centerY + y, 2, 2)
      }
    }
  }
  
  // 绘制外圈光环
  ctx.beginPath()
  ctx.arc(centerX, centerY, maxRadius + 5 + Math.sin(Date.now() * 0.005) * 5, 0, Math.PI * 2)
  ctx.strokeStyle = `hsla(${Date.now() * 0.05 % 360}, 80%, 60%, 0.3)`
  ctx.lineWidth = 2
  ctx.stroke()
}

// 绘制可视化效果
const drawVisualizer = () => {
  const canvas = canvasRef.value
  if (!canvas || !analyser) return
  
  const ctx = canvas.getContext('2d')
  
  const draw = () => {
    if (!isActive.value || !analyser) {
      return
    }
    
    analyser.getByteFrequencyData(dataArray)
    volumeLevel.value = calculateVolume(dataArray)
    
    // 根据选择的模式绘制不同的效果
    if (visualMode.value === 'circle') {
      drawCircleWave(ctx, canvas, dataArray)
    } else {
      drawSphere(ctx, canvas, dataArray)
    }
    
    // 绘制音量文字
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)'
    ctx.font = '16px Arial'
    ctx.textAlign = 'right'
    ctx.fillText(`音量: ${volumeLevel.value}%`, canvas.width - 20, 30)
    
    animationFrame = requestAnimationFrame(draw)
  }
  
  draw()
}

// 组件卸载前清理
onBeforeUnmount(() => {
  stopMicrophone()
})
</script>

<style scoped>
.voice-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

canvas {
  border: 3px solid #4a4a6a;
  border-radius: 12px;
  background: #000;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  max-width: 100%;
  height: auto;
  transition: all 0.3s ease;
}

canvas:hover {
  border-color: #667eea;
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.3);
}

.button-group {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn {
  padding: 12px 30px;
  font-size: 16px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  letter-spacing: 0.5px;
  min-width: 160px;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
  width: 300px;
  height: 300px;
}

.btn:active {
  transform: scale(0.95);
}

.start-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.start-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.stop-btn {
  background: linear-gradient(135deg, #f56565 0%, #c53030 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(245, 101, 101, 0.4);
}

.stop-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 101, 101, 0.6);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn:disabled::before {
  display: none;
}

.volume-indicator {
  width: 300px;
  height: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  overflow: hidden;
  position: relative;
  border: 2px solid #4a4a6a;
}

.volume-bar {
  height: 100%;
  background: linear-gradient(90deg, #4ade80, #3b82f6, #8b5cf6);
  transition: width 0.1s ease;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

.volume-indicator span {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 14px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.mode-selector {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.mode-btn {
  padding: 8px 20px;
  font-size: 14px;
  border: 2px solid #4a4a6a;
  border-radius: 25px;
  background: transparent;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mode-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.mode-btn:hover {
  border-color: #667eea;
  transform: translateY(-2px);
}
</style>