# 文档入库（三期）Spec

## Why
知识库创建完成后需要支持“上传文档→向量化→写入 FAISS→前端可管理文档”的闭环，便于后续 RAG 检索与问答。

## What Changes
- 新增 3 个文档入库/管理接口（均要求已登录）：
  - `POST /api/kb/upload`：上传文件到指定知识库并入库（保存文件、提取文本、分块、embedding、写入 FAISS、记录 Document）
  - `GET /api/kb/{id}/documents`：获取知识库文档列表（用于前端展示）
  - `DELETE /api/document/{id}`：删除单个文档，并通过“重建索引”的方式同步更新 FAISS
- 新增对“文档分块内容”的持久化（用于重建索引），以支持删除文档后可重新构建向量库
- 引入 LangChain + OpenAI Embeddings（OpenAI API）进行向量化（实现阶段需要向你确认模型与 API Key）

## Impact
- Affected specs: 知识库入库流程、文件存储、向量化与索引管理、文档生命周期管理
- Affected code: `knowledge` app（models/serializers/views/urls/tests）、settings（上传目录/向量化配置）、新增 LangChain/FAISS/OpenAI 依赖

## ADDED Requirements

### Requirement: 上传文档入库
系统 SHALL 提供 `POST /api/kb/upload` 用于上传文档并写入指定知识库的 FAISS 索引。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Request
- Content-Type: `multipart/form-data`
- Form fields：
  - `kb_id`: number（必填）
  - `file`: file（必填）
  - `on_conflict`: string（可选）当同一知识库中出现同名文件时的处理策略：
    - `keep`：保留（自动生成随机文件名并入库）
    - `replace`：替换（删除旧文档并用新文档替换）

#### Pipeline
系统 SHALL 依次执行以下流程：
1) 保存文件（保留原文件名，落地到可配置的上传目录）
2) 文本提取（至少支持纯文本；其它类型如 PDF/DOCX 在实现阶段按依赖可用性决定）
3) 分块（chunking）
4) embedding（使用 LangChain 对接 OpenAI API）
5) 写入 FAISS（写入到该知识库的 `KnowledgeBase.faiss_path`）
6) 记录数据库：
   - 新增 `Document` 记录（kb、filename、chunk_count）
   - 新增文档分块记录（用于后续重建索引）

#### Index Rules
- 若 `KnowledgeBase.faiss_path` 对应索引尚不存在/不可加载，系统 SHALL 创建新索引并保存。
- 写入成功后，FAISS 中的向量数量 SHALL 增加（可通过测试用例侧验证）。

#### Conflict Rules（重名处理）
当 `Document(kb_id, filename)` 已存在时，系统 SHALL 根据 `on_conflict` 执行：
- `keep`：
  - SHALL 为本次上传生成随机文件名（保留扩展名），用于磁盘落地文件名与 Document.filename
  - SHALL 不影响已有同名文档
- `replace`：
  - SHALL 删除该 kb 下已有同名 Document 记录及其分块记录
  - SHOULD 删除旧文件（若文件不存在则忽略）
  - SHALL 将新文件作为该 filename 的替代版本入库
  - SHALL 保证最终索引与数据库一致（可通过重建索引或等价方式实现）

#### Response
- **201**：返回创建的 Document 信息（以及可选的入库统计）
  - `id`: number|string
  - `kb_id`: number|string
  - `filename`: string
  - `chunk_count`: number
  - `uploaded_at`: string（ISO 8601）
- **400**：参数/文件校验失败
- **401**：未登录或 token 无效/过期
- **404**：kb_id 不存在或不属于当前用户

#### Scenario: Success case
- **WHEN** 已登录用户上传文件并提供自己名下的 `kb_id`
- **THEN** 生成 Document 记录与分块记录，且 FAISS 向量数量增加，返回 201

### Requirement: 获取知识库文档列表
系统 SHALL 提供 `GET /api/kb/{id}/documents` 返回该知识库的文档列表，仅允许访问自己名下的知识库。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Response
- **200**：返回文档列表（按 uploaded_at 倒序）
  - `items`: array of Document
    - `id`
    - `filename`
    - `chunk_count`
    - `uploaded_at`
- **401**：未登录或 token 无效/过期
- **404**：知识库不存在或不属于当前用户

### Requirement: 删除单个文档（重建索引）
系统 SHALL 提供 `DELETE /api/document/{id}` 删除指定文档，并通过“重建索引”更新对应知识库的 FAISS。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Behavior
- 若 Document 不存在或不属于当前用户（通过其 kb 归属判断），SHALL 返回 **404**。
- 删除成功后：
  - SHALL 删除 Document 记录与其分块记录
  - SHOULD 删除已保存的原始文件（若文件不存在则忽略）
  - SHALL 重新构建该知识库的 FAISS 索引：以数据库中剩余分块为输入，重新 embedding 并保存到 `faiss_path`

#### Response
- **204**：删除成功（无 body）
- **401**：未登录或 token 无效/过期
- **404**：资源不存在（或不属于当前用户）

## MODIFIED Requirements
### Requirement: 上传文档入库（重名处理）
系统 SHALL 支持通过 `on_conflict` 控制同名文件上传策略：
- **WHEN** 同一 kb 中上传了同名文件且 `on_conflict=keep`
- **THEN** 自动生成随机文件名并创建新 Document，不删除旧 Document
- **WHEN** 同一 kb 中上传了同名文件且 `on_conflict=replace`
- **THEN** 删除旧 Document 并使新 Document 成为替代版本，且索引与数据库保持一致

## REMOVED Requirements
无

## Implementation Notes（实现阶段约束）
- 向量化必须使用 LangChain + OpenAI API。实现阶段 SHALL 向你确认：
  - 使用的 embedding 模型名称
  - OpenAI Base URL（若使用代理/兼容接口）
  - API Key 的获取方式
- API Key SHALL 仅通过环境变量/本地 `.env` 提供，不可写入代码仓库与日志。
