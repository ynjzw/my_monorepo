<template>
  <main class="illustration-page">
    <div class="stacking-illustration" role="img" aria-label="层层堆叠的方块，右下方有一块橙色方块和箭头标记">
      <div class="block-stack" aria-hidden="true">
        <div class="stack-row row-one">
          <div class="block block-narrow"></div>
          <div class="block"></div>
          <div class="block block-wide"></div>
        </div>
        <div class="stack-row row-two">
          <div class="block block-wide"></div>
          <div class="block"></div>
          <div class="block block-narrow"></div>
        </div>
        <div class="stack-row row-three">
          <div class="block"></div>
          <div class="block block-narrow"></div>
          <div class="block block-wide"></div>
          <div class="block"></div>
        </div>
        <div class="stack-row row-four">
          <div class="block block-wide"></div>
          <div class="block"></div>
          <div class="block block-narrow"></div>
          <div class="block"></div>
        </div>
        <div class="stack-row row-five">
          <div class="block"></div>
          <div class="block block-wide"></div>
          <div class="block"></div>
          <div class="block block-wide"></div>
          <div class="block"></div>
        </div>
        <div class="stack-row row-six">
          <div class="block block-narrow"></div>
          <div class="block"></div>
          <div class="block block-wide"></div>
          <div class="block"></div>
        </div>
        <div class="stack-row row-seven">
          <div class="block"></div>
          <div class="block block-wide"></div>
          <div class="block block-narrow"></div>
          <div class="block"></div>
        </div>
      </div>
      <div class="orange-block"></div>
      <div class="arrow"></div>
    </div>
  </main>
</template>

<style scoped>
.illustration-page {
  display: grid;
  min-height: calc(100vh - 34px);
  min-height: calc(100dvh - 34px);
  place-items: center;
  padding: 16px;
  background: #fff;
}

.stacking-illustration {
  position: relative;
  width: min(460px, 42dvh, 90vw);
  aspect-ratio: 672 / 1168;
}

.block-stack {
  position: absolute;
  inset: 12% 5% 5%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 1%;
}

.stack-row {
  display: flex;
  align-self: center;
  gap: 1%;
  height: 12%;
}

.row-one {
  width: 38%;
  height: 8%;
}

.row-two {
  width: 54%;
  height: 10%;
}

.row-three {
  width: 68%;
  height: 12%;
}

.row-four {
  width: 82%;
  height: 14%;
}

.row-five {
  width: 100%;
  height: 22%;
}

.row-six {
  width: 94%;
  height: 12%;
}

.row-seven {
  width: 100%;
  height: 10%;
}

.block {
  flex: 1;
  border: 2px solid #172033;
  border-radius: 7px;
  background: #f3f3f0;
  box-shadow: 0 3px 0 rgb(23 32 51 / 12%);
}

.block-narrow {
  flex: 0.6;
}

.block-wide {
  flex: 1.5;
}

.orange-block {
  position: absolute;
  right: 17%;
  bottom: 12%;
  width: 14%;
  height: 10%;
  border: 2px solid #d95e0b;
  border-radius: 7px;
  background: #f58222;
  box-shadow: 0 3px 0 rgb(23 32 51 / 15%);
}

.orange-block::after {
  position: absolute;
  right: 28%;
  bottom: -16%;
  left: 28%;
  height: 16%;
  background: #f4b184;
  content: '';
}

.arrow {
  position: absolute;
  right: 2%;
  bottom: 16%;
  width: 17%;
  height: 3px;
  transform: rotate(-15deg);
  transform-origin: right center;
  background: #172033;
}

.arrow::before {
  position: absolute;
  top: 50%;
  left: 0;
  width: 9px;
  height: 9px;
  transform: translateY(-50%) rotate(-45deg);
  border-top: 3px solid #172033;
  border-left: 3px solid #172033;
  content: '';
}

@media (max-width: 600px) {
  .stacking-illustration {
    width: min(90vw, 42dvh);
  }

  .block {
    border-width: 1.5px;
    border-radius: 5px;
  }

  .orange-block {
    border-width: 1.5px;
    border-radius: 5px;
  }
}
</style>
