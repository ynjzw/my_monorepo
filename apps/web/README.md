# 项目名称

这是一个基于 Vue.js 和 Vite 的前端项目，旨在提供一个快速和现代的开发体验。

## 目录结构

```
web
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── nginx
│   └── default.conf
├── package.json
├── vite.config.js
├── .env
├── public
│   ├── typescript.svg
│   └── vite.svg
├── src
│   ├── main.ts
│   ├── App.vue
│   └── components
│       └── HelloWorld.vue
└── README.md
```

## 技术栈

- **Vue.js**: 用于构建用户界面的渐进式框架。
- **Vite**: 下一代前端工具，提供快速的开发和构建体验。
- **Docker**: 用于容器化应用，确保在不同环境中的一致性。

## 安装

1. 克隆项目：
   ```
   git clone <repository-url>
   cd web
   ```

2. 安装依赖：
   ```
   yarn install
   ```

## 使用

### 开发模式

在开发模式下启动应用：
```
yarn dev
```
应用将运行在 `http://localhost:5173`。

### 生产构建

构建生产版本：
```
yarn build
```

### Docker

使用 Docker 构建和运行应用：
1. 构建 Docker 镜像：
   ```
   docker build -t my-vue-app .
   ```

2. 运行 Docker 容器：
   ```
   docker run -p 8080:80 my-vue-app
   ```

应用将通过 `http://localhost:8080` 访问。

## 贡献

欢迎提交问题和拉取请求！请确保遵循项目的贡献指南。

## 许可证

该项目使用 MIT 许可证。有关详细信息，请参阅 LICENSE 文件。