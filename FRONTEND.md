# 前端页面文档

本文档描述了 RAG 智能助手前端系统的页面结构、路由配置及与其对应的后端 API 的关联。

## 页面层级与路由

前端基于 Vue 3 + Vue Router 构建，主要分为两类页面：
1. **公开页面**：不需要登录即可访问的页面（登录、注册）
2. **鉴权页面**：需要携带有效 JWT Token 才能访问的页面（知识库管理、问答等）

---

### 1. 登录与注册模块

#### 1.1 登录页 (`/login`)
- **组件位置**：`src/views/LoginView.vue`
- **功能描述**：用户输入用户名和密码获取 Access/Refresh Token，并将 Token 存储在本地，成功后跳转至首页。
- **关联 API**：
  - `POST /api/users/login`：用户登录

#### 1.2 注册页 (`/register`)
- **组件位置**：`src/views/RegisterView.vue`
- **功能描述**：新用户注册，提供用户名、密码和可选的邮箱，成功后引导用户前往登录。
- **关联 API**：
  - `POST /api/users/register`：用户注册

---

### 2. 用户控制台模块（主应用区）

该区域采用经典侧边栏布局，包含左侧导航菜单（`App.vue` 提供结构）和右侧内容展示区。

#### 2.1 知识库列表页 (`/kb`)
- **组件位置**：`src/views/KbListView.vue`
- **功能描述**：展示当前用户创建的所有知识库。用户可以新建知识库、删除知识库，以及快速进入对应知识库的文档管理或问答界面。
- **关联 API**：
  - `GET /api/kb/list`：获取我的知识库列表
  - `POST /api/kb/create`：创建知识库
  - `DELETE /api/kb/{id}`：删除知识库

#### 2.2 文档管理页 (`/kb/:kbId/documents`)
- **组件位置**：`src/views/KbDocumentsView.vue`
- **功能描述**：管理特定知识库下的文档。支持拖拽上传（txt/md/pdf），并可配置重名策略（保留或覆盖）。显示当前文档列表及其切分块数。
- **关联 API**：
  - `GET /api/kb/{id}/documents`：获取知识库文档列表
  - `POST /api/kb/upload`：上传文档入库
  - `DELETE /api/document/{id}`：删除单个文档

#### 2.3 智能问答页 (`/kb/:kbId/chat`)
- **组件位置**：`src/views/ChatView.vue`
- **功能描述**：现代化的对话式交互界面。用户向指定知识库提问，系统检索资料后生成回答。**新版界面会在 AI 回复下方展示此次回答的消耗时间（耗时）及模型 Token 消耗量**。
- **关联 API**：
  - `POST /api/rag/chat`：非流式问答接口（返回包含 `elapsed_ms` 和 `token_usage` 的完整 JSON）
  - `POST /api/rag/chat/stream`：流式问答接口（旧版或支持流式的回退方案）

---

### 3. 管理员专区

管理员专区面向具有 `is_staff=True` 权限的用户开放，用于全局管理平台上的所有用户及知识库。

#### 3.1 全局用户管理 (`/admin/users`)
- **组件位置**：`src/views/admin/AdminUsersView.vue`
- **功能描述**：展示系统内所有注册用户，支持按用户名或邮箱搜索。管理员可在此页面新建用户、重置用户密码、修改用户状态（启用/禁用）及赋予管理员权限。
- **关联 API**：
  - `GET /api/admin/users`：获取用户列表
  - `POST /api/admin/users`：创建用户
  - `PATCH /api/admin/users/{id}`：更新用户（包含重置密码）
  - `DELETE /api/admin/users/{id}`：删除用户

#### 3.2 全局知识库管理 (`/admin/kbs`)
- **组件位置**：`src/views/admin/AdminKbsView.vue`
- **功能描述**：管理系统中所有用户创建的知识库。可按 `user_id` 过滤。支持直接为特定用户创建知识库、修改知识库信息、删除违规知识库，并能深入管理某知识库下的具体文档。
- **关联 API**：
  - `GET /api/admin/kb`：获取全部知识库列表
  - `POST /api/admin/kb`：创建知识库（需指定 user_id）
  - `PATCH /api/admin/kb/{id}`：更新知识库
  - `DELETE /api/admin/kb/{id}`：删除知识库
  - `GET /api/admin/kb/{id}/documents`：获取知识库文档列表
  - `DELETE /api/admin/document/{id}`：删除特定文档

---

## 核心服务逻辑

### HTTP 请求拦截与鉴权 (`src/services/api.js`)
- 使用 Axios 拦截器，自动在所有请求头中注入 `Authorization: Bearer <access_token>`。
- 监听 `401 Unauthorized` 状态码：
  - 触发无感刷新（调用 `/api/users/refresh` 获取新 Access Token 并重发失败请求）。
  - 若 Refresh Token 也已失效，则强制清除本地 Token，并重定向用户至登录页。

### 路由守卫 (`src/router/index.js`)
- 借助 Vue Router 的 `beforeEach` 钩子，判断 `meta.requiresAuth`：
  - 未登录用户尝试访问保护页面时，拦截并跳转到 `/login?redirect=...`
  - 已登录用户尝试访问 `/login` 时，直接跳转到首页 `/kb`。
