FROM node:22

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package.json ./

# 安装 pnpm
RUN npm install -g pnpm@8.15.6

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制应用代码（排除 node_modules）
COPY . .

# 构建应用
RUN pnpm build

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["pnpm", "preview"]