# Tasks
- [x] Task 1: 建立文档入库的数据模型
  - [x] 为 Document 增加保存文件路径字段（或新增独立表记录文件路径）
  - [x] 新增文档分块表（用于重建索引：document 外键 + chunk_text + chunk_index）
  - [x] 完成迁移并可在测试库中创建/查询

- [x] Task 2: 接入 LangChain + OpenAI Embeddings + FAISS
  - [x] 增加依赖（langchain、openai、faiss-cpu 等，按平台可用性选择）
  - [x] 增加配置项（embedding 模型、base_url、API key 环境变量约束）
  - [x] 封装“加载/保存 FAISS、写入向量、重建索引”的服务层函数

- [x] Task 3: 实现上传入库接口 `POST /api/kb/upload`
  - [x] 保存上传文件到磁盘（目录可配置）
  - [x] 文本提取与分块（最小支持 txt；其它类型按依赖扩展）
  - [x] 写入 Document 与分块表
  - [x] embedding 并写入 FAISS，保存到 KnowledgeBase.faiss_path
  - [x] 挂载路由并加鉴权与归属校验

- [x] Task 4: 实现文档列表接口 `GET /api/kb/{id}/documents`
  - [x] 返回指定 kb 的 Document 列表（仅当前用户）
  - [x] 挂载路由并加鉴权与归属校验

- [x] Task 5: 实现删除文档接口 `DELETE /api/document/{id}`
  - [x] 删除 Document 与分块记录，并删除原文件（容错）
  - [x] 重建该 kb 的 FAISS 索引并保存
  - [x] 挂载路由并加鉴权与归属校验

- [x] Task 6: 添加测试用例
  - [x] 未登录访问 upload/documents/delete 返回 401
  - [x] 上传：Document 记录生成且 chunk_count 正确，FAISS 向量数增加
  - [x] 文档列表：仅返回该 kb 的文档（且仅当前用户）
  - [x] 删除文档：删除 DB 记录并触发重建索引（向量数减少或重建结果一致）

- [x] Task 7: 支持上传同名文件的前端策略
  - [x] 上传参数新增 `on_conflict`（keep/replace）
  - [x] keep：自动生成随机文件名并保留旧文档
  - [x] replace：删除旧文档并替换为新文档，索引与数据库一致
  - [x] 补充测试覆盖 keep/replace 两条分支

# Task Dependencies
- Task 3-5 依赖 Task 1 与 Task 2
- Task 6 依赖 Task 3-5
- Task 7 依赖 Task 3
