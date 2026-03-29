# 管理员后台接口 + 问答耗时/Token 统计 Spec

## Why
当前用户侧的 API 与页面已完成，但缺少管理员侧用于管理用户、知识库、文档的后台接口；同时问答接口需要返回耗时与 token 消耗以便前端展示与运维观测。

## What Changes
- 新增管理员接口（仅后台）：`/api/admin/*`，支持管理用户、知识库、文档
- 新增管理员鉴权规则：管理员接口需要登录（JWT Bearer）且具备管理员权限
- 修改问答接口：`POST /api/rag/chat` 响应中追加耗时与 token 使用量字段
- 增加/完善对应的 API 文档与自动化测试

## Impact
- Affected specs: 管理员权限、用户/知识库/文档管理、问答统计
- Affected code: DRF views/serializers/urls；users/knowledge/rag 模块；API.md；测试用例

## ADDED Requirements

### Requirement: 管理员接口鉴权与权限
系统 SHALL 对所有 `/api/admin/*` 接口强制执行如下约束：
- 认证：需要登录（JWT Bearer）
- 授权：仅管理员可访问（建议以 Django `is_staff` 或 `is_superuser` 判定）

#### Scenario: Unauthorized
- **WHEN** 未登录访问 `/api/admin/*`
- **THEN** 返回 401

#### Scenario: Forbidden
- **WHEN** 已登录但非管理员访问 `/api/admin/*`
- **THEN** 返回 403

---

### Requirement: 管理员用户管理接口
系统 SHALL 提供用户管理接口，用于管理员对用户进行查询、创建、更新、删除。

#### 1) 获取用户列表
- 方法与路径：`GET /api/admin/users`
- 认证与授权：需要管理员
- Query（可选）：
  - `q`：按 username/email 模糊搜索
  - `is_active`：`true/false` 过滤
- Response（200）：
  - `items`：数组，元素字段：
    - `id`、`username`、`email`、`is_active`、`is_staff`、`date_joined`

#### 2) 创建用户
- 方法与路径：`POST /api/admin/users`
- Body（JSON）：
  - `username`（必填）
  - `password`（必填）
  - `email`（可选）
  - `is_active`（可选，默认 true）
  - `is_staff`（可选，默认 false）
- Response（201）：返回创建后的用户对象（不包含密码）

#### 3) 更新用户
- 方法与路径：`PATCH /api/admin/users/{id}`
- Body（JSON，至少一项）：
  - `username`、`email`、`is_active`、`is_staff`（可选）
  - `password`（可选；若提供则重置密码）
- Response（200）：返回更新后的用户对象（不包含密码）

#### 4) 删除用户
- 方法与路径：`DELETE /api/admin/users/{id}`
- Response：`204 No Content`

#### Scenario: Not found
- **WHEN** 管理员更新/删除的用户不存在
- **THEN** 返回 404

---

### Requirement: 管理员知识库管理接口
系统 SHALL 提供知识库管理接口，用于管理员对知识库进行查询、创建、更新、删除与查看其文档列表。

#### 1) 获取知识库列表
- 方法与路径：`GET /api/admin/kb`
- Query（可选）：
  - `user_id`：仅返回指定用户的知识库
- Response（200）：
  - `items`：数组，元素字段：
    - `id`、`user_id`、`name`、`description`、`faiss_path`、`created_at`

#### 2) 创建知识库（指定归属用户）
- 方法与路径：`POST /api/admin/kb`
- Body（JSON）：
  - `user_id`（必填）
  - `name`（必填）
  - `description`（可选）
- Response（201）：返回创建后的知识库对象
- 约束：创建成功后应创建对应的空索引文件（与用户侧创建知识库一致）

#### 3) 更新知识库
- 方法与路径：`PATCH /api/admin/kb/{id}`
- Body（JSON，至少一项）：
  - `name`、`description`
- Response（200）：返回更新后的知识库对象

#### 4) 删除知识库
- 方法与路径：`DELETE /api/admin/kb/{id}`
- Response：`204 No Content`
- 约束：删除后应删除索引文件；其下 Document/Chunk 数据应随外键级联清理（数据库层）

#### 5) 获取知识库文档列表
- 方法与路径：`GET /api/admin/kb/{id}/documents`
- Response（200）：
  - `items`：数组，元素字段：
    - `id`、`filename`、`chunk_count`、`uploaded_at`

#### Scenario: Not found
- **WHEN** 管理员查询/更新/删除的知识库不存在
- **THEN** 返回 404

---

### Requirement: 管理员文档管理接口
系统 SHALL 提供文档管理接口，用于管理员删除文档并保持索引与数据库一致。

#### 删除文档（重建索引）
- 方法与路径：`DELETE /api/admin/document/{id}`
- Response：`204 No Content`
- 约束：
  - 删除 Document/Chunk 记录并删除原文件（若存在）
  - 通过“重建索引”保证 FAISS 与数据库一致（与用户侧删除文档一致的策略）

#### Scenario: Not found
- **WHEN** 管理员删除的文档不存在
- **THEN** 返回 404

## MODIFIED Requirements

### Requirement: 问答接口响应追加耗时与 Token 用量
系统 SHALL 修改 `POST /api/rag/chat` 的 200 响应，在原有 `answer` 基础上追加以下字段：
- `elapsed_ms`：整数，总耗时（毫秒），覆盖“检索 + 生成 + 业务处理”的总时间
- `token_usage`：对象，包含：
  - `prompt_tokens`：整数或 null
  - `completion_tokens`：整数或 null
  - `total_tokens`：整数或 null

#### Response（200）
```json
{
  "answer": "自然语言回答文本",
  "elapsed_ms": 1234,
  "token_usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }
}
```

#### 约束
- 若底层模型提供 token usage，系统 SHOULD 尽可能返回准确值
- 若无法获取 token usage，系统 SHALL 返回 `token_usage` 字段但其子字段为 `null`（避免前端字段缺失导致兼容性问题）

#### Scenario: Success case
- **WHEN** 用户已登录并提交 `kb_id` 与 `question`
- **AND** `kb_id` 归属于当前用户
- **THEN** 返回 200，包含 `answer`、`elapsed_ms`、`token_usage`

## REMOVED Requirements
无。

