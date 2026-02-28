<script setup>
import personGif from '../images/person.gif'
import worldGif from '../images/world.gif'
</script>

<template>
  <div class="container">
    <div class="taiji">
            <img class="person" :src="personGif" @click="$router.push({'name':'person'})">
            <img class="world" :src="worldGif" @click="$router.push({'name':'world'})">
    </div>
  </div>
</template>

<style scoped>

*{margin: 0;padding: 0;}
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.taiji{
    width: 300px;
    height: 300px;
    margin-left:0%;
    margin-top:5%;
    background-color: #000;
    border: 0px solid #fff;
    border-radius: 50%;
    background: linear-gradient(to right,black 50%,white 50%);
    position: relative;
    animation: rota 10s linear infinite;
    opacity: 50%;
    overflow: hidden;
}
.taiji:hover{
    animation-play-state: paused;
}
.person{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: -webkit-radial-gradient(center,white 20%,black 20%);
    position: absolute;
    top: 0;
    left: 75px;
}
.world{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: -webkit-radial-gradient(center,black 20%,white 20%);
    position: absolute;
    bottom: 0;
    left: 75px;
}

@keyframes rota {
    0%{
        transform: rotate(0);
    }
    100%{
        transform: rotate(360deg);
    }
}

</style>

