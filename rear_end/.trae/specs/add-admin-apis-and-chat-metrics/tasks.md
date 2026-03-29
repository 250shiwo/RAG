# Tasks
- [x] Task 1: 新增管理员接口路由与权限保护
  - [x] SubTask 1.1: 定义管理员权限判定（is_staff/is_superuser）
  - [x] SubTask 1.2: 建立 /api/admin 路由入口并接入总路由

- [x] Task 2: 实现管理员用户管理接口
  - [x] SubTask 2.1: 实现 GET /api/admin/users（支持 q、is_active 过滤）
  - [x] SubTask 2.2: 实现 POST /api/admin/users（创建用户）
  - [x] SubTask 2.3: 实现 PATCH /api/admin/users/{id}（更新资料/重置密码）
  - [x] SubTask 2.4: 实现 DELETE /api/admin/users/{id}（删除用户）

- [x] Task 3: 实现管理员知识库管理接口
  - [x] SubTask 3.1: 实现 GET /api/admin/kb（支持 user_id 过滤）
  - [x] SubTask 3.2: 实现 POST /api/admin/kb（指定 user_id 创建知识库并创建空索引）
  - [x] SubTask 3.3: 实现 PATCH /api/admin/kb/{id}（更新 name/description）
  - [x] SubTask 3.4: 实现 DELETE /api/admin/kb/{id}（删除知识库并删除索引文件）
  - [x] SubTask 3.5: 实现 GET /api/admin/kb/{id}/documents（列出文档）

- [x] Task 4: 实现管理员文档删除接口
  - [x] SubTask 4.1: 实现 DELETE /api/admin/document/{id}（删除文件/记录并重建索引）

- [x] Task 5: 问答接口返回耗时与 Token 消耗
  - [x] SubTask 5.1: 在 rag_chat 流程采集总耗时并返回 elapsed_ms
  - [x] SubTask 5.2: 从模型响应中提取 token usage；无法获取则返回 null
  - [x] SubTask 5.3: 更新 /api/rag/chat 响应结构并保持错误码行为不变

- [x] Task 6: 文档与测试
  - [x] SubTask 6.1: 更新 API.md（新增 /api/admin/* 与 /api/rag/chat 新字段）
  - [x] SubTask 6.2: 增加/更新测试用例覆盖管理员权限与核心接口返回

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 depends on Task 3
- Task 5 depends on Task 1
- Task 6 depends on Task 2, Task 3, Task 4, Task 5
