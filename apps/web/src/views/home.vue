<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import personGif from '../images/person.gif'
import worldGif from '../images/world.gif'

const vantaRef = ref(null)
let vantaEffect = null

onMounted(() => {
  if (!vantaRef.value || !window.VANTA || !window.VANTA.NET) {                                 
    return
  }

  vantaEffect = window.VANTA.NET({
    el: vantaRef.value,
    mouseControls: true,
    touchControls: true,
    gyroControls: false,
    minHeight: 800.0,
    minWidth: 800.0,
    blurFactor: 0.5,
    speed: 1.2,
    zoom: 1.0,
  })
})

onBeforeUnmount(() => {
  if (vantaEffect && typeof vantaEffect.destroy === 'function') {
    vantaEffect.destroy()
  }
  vantaEffect = null
})
</script>

<template>
  <div ref="vantaRef" class="vanta-scene">
    <div class="container">
      <div class="taiji">
        <img class="person" :src="personGif" @click="$router.push({ name: 'person' })">
        <img class="world" :src="worldGif" @click="$router.push({ name: 'world' })">
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

.vanta-scene {
  position: relative;
  width: 100%;
  min-height: calc(100vh - 34px);
  overflow: hidden;
  background: #050816;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 34px);
  position: relative;
  z-index: 1;
}

.taiji {
  width: 300px;
  height: 300px;
  margin-left: 0%;
  margin-top: 5%;
  background-color: #000;
  border: 0px solid #fff;
  border-radius: 50%;
  background: linear-gradient(to right, black 50%, white 50%);
  position: relative;
  animation: rota 10s linear infinite;
  opacity: 50%;
  overflow: hidden;
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.18);
}

.taiji:hover {
  animation-play-state: paused;
}

.person {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: -webkit-radial-gradient(center, white 20%, black 20%);
  position: absolute;
  top: 0;
  left: 75px;
}

.world {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: -webkit-radial-gradient(center, black 20%, white 20%);
  position: absolute;
  bottom: 0;
  left: 75px;
}

@keyframes rota {
  0% {
    transform: rotate(0);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>

