// eslint.config.js
import js from "@eslint/js";

export default jseslint.config( // 如果用 TS，用 tseslint.config 包裹
  js.configs.recommended,
  {
    // 全局忽略（替代原来的 .eslintignore）
    ignores: ["**/dist/", "**/node_modules/"],
  },
  {
    // 在这里迁移你原来的自定义规则
    rules: {
      // "no-console": "warn",
    },
  },
);