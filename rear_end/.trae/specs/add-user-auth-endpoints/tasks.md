# Tasks
- [x] Task 1: 接入 DRF JWT 鉴权配置
  - [x] 安装并配置 simplejwt（认证类、token 参数、过期策略）
  - [x] 配置全局 DRF Authentication/Permission 默认值
  - [x] 确认 `Authorization: Bearer <access>` 生效

- [x] Task 2: 实现注册接口 `POST /api/users/register`
  - [x] 实现注册 serializer（字段校验、密码 hash 存储）
  - [x] 实现 view（创建用户并返回安全的用户信息）
  - [x] 挂载路由到 `/api/users/register`

- [x] Task 3: 实现登录接口 `POST /api/users/login`
  - [x] 实现登录逻辑（用户名密码校验）
  - [x] 生成并返回 JWT token（access/refresh）
  - [x] 挂载路由到 `/api/users/login`

- [x] Task 4: 实现当前用户接口 `GET /api/users/me`
  - [x] 实现鉴权保护（必须登录）
  - [x] 返回当前用户信息（与注册返回结构一致）
  - [x] 挂载路由到 `/api/users/me`

- [x] Task 5: 添加接口验证用测试用例
  - [x] 注册成功/重复用户名失败
  - [x] 登录成功/凭证错误失败
  - [x] me：带 token 成功/不带 token 失败

# Task Dependencies
- Task 2, Task 3, Task 4 依赖 Task 1
- Task 5 依赖 Task 2, Task 3, Task 4
