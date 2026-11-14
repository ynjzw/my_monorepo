<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isRegister = ref(route.query.mode === 'register')
const showPassword = ref(false)
const email = ref('')
const name = ref('')
const password = ref('')
const confirmPassword = ref('')
const acceptedTerms = ref(false)
const rememberMe = ref(true)
const notice = ref('')

const pageTitle = computed(() => isRegister.value ? '开启你的探索之旅' : '欢迎回来')
const pageDescription = computed(() => isRegister.value
  ? '创建账号，收藏你的灵感与发现。'
  : '登录后继续探索属于你的知识世界。')

function switchMode(register) {
  isRegister.value = register
  notice.value = ''
  password.value = ''
  confirmPassword.value = ''
}

function submitForm() {
  notice.value = ''

  if (isRegister.value && password.value !== confirmPassword.value) {
    notice.value = '两次输入的密码不一致，请检查后重试。'
    return
  }

  if (isRegister.value && !acceptedTerms.value) {
    notice.value = '请先阅读并同意服务条款与隐私政策。'
    return
  }

  notice.value = '页面已就绪；认证服务接口尚未接入，表单信息未提交。'
}
</script>

<template>
  <main class="auth-page">
    <section class="welcome-panel" aria-label="产品介绍">
      <RouterLink class="brand" :to="{ name: 'home' }" aria-label="天人图首页">
        <span class="brand-mark" aria-hidden="true">天</span>
        <span>天人图</span>
      </RouterLink>

      <div class="welcome-copy">
        <span class="eyebrow"><i></i> A SPACE FOR YOUR IDEAS</span>
        <h1>让每一个<br><span>想法彼此连接。</span></h1>
        <p>从灵感出发，构建你的知识图景。<br>在这里，发现思考之间的全新可能。</p>
      </div>

      <div class="orbit-art" aria-hidden="true">
        <div class="orbit orbit-one"></div>
        <div class="orbit orbit-two"></div>
        <div class="orbit orbit-three"></div>
        <span class="orbit-center">天</span>
        <span class="orbit-node node-one">念</span>
        <span class="orbit-node node-two">知</span>
        <span class="orbit-node node-three">行</span>
        <span class="orbit-node node-four">∞</span>
      </div>

      <div class="welcome-footer">
        <span>让思考，看见彼此。</span>
        <span>01 — 04</span>
      </div>
    </section>

    <section class="form-panel">
      <div class="form-wrap">
        <div class="mobile-brand">
          <span class="brand-mark" aria-hidden="true">天</span>
          <span>天人图</span>
        </div>

        <div class="form-heading">
          <span class="form-kicker">{{ isRegister ? 'CREATE YOUR ACCOUNT' : 'YOUR SPACE AWAITS' }}</span>
          <h2>{{ pageTitle }}</h2>
          <p>{{ pageDescription }}</p>
        </div>

        <div class="mode-switch" role="tablist" aria-label="登录或注册">
          <button
            type="button"
            role="tab"
            :aria-selected="!isRegister"
            :class="{ active: !isRegister }"
            @click="switchMode(false)"
          >登录</button>
          <button
            type="button"
            role="tab"
            :aria-selected="isRegister"
            :class="{ active: isRegister }"
            @click="switchMode(true)"
          >注册</button>
        </div>

        <form class="auth-form" @submit.prevent="submitForm">
          <label v-if="isRegister" class="field">
            <span>怎么称呼你</span>
            <span class="input-wrap">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="8" r="3.5" />
                <path d="M5 20c.5-3.5 2.8-5.3 7-5.3s6.5 1.8 7 5.3" />
              </svg>
              <input
                v-model.trim="name"
                type="text"
                name="name"
                placeholder="你的昵称"
                autocomplete="name"
                minlength="2"
                maxlength="30"
                required
              >
            </span>
          </label>

          <label class="field">
            <span>邮箱地址</span>
            <span class="input-wrap">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <rect x="3.5" y="5" width="17" height="14" rx="3" />
                <path d="m5 7 7 5.5L19 7" />
              </svg>
              <input
                v-model.trim="email"
                type="email"
                name="email"
                placeholder="name@example.com"
                autocomplete="email"
                required
              >
            </span>
          </label>

          <label class="field">
            <span>登录密码</span>
            <span class="input-wrap">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <rect x="4" y="10" width="16" height="11" rx="3" />
                <path d="M8 10V7a4 4 0 0 1 8 0v3m-4 5v2" />
              </svg>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                :placeholder="isRegister ? '至少 8 位字符' : '请输入密码'"
                :autocomplete="isRegister ? 'new-password' : 'current-password'"
                :minlength="isRegister ? 8 : 1"
                required
              >
              <button
                class="password-toggle"
                type="button"
                :aria-label="showPassword ? '隐藏密码' : '显示密码'"
                @click="showPassword = !showPassword"
              >
                <svg v-if="showPassword" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M3 3l18 18M10.6 10.6a2 2 0 0 0 2.8 2.8" />
                  <path d="M9.9 5.2A10.7 10.7 0 0 1 12 5c5.5 0 9 7 9 7a14 14 0 0 1-3.1 3.8M6.2 6.2C3.9 7.7 3 12 3 12s3.5 7 9 7c1.1 0 2.1-.3 3-.7" />
                </svg>
                <svg v-else viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M3 12s3.5-7 9-7 9 7 9 7-3.5 7-9 7-9-7-9-7Z" />
                  <circle cx="12" cy="12" r="2.5" />
                </svg>
              </button>
            </span>
            <small v-if="isRegister" class="field-hint">建议使用字母、数字和符号的组合</small>
          </label>

          <label v-if="isRegister" class="field">
            <span>确认密码</span>
            <span class="input-wrap">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <rect x="4" y="10" width="16" height="11" rx="3" />
                <path d="M8 10V7a4 4 0 0 1 8 0v3m-4 5v2" />
              </svg>
              <input
                v-model="confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                name="confirm-password"
                placeholder="再次输入密码"
                autocomplete="new-password"
                minlength="8"
                required
              >
            </span>
          </label>

          <div v-if="!isRegister" class="form-options">
            <label class="check-option">
              <input v-model="rememberMe" type="checkbox">
              <span>记住我</span>
            </label>
            <button class="text-button" type="button" @click="notice = '密码重置服务暂未开放，请联系管理员。'">
              忘记密码？
            </button>
          </div>

          <label v-else class="check-option terms-option">
            <input v-model="acceptedTerms" type="checkbox">
            <span>我已阅读并同意 <span class="terms-name">服务条款</span> 与 <span class="terms-name">隐私政策</span></span>
          </label>

          <p v-if="notice" class="form-notice" role="status">{{ notice }}</p>

          <button class="submit-button" type="submit">
            <span>{{ isRegister ? '创建账号' : '登录' }}</span>
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M5 12h14m-6-6 6 6-6 6" />
            </svg>
          </button>
        </form>

        <p class="switch-prompt">
          {{ isRegister ? '已经有账号了？' : '还没有账号？' }}
          <button type="button" @click="switchMode(!isRegister)">
            {{ isRegister ? '返回登录' : '立即注册' }}
          </button>
        </p>

        <div class="form-bottom">
          <span>安全 · 私密 · 专属于你</span>
          <RouterLink :to="{ name: 'home' }">返回首页 <span aria-hidden="true">↗</span></RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.auth-page {
  position: fixed;
  inset: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: minmax(390px, 0.92fr) minmax(480px, 1.08fr);
  width: 100vw;
  min-height: 100vh;
  overflow-y: auto;
  background: #fff;
  color: #242a39;
  font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
}

.welcome-panel {
  position: relative;
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  overflow: hidden;
  padding: 38px clamp(36px, 6vw, 88px) 28px;
  background:
    radial-gradient(ellipse at 75% 80%, rgb(166 137 221 / 27%), transparent 34%),
    radial-gradient(ellipse at 3% 35%, rgb(95 114 207 / 30%), transparent 45%),
    linear-gradient(145deg, #15192d 0%, #222644 52%, #2b2543 100%);
  color: #fff;
}

.welcome-panel::before,
.welcome-panel::after {
  position: absolute;
  width: 460px;
  height: 460px;
  border: 1px solid rgb(255 255 255 / 7%);
  border-radius: 50%;
  content: "";
  pointer-events: none;
}

.welcome-panel::before {
  right: -310px;
  bottom: -240px;
}

.welcome-panel::after {
  right: -360px;
  bottom: -290px;
}

.brand {
  position: relative;
  z-index: 1;
  display: inline-flex;
  width: fit-content;
  align-items: center;
  gap: 11px;
  color: #fff;
  font-size: 15px;
  font-weight: 650;
  letter-spacing: 0.06em;
  text-decoration: none;
}

.brand-mark {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  border: 1px solid rgb(255 255 255 / 25%);
  border-radius: 12px;
  background: linear-gradient(145deg, #9297ee, #766fd0);
  box-shadow: 0 6px 20px rgb(124 117 211 / 28%);
  color: #fff;
  font-size: 17px;
  font-weight: 600;
}

.welcome-copy {
  position: relative;
  z-index: 1;
  margin-top: clamp(72px, 12vh, 132px);
}

.eyebrow,
.form-kicker {
  color: #aaa9d3;
  font-size: 10px;
  font-weight: 650;
  letter-spacing: 0.18em;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 9px;
}

.eyebrow i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #a7e4c5;
  box-shadow: 0 0 12px rgb(167 228 197 / 70%);
}

.welcome-copy h1 {
  margin: 22px 0 18px;
  font-size: clamp(34px, 4vw, 52px);
  font-weight: 560;
  letter-spacing: -0.045em;
  line-height: 1.4;
}

.welcome-copy h1 span {
  color: #c4b8fa;
}

.welcome-copy p {
  margin: 0;
  color: #b6b8ce;
  font-size: 14px;
  line-height: 2;
}

.orbit-art {
  position: absolute;
  right: clamp(34px, 7vw, 92px);
  bottom: clamp(94px, 16vh, 164px);
  display: grid;
  width: 260px;
  height: 220px;
  place-items: center;
  opacity: 0.95;
}

.orbit {
  position: absolute;
  border: 1px solid rgb(207 200 255 / 25%);
  border-radius: 50%;
  transform: rotate(-28deg);
}

.orbit-one {
  width: 230px;
  height: 88px;
}

.orbit-two {
  width: 182px;
  height: 154px;
  transform: rotate(38deg);
}

.orbit-three {
  width: 250px;
  height: 190px;
  border-color: rgb(207 200 255 / 12%);
  transform: rotate(-58deg);
}

.orbit-center,
.orbit-node {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid rgb(255 255 255 / 20%);
  border-radius: 50%;
  backdrop-filter: blur(8px);
}

.orbit-center {
  width: 66px;
  height: 66px;
  background: linear-gradient(145deg, #9f9af0, #756cbf);
  box-shadow: 0 0 40px rgb(156 144 255 / 35%);
  font-size: 25px;
}

.orbit-node {
  width: 38px;
  height: 38px;
  background: rgb(255 255 255 / 11%);
  color: #ded8ff;
  font-size: 14px;
}

.node-one {
  top: 17px;
  left: 41px;
}

.node-two {
  top: 57px;
  right: 12px;
}

.node-three {
  bottom: 12px;
  left: 94px;
}

.node-four {
  top: 12px;
  right: 61px;
  color: #e8c99a;
  font-size: 20px;
}

.welcome-footer {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  color: #9296b1;
  font-size: 11px;
  letter-spacing: 0.06em;
}

.form-panel {
  display: grid;
  min-width: 0;
  place-items: center;
  padding: 54px 40px 30px;
}

.form-wrap {
  width: min(100%, 400px);
}

.mobile-brand {
  display: none;
}

.form-heading {
  margin-bottom: 28px;
}

.form-kicker {
  color: #9092b7;
  font-size: 9px;
}

.form-heading h2 {
  margin: 12px 0 7px;
  color: #292d3d;
  font-size: 30px;
  font-weight: 650;
  letter-spacing: -0.04em;
  line-height: 1.3;
}

.form-heading p {
  margin: 0;
  color: #8d91a0;
  font-size: 13px;
  line-height: 1.7;
}

.mode-switch {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin-bottom: 24px;
  padding: 4px;
  border: 1px solid #eeeff4;
  border-radius: 11px;
  background: #f7f8fa;
}

.mode-switch button {
  min-height: 36px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: #8a8e9c;
  font: inherit;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.18s ease, box-shadow 0.18s ease, color 0.18s ease;
}

.mode-switch button.active {
  background: #fff;
  box-shadow: 0 1px 5px rgb(35 39 61 / 9%);
  color: #454166;
  font-weight: 600;
}

.auth-form {
  display: grid;
  gap: 17px;
}

.field {
  display: grid;
  gap: 8px;
  color: #515566;
  font-size: 12px;
  font-weight: 560;
}

.input-wrap {
  display: flex;
  min-height: 47px;
  align-items: center;
  gap: 10px;
  padding: 0 13px;
  border: 1px solid #e8e9ef;
  border-radius: 10px;
  background: #fff;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.input-wrap:focus-within {
  border-color: #9c91d7;
  box-shadow: 0 0 0 3px rgb(156 145 215 / 13%);
}

.input-wrap > svg,
.password-toggle svg {
  width: 17px;
  height: 17px;
  flex: 0 0 auto;
  fill: none;
  stroke: #a0a2af;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.6;
}

.input-wrap input {
  width: 100%;
  min-width: 0;
  height: 44px;
  padding: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: #303445;
  font: inherit;
  font-size: 12px;
}

.input-wrap input::placeholder {
  color: #b9bbc5;
}

.password-toggle {
  display: grid;
  width: 28px;
  height: 32px;
  flex: 0 0 auto;
  place-items: center;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.password-toggle:hover svg {
  stroke: #6d6799;
}

.field-hint {
  color: #a5a7b2;
  font-size: 10px;
  font-weight: 400;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: -1px;
}

.check-option {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #777b89;
  font-size: 11px;
  font-weight: 400;
  cursor: pointer;
}

.check-option input {
  width: 14px;
  height: 14px;
  margin: 0;
  accent-color: #7772be;
  cursor: pointer;
}

.text-button,
.switch-prompt button {
  padding: 0;
  border: 0;
  background: transparent;
  color: #716bb0;
  font: inherit;
  font-size: 11px;
  cursor: pointer;
}

.text-button:hover,
.switch-prompt button:hover {
  color: #514993;
}

.terms-option {
  align-items: flex-start;
  line-height: 1.7;
}

.terms-option input {
  flex: 0 0 auto;
  margin-top: 2px;
}

.terms-name {
  color: #716bb0;
  font-weight: 550;
}

.form-notice {
  margin: -3px 0 0;
  padding: 9px 11px;
  border: 1px solid #ece8f7;
  border-radius: 8px;
  background: #f8f6fc;
  color: #6b6193;
  font-size: 11px;
  line-height: 1.6;
}

.submit-button {
  display: flex;
  min-height: 47px;
  align-items: center;
  justify-content: center;
  gap: 11px;
  margin-top: 2px;
  border: 0;
  border-radius: 10px;
  background: linear-gradient(100deg, #686db2, #8274bf);
  box-shadow: 0 7px 16px rgb(112 106 177 / 20%);
  color: #fff;
  font: inherit;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: box-shadow 0.18s ease, transform 0.18s ease;
}

.submit-button:hover {
  box-shadow: 0 9px 20px rgb(112 106 177 / 28%);
  transform: translateY(-1px);
}

.submit-button svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.7;
}

.switch-prompt {
  margin: 20px 0 0;
  color: #9295a2;
  font-size: 11px;
  text-align: center;
}

.switch-prompt button {
  margin-left: 4px;
  font-weight: 600;
}

.form-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 56px;
  padding-top: 17px;
  border-top: 1px solid #f0f0f4;
  color: #aaacb7;
  font-size: 10px;
}

.form-bottom a {
  color: #777991;
  text-decoration: none;
}

.form-bottom a:hover {
  color: #615d9b;
}

.form-bottom a span {
  margin-left: 3px;
}

@media (max-width: 800px) {
  .auth-page {
    grid-template-columns: minmax(310px, 0.8fr) minmax(420px, 1.2fr);
  }

  .welcome-panel {
    padding-right: 32px;
    padding-left: 36px;
  }

  .orbit-art {
    right: 18px;
    transform: scale(0.82);
    transform-origin: right bottom;
  }

  .form-panel {
    padding-right: 30px;
    padding-left: 30px;
  }
}

@media (max-width: 640px) {
  .auth-page {
    display: block;
    min-height: 100svh;
    background:
      radial-gradient(ellipse at 100% 0%, rgb(180 168 232 / 17%), transparent 36%),
      #fff;
  }

  .welcome-panel {
    display: none;
  }

  .form-panel {
    min-height: 100svh;
    padding: 28px 24px 22px;
  }

  .form-wrap {
    width: min(100%, 400px);
  }

  .mobile-brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-bottom: clamp(38px, 9vh, 72px);
    color: #343148;
    font-size: 14px;
    font-weight: 650;
  }

  .mobile-brand .brand-mark {
    width: 33px;
    height: 33px;
    font-size: 15px;
  }

  .form-heading h2 {
    font-size: 27px;
  }

  .form-bottom {
    margin-top: 42px;
  }
}

@media (max-width: 360px) {
  .form-panel {
    padding-right: 18px;
    padding-left: 18px;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
