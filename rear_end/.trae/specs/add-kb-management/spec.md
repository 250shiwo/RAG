# 知识库管理（二期）Spec

## Why
需要提供知识库的基础管理能力，支持用户创建、查看自己的知识库列表、并删除知识库，同时确保索引文件在磁盘侧同步创建/清理。

## What Changes
- 新增 3 个知识库管理接口（均要求已登录）：
  - `POST /api/kb/create`：创建 KnowledgeBase，生成 `faiss_path` 并创建空索引文件
  - `GET /api/kb/list`：返回当前用户的知识库列表
  - `DELETE /api/kb/{id}`：删除知识库（数据库记录 + 对应索引文件）
- 新增索引文件存储根目录配置（默认落地到项目目录下的本地路径）
- 为上述接口补充自动化测试，覆盖鉴权与资源归属校验

## Impact
- Affected specs: 知识库生命周期管理、文件系统资源管理、鉴权/用户隔离
- Affected code: `knowledge` app（urls/views/serializers/tests）、settings（索引根目录配置）、模型写入逻辑（`KnowledgeBase.faiss_path`）

## ADDED Requirements

### Requirement: 创建知识库
系统 SHALL 提供 `POST /api/kb/create` 用于创建 KnowledgeBase，并在磁盘创建空索引文件。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Request
- Content-Type: `application/json`
- Body：
  - `name`: string（必填，长度 <= 100）
  - `description`: string（可选）

#### File Rules
- 系统 SHALL 为每个新知识库生成 `faiss_path` 并写入数据库。
- 系统 SHALL 在磁盘创建一个“空索引文件”，其路径与 `faiss_path` 一致。
- 索引根目录 SHALL 可配置（例如 `FAISS_INDEX_ROOT`）；若未配置，默认使用 `BASE_DIR / "faiss_indexes"`。
- `faiss_path` SHALL 指向索引文件的绝对路径，文件名建议包含 `kb_id` 以保证唯一性（例如 `<root>/<user_id>/<kb_id>.index`）。

#### Response
- **201**：创建成功，返回知识库信息
  - `id`: number|string
  - `name`: string
  - `description`: string
  - `faiss_path`: string
  - `created_at`: string（ISO 8601）
- **400**：参数校验失败
- **401**：未登录或 token 无效/过期

#### Scenario: Success case
- **WHEN** 已登录用户提交合法的 `name`（可带 `description`）
- **THEN** 数据库生成 KnowledgeBase 记录，且磁盘生成对应索引文件，并返回 201

#### Scenario: Missing name
- **WHEN** 已登录用户未提交 `name`
- **THEN** 返回 400

### Requirement: 获取我的知识库列表
系统 SHALL 提供 `GET /api/kb/list` 返回当前用户的知识库列表，仅包含其自身资源。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Response
- **200**：返回列表
  - `items`: array of KnowledgeBase
    - `id/name/description/faiss_path/created_at`
- **401**：未登录或 token 无效/过期

#### Scenario: Success case
- **WHEN** 已登录用户访问 `/api/kb/list`
- **THEN** 返回仅属于该用户的知识库列表

### Requirement: 删除知识库
系统 SHALL 提供 `DELETE /api/kb/{id}` 删除知识库及其索引文件，并确保用户只能删除自己的知识库。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Behavior
- 若知识库不存在，SHALL 返回 **404**。
- 若知识库存在但不属于当前用户，SHALL 返回 **404**（推荐）或 **403**（可选），实现时保持一致即可。
- 删除成功后：
  - SHALL 删除数据库记录
  - SHALL 删除 `faiss_path` 指向的索引文件（若文件不存在，SHALL 忽略并继续完成删除）

#### Response
- **204**：删除成功（无 body）
- **401**：未登录或 token 无效/过期
- **404**：资源不存在（或不属于当前用户）

#### Scenario: Success case
- **WHEN** 已登录用户删除自己名下的知识库
- **THEN** 数据库记录被删除，且磁盘索引文件被删除，返回 204

## MODIFIED Requirements
无

## REMOVED Requirements
无
