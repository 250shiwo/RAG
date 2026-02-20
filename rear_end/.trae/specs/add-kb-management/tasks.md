# Tasks
- [x] Task 1: 知识库创建接口（含索引文件创建）
  - [x] 定义 create serializer（name/description 校验）
  - [x] 实现 create view：写入 KnowledgeBase、生成 faiss_path、创建空索引文件
  - [x] 挂载路由 `POST /api/kb/create`

- [x] Task 2: 知识库列表接口
  - [x] 实现 list view：仅返回 request.user 的 KnowledgeBase
  - [x] 挂载路由 `GET /api/kb/list`

- [x] Task 3: 知识库删除接口（含索引文件删除）
  - [x] 实现 delete view：校验归属、删除 DB 记录、删除 faiss_path 文件
  - [x] 挂载路由 `DELETE /api/kb/{id}`

- [x] Task 4: 配置与公共工具
  - [x] 增加 `FAISS_INDEX_ROOT` 配置（未配置时使用默认目录）
  - [x] 抽取索引路径生成/文件创建删除的公共函数（便于测试与复用）

- [x] Task 5: 添加测试用例
  - [x] 鉴权：未登录访问 create/list/delete 返回 401
  - [x] 创建：数据库有记录且磁盘生成 index 文件
  - [x] 列表：仅返回当前用户的知识库
  - [x] 删除：删除 DB 记录并删除磁盘 index 文件（文件缺失时也能成功）

# Task Dependencies
- Task 2, Task 3 依赖 Task 1 的基础结构（serializers/permissions/urls）
- Task 5 依赖 Task 1-3
