# Tasks
- [x] Task 1: 初始化前端依赖与工程结构（Vue3 + Element Plus）
  - [x] 安装并接入 Element Plus、Vue Router、Axios（可选 Pinia）
  - [x] 配置 Vite `/api` 代理与环境变量 `VITE_API_BASE_URL`

- [x] Task 2: 封装 API Client 与鉴权会话
  - [x] 统一封装请求（baseURL、超时、错误处理）
  - [x] token 存储与注入 `Authorization: Bearer <access>`
  - [x] 401 处理：跳转登录（可选实现 refresh + 重试一次）

- [x] Task 3: 实现登录/注册页面与路由守卫
  - [x] 登录 `/login`（对接 `/api/users/login`）
  - [x] 注册 `/register`（对接 `/api/users/register`）
  - [x] 路由守卫：未登录禁止访问业务页面

- [x] Task 4: 实现知识库页面
  - [x] 知识库列表 `/kb`（对接 `/api/kb/list`）
  - [x] 创建知识库（对接 `/api/kb/create`）
  - [x] 删除知识库（对接 `/api/kb/{id}`）

- [x] Task 5: 实现文档管理页面
  - [x] 文档列表 `/kb/:kbId/documents`（对接 `/api/kb/{id}/documents`）
  - [x] 上传文档（对接 `/api/kb/upload`，支持 keep/replace）
  - [x] 删除文档（对接 `/api/document/{id}`）

- [x] Task 6: 实现问答页面（RAG Chat）
  - [x] 问答 `/kb/:kbId/chat`（对接 `/api/rag/chat`）
  - [x] 展示回答与加载态，保留基础对话历史（同页面会话内）

- [ ] Task 7: 验证与打包
  - [ ] 走通最小业务链路：登录 → 创建 kb → 上传文档 → 问答
  - [ ] `npm run build` 通过

# Task Dependencies
- Task 2 依赖 Task 1
- Task 3-6 依赖 Task 2
- Task 7 依赖 Task 3-6
