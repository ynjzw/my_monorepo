<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const encouragements = [
  '慢慢来，灵感会在路上遇见你。',
  '今天也在认真构建自己的世界。',
  '先完成一小步，就已经很棒啦。',
  '记得喝口水，给大脑一点休息时间。'
]

const position = ref(null)
const isOpen = ref(false)
const isHidden = ref(false)
const isDragging = ref(false)
const message = ref('嗨！我会在这里陪你一起工作。')
const panelSide = ref('left')
const panelBelow = ref(false)
const dragOrigin = ref(null)
let movedDuringDrag = false
let suppressClick = false
let encouragementIndex = 0

const petStyle = computed(() => position.value
  ? { left: `${position.value.x}px`, top: `${position.value.y}px` }
  : {})

const panelStyle = computed(() => ({
  [panelSide.value === 'left' ? 'right' : 'left']: '0',
  [panelBelow.value ? 'top' : 'bottom']: '82px'
}))

function clampPosition(x, y) {
  const size = 72
  return {
    x: Math.max(8, Math.min(x, window.innerWidth - size - 8)),
    y: Math.max(8, Math.min(y, window.innerHeight - size - 8))
  }
}

function updatePanelPlacement() {
  if (!position.value) return
  panelSide.value = position.value.x + 36 > window.innerWidth / 2 ? 'left' : 'right'
  panelBelow.value = position.value.y < 230
}

function handlePointerDown(event) {
  if (event.button !== 0) return
  const rect = event.currentTarget.getBoundingClientRect()
  dragOrigin.value = {
    pointerX: event.clientX,
    pointerY: event.clientY,
    x: rect.left,
    y: rect.top
  }
  movedDuringDrag = false
  isDragging.value = true
  event.currentTarget.setPointerCapture(event.pointerId)
}

function handlePointerMove(event) {
  if (!isDragging.value || !dragOrigin.value) return
  const deltaX = event.clientX - dragOrigin.value.pointerX
  const deltaY = event.clientY - dragOrigin.value.pointerY
  if (Math.abs(deltaX) > 5 || Math.abs(deltaY) > 5) movedDuringDrag = true
  if (movedDuringDrag) {
    position.value = clampPosition(dragOrigin.value.x + deltaX, dragOrigin.value.y + deltaY)
    updatePanelPlacement()
  }
}

function handlePointerUp() {
  if (!isDragging.value) return
  isDragging.value = false
  if (movedDuringDrag) suppressClick = true
  dragOrigin.value = null
}

function handlePetClick() {
  if (suppressClick) {
    suppressClick = false
    return
  }
  isOpen.value = !isOpen.value
}

function cheerUp() {
  message.value = encouragements[encouragementIndex % encouragements.length]
  encouragementIndex += 1
}

function handleResize() {
  if (!position.value) return
  position.value = clampPosition(position.value.x, position.value.y)
  updatePanelPlacement()
}

onMounted(() => {
  position.value = clampPosition(window.innerWidth - 96, window.innerHeight - 98)
  updatePanelPlacement()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div v-if="!isHidden" class="desktop-pet" :class="{ 'is-dragging': isDragging }" :style="petStyle">
    <Transition name="pet-pop">
      <section v-if="isOpen" class="pet-panel" :style="panelStyle" aria-label="桌宠对话">
        <div class="panel-heading">
          <div class="panel-avatar" aria-hidden="true">🐱</div>
          <div>
            <strong>小团子</strong>
            <span class="online-status"><i></i> 陪伴中</span>
          </div>
          <button class="panel-close" type="button" aria-label="关闭对话框" @click="isOpen = false">×</button>
        </div>
        <p class="pet-message">{{ message }}</p>
        <div class="pet-actions">
          <button type="button" @click="cheerUp">给我一点灵感 <span aria-hidden="true">✦</span></button>
          <button type="button" @click="isHidden = true; isOpen = false">先藏起来</button>
        </div>
        <span class="panel-hint">拖动我，可以换个位置</span>
      </section>
    </Transition>

    <button
      class="pet-button"
      type="button"
      aria-label="打开桌宠小团子的对话"
      :aria-expanded="isOpen"
      @pointerdown="handlePointerDown"
      @pointermove="handlePointerMove"
      @pointerup="handlePointerUp"
      @pointercancel="handlePointerUp"
      @click="handlePetClick"
    >
      <span class="pet-shadow"></span>
      <span class="pet-body">
        <span class="pet-ear pet-ear-left"></span>
        <span class="pet-ear pet-ear-right"></span>
        <span class="pet-face">
          <i class="pet-eye pet-eye-left"></i>
          <i class="pet-eye pet-eye-right"></i>
          <i class="pet-blush pet-blush-left"></i>
          <i class="pet-blush pet-blush-right"></i>
          <i class="pet-nose"></i>
        </span>
        <span class="pet-belly"></span>
      </span>
      <span class="pet-sparkle sparkle-one">✦</span>
      <span class="pet-sparkle sparkle-two">·</span>
    </button>
  </div>

  <button
    v-else
    class="pet-reopen"
    type="button"
    aria-label="重新显示桌宠"
    @click="isHidden = false"
  >🐾</button>
</template>

<style scoped>
.desktop-pet {
  position: fixed;
  z-index: 1000;
  width: 72px;
  height: 72px;
  touch-action: none;
  user-select: none;
}

.pet-button {
  position: relative;
  display: block;
  width: 72px;
  height: 72px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: grab;
  touch-action: none;
  -webkit-tap-highlight-color: transparent;
}

.pet-button:focus-visible,
.pet-reopen:focus-visible,
.pet-panel button:focus-visible {
  outline: 3px solid #818cf8;
  outline-offset: 4px;
}

.is-dragging .pet-button {
  cursor: grabbing;
}

.pet-shadow {
  position: absolute;
  right: 7px;
  bottom: 1px;
  left: 7px;
  height: 12px;
  border-radius: 50%;
  background: rgb(56 47 94 / 16%);
  filter: blur(5px);
}

.pet-body {
  position: absolute;
  inset: 9px 7px 5px;
  display: block;
  border: 2px solid #594d71;
  border-radius: 48% 48% 45% 45%;
  background: linear-gradient(145deg, #fffdf8 8%, #f5eefe 88%);
  box-shadow: inset -5px -5px 0 rgb(206 188 230 / 22%), 0 5px 0 #d9c9e8;
  animation: pet-bob 2.4s ease-in-out infinite;
}

.pet-ear {
  position: absolute;
  top: -5px;
  z-index: -1;
  width: 22px;
  height: 24px;
  border: 2px solid #594d71;
  border-radius: 75% 25% 35% 35%;
  background: #f7effc;
}

.pet-ear-left {
  left: 2px;
  transform: rotate(-20deg);
}

.pet-ear-right {
  right: 2px;
  transform: scaleX(-1) rotate(-20deg);
}

.pet-face {
  position: absolute;
  inset: 0;
}

.pet-eye {
  position: absolute;
  top: 24px;
  width: 5px;
  height: 7px;
  border-radius: 50%;
  background: #494158;
}

.pet-eye-left {
  left: 15px;
}

.pet-eye-right {
  right: 15px;
}

.pet-blush {
  position: absolute;
  top: 34px;
  width: 8px;
  height: 4px;
  border-radius: 50%;
  background: #f4a8ba;
  opacity: 0.8;
}

.pet-blush-left {
  left: 8px;
}

.pet-blush-right {
  right: 8px;
}

.pet-nose {
  position: absolute;
  top: 32px;
  left: 50%;
  width: 4px;
  height: 3px;
  border-radius: 50%;
  background: #c97a91;
  transform: translateX(-50%);
}

.pet-belly {
  position: absolute;
  right: 15px;
  bottom: 5px;
  left: 15px;
  height: 14px;
  border-radius: 50%;
  background: rgb(240 226 247 / 75%);
}

.pet-sparkle {
  position: absolute;
  color: #f4bf62;
  font-weight: 800;
  pointer-events: none;
}

.sparkle-one {
  top: 0;
  right: 2px;
  font-size: 15px;
}

.sparkle-two {
  top: 17px;
  left: -2px;
  color: #9c8ac5;
  font-size: 22px;
}

.pet-panel {
  position: absolute;
  z-index: 1;
  width: 260px;
  padding: 17px;
  border: 1px solid #eee8f5;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 14px 40px rgb(52 42 74 / 16%);
  color: #312b40;
  font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
  text-align: left;
  touch-action: auto;
  user-select: text;
}

.panel-heading {
  display: flex;
  align-items: center;
  gap: 10px;
}

.panel-avatar {
  display: grid;
  width: 38px;
  height: 38px;
  place-items: center;
  border-radius: 13px;
  background: #f4edfb;
  font-size: 22px;
}

.panel-heading strong,
.online-status {
  display: block;
}

.panel-heading strong {
  font-size: 14px;
  line-height: 20px;
}

.online-status {
  margin-top: 1px;
  color: #8a8397;
  font-size: 11px;
  line-height: 16px;
}

.online-status i {
  display: inline-block;
  width: 6px;
  height: 6px;
  margin-right: 4px;
  border-radius: 50%;
  background: #61c69a;
  vertical-align: 1px;
}

.panel-close {
  display: grid;
  width: 28px;
  height: 28px;
  margin-left: auto;
  padding: 0;
  place-items: center;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: #9891a3;
  font-size: 22px;
  cursor: pointer;
}

.panel-close:hover {
  background: #f6f3f9;
}

.pet-message {
  min-height: 42px;
  margin: 15px 0 13px;
  padding: 11px 12px;
  border-radius: 12px 12px 12px 4px;
  background: #f7f3fb;
  color: #554b68;
  font-size: 13px;
  line-height: 20px;
}

.pet-actions {
  display: grid;
  gap: 7px;
}

.pet-actions button {
  min-height: 34px;
  padding: 7px 10px;
  border: 1px solid #eee8f5;
  border-radius: 9px;
  background: #fff;
  color: #615673;
  font: inherit;
  font-size: 12px;
  text-align: left;
  cursor: pointer;
}

.pet-actions button:first-child {
  border-color: #e7dcf6;
  background: #f7f2fc;
  color: #6a4f91;
}

.pet-actions button:hover {
  border-color: #cdb9e4;
}

.pet-actions button span {
  float: right;
  color: #b38bdc;
}

.panel-hint {
  display: block;
  margin-top: 10px;
  color: #a29bab;
  font-size: 10px;
  text-align: center;
}

.pet-reopen {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 1000;
  display: grid;
  width: 44px;
  height: 44px;
  padding: 0;
  place-items: center;
  border: 1px solid #e8def3;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 6px 20px rgb(52 42 74 / 14%);
  font-size: 21px;
  cursor: pointer;
}

.pet-pop-enter-active,
.pet-pop-leave-active {
  transition: opacity 0.16s ease, transform 0.16s ease;
}

.pet-pop-enter-from,
.pet-pop-leave-to {
  opacity: 0;
  transform: translateY(6px) scale(0.97);
}

@keyframes pet-bob {
  0%, 100% {
    transform: translateY(0) rotate(-2deg);
  }
  50% {
    transform: translateY(-4px) rotate(2deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .pet-body {
    animation: none;
  }

  .pet-pop-enter-active,
  .pet-pop-leave-active {
    transition: none;
  }
}
</style>
