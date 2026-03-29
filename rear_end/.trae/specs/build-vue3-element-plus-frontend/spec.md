# 前端页面（Vue3 + Element Plus）Spec

## Why
当前后端 API 已具备用户鉴权、知识库管理、文档入库与问答能力，需要配套前端页面完成可用的交互闭环。

## What Changes
- 新增/完善前端工程（基于现有 `front_end/`）：引入 Vue Router、Element Plus、Axios（可选 Pinia）
- 新增鉴权与会话管理：登录/注册、token 持久化、自动附加 `Authorization: Bearer <access>`
- 新增页面与路由：
  - 登录 `/login`、注册 `/register`
  - 知识库列表/创建/删除 `/kb`
  - 文档管理（列表/上传/删除）`/kb/:kbId/documents`
  - 问答页面（RAG Chat）`/kb/:kbId/chat`
- 开发期联调：Vite devServer 代理 `/api` 到后端，避免 CORS 问题
- 文档更新：根据 `rear_end/API.md` 补齐前端功能入口与交互说明

## Impact
- Affected specs: 前端 UI、鉴权、知识库/文档/问答交互
- Affected code: `front_end/src/**`、`front_end/vite.config.js`、`front_end/package.json`

## ADDED Requirements

### Requirement: API 基础配置
系统 SHALL 支持配置后端 API Base URL：
- 开发模式：默认使用 Vite 代理（`/api` 转发到后端）
- 部署模式：支持通过 `VITE_API_BASE_URL` 指定完整后端地址

#### Scenario: Dev proxy
- **WHEN** 前端在本地开发模式运行
- **THEN** 前端请求 `/api/**` 由 Vite 代理到后端 `http://127.0.0.1:8000`

### Requirement: 用户注册与登录
系统 SHALL 提供注册与登录页面，并按 API 文档完成流程：
- 注册：`POST /api/users/register`
- 登录：`POST /api/users/login` 获取 `access/refresh`
- 获取当前用户：`GET /api/users/me`

#### Scenario: Login success
- **WHEN** 用户提交正确账号密码
- **THEN** 前端保存 `access/refresh`（持久化到 localStorage 或同等机制）
- **AND** 后续请求自动附带 `Authorization: Bearer <access>`
- **AND** 导航到知识库页面

#### Scenario: Auth required
- **WHEN** 用户访问需要登录的页面但未登录/Token 失效
- **THEN** 跳转到登录页，并提示需要登录

#### Scenario: Refresh access（可选增强）
- **WHEN** 请求返回 401 且存在 refresh token
- **THEN** 前端调用 `POST /api/users/refresh` 换取新的 access 并重试一次原请求

### Requirement: 知识库管理
系统 SHALL 提供知识库管理页面，实现：
- 创建知识库：`POST /api/kb/create`
- 获取知识库列表：`GET /api/kb/list`
- 删除知识库：`DELETE /api/kb/{id}`

#### Scenario: KB list
- **WHEN** 用户进入知识库页面
- **THEN** 展示当前用户的知识库列表（名称、描述、创建时间）

### Requirement: 文档入库与管理
系统 SHALL 提供文档管理页面，实现：
- 上传文档入库：`POST /api/kb/upload`（支持 `on_conflict=keep/replace`）
- 获取文档列表：`GET /api/kb/{id}/documents`
- 删除文档：`DELETE /api/document/{id}`

#### Scenario: Upload success
- **WHEN** 用户选择某个知识库并上传 txt 文件
- **THEN** 前端展示入库结果（文件名、chunk_count、上传时间）

### Requirement: 问答（RAG Chat）
系统 SHALL 提供问答页面，实现：
- 发送问题：`POST /api/rag/chat`（`kb_id`、`question`）
- 展示回答：响应 `answer` 为自然语言文本

#### Scenario: Chat success
- **WHEN** 用户在指定 kb 的问答页面提交问题
- **THEN** 展示加载态
- **AND** 返回后展示自然语言回答文本

### Requirement: UI 与交互约定
系统 SHALL 满足：
- 使用 Element Plus 组件构建表单、表格、弹窗、提示消息
- 全局错误提示：对 400/401/404/500 做可理解的提示（不展示敏感信息）
- 长操作反馈：上传/问答显示 loading 状态，防止重复提交

## MODIFIED Requirements
无。

## REMOVED Requirements
无。

