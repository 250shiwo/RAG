# 问答接口（RAG Chat）Spec

## Why
阶段四需要提供一个最小可用的问答接口，用于基于指定知识库进行相似度检索并返回自然语言回答。

## What Changes
- 新增接口：`POST /api/rag/chat`
- 新增问答服务流程：加载索引 → embedding 问题 → 相似度检索 → 取文本块 → 拼接 prompt → 调用模型 → 返回回答
- 新增/复用配置：LLM 模型、base_url、API key、检索 top_k、最大上下文块数等
- 增加鉴权与资源归属校验（仅允许访问当前用户的 kb）

## Impact
- Affected specs: 问答模块、索引加载与检索、模型调用
- Affected code: DRF views/serializers/urls；索引（FAISS）加载服务；LLM 调用封装；测试用例

## ADDED Requirements

### Requirement: 问答接口
系统 SHALL 提供 `POST /api/rag/chat` 接口，基于 `kb_id` 指定知识库完成检索增强生成并返回自然语言回答。

#### Request
- 方法与路径：`POST /api/rag/chat`
- 认证：需要登录（JWT Bearer）
- Body（JSON）：
  - `kb_id`：知识库 ID（必填）
  - `question`：用户问题（必填，非空字符串）

#### Response（200）
- `answer`：自然语言回答（非空字符串）

#### Scenario: Success case
- **WHEN** 用户已登录，并提交 `kb_id` 与 `question`
- **AND** `kb_id` 归属于当前用户
- **THEN** 系统加载该 kb 的向量索引
- **AND** 对 `question` 进行 embedding
- **AND** 进行相似度检索并取回 TopK 文本块
- **AND** 将文本块与问题拼接为 prompt
- **AND** 调用模型生成回答
- **AND** 返回 200，且 `answer` 为自然语言文本

#### Scenario: Invalid input
- **WHEN** `kb_id` 缺失/非法 或 `question` 为空
- **THEN** 返回 400

#### Scenario: Unauthorized
- **WHEN** 未登录访问
- **THEN** 返回 401

#### Scenario: Forbidden / Not found
- **WHEN** `kb_id` 不存在或不属于当前用户
- **THEN** 返回 404（或 403，但需在项目内保持一致）

#### Scenario: Index missing/unloadable
- **WHEN** kb 对应索引文件不存在或无法加载
- **THEN** 返回 400 或 500（需在实现中定义一致的错误码与错误信息）

### Requirement: 检索流程（RAG）
系统 SHALL 按如下顺序执行问答流程：
1. 加载指定 kb 的索引（FAISS）
2. 计算问题 embedding
3. 基于向量相似度检索 TopK
4. 取回对应文本块并按相关度排序
5. 将文本块拼接到 prompt（包含指令与用户问题）
6. 调用模型生成回答
7. 返回自然语言回答

### Requirement: 安全与可维护性
系统 SHALL 满足以下约束：
- 不在日志中打印 API key、token 等敏感信息
- prompt 组装应对极端长文本做截断/限额（避免超出模型上下文）
- 索引加载失败应返回稳定、可诊断的错误响应（不暴露敏感路径）

## MODIFIED Requirements
无。

## REMOVED Requirements
无。

