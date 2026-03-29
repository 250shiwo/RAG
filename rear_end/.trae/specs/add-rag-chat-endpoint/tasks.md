# Tasks
- [x] Task 1: 设计并实现 `POST /api/rag/chat` 的请求/响应序列化
  - [x] 定义入参校验（kb_id、question）
  - [x] 定义出参结构（answer）

- [x] Task 2: 实现 RAG 问答服务层流程
  - [x] 加载指定 kb 的 FAISS 索引
  - [x] 对 question 计算 embedding 并做相似度检索
  - [x] 拉取 TopK 文本块并拼接 prompt（含截断策略）
  - [x] 调用模型生成回答并返回

- [x] Task 3: 挂载接口路由与权限校验
  - [x] 增加 view（鉴权 + kb 归属校验）
  - [x] 挂载路由 `/api/rag/chat`
  - [x] 统一错误码与错误响应格式（输入错误/未授权/不存在/索引异常）

- [x] Task 4: 添加自动化测试与基础验证
  - [x] 未登录访问返回 401
  - [x] 非法参数返回 400
  - [x] 访问他人 kb 返回 404/403（与项目一致）
  - [x] 正常流程能返回非空 answer（可使用 mock LLM 与固定检索结果）

# Task Dependencies
- Task 3 依赖 Task 1 与 Task 2
- Task 4 依赖 Task 3
