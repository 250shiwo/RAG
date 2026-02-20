# 用户注册/登录/JWT鉴权接口 Spec

## Why
当前后端缺少统一的用户注册、登录与鉴权验证接口，导致后续业务接口无法基于 token 进行访问控制与身份识别。

## What Changes
- 新增 3 个用户相关接口：
  - `POST /api/users/register`：创建用户
  - `POST /api/users/login`：返回 JWT token
  - `GET /api/users/me`：返回当前登录用户信息（用于验证鉴权）
- 引入并使用 DRF JWT（默认采用 `djangorestframework-simplejwt`）进行鉴权
- 统一 token 传递方式：`Authorization: Bearer <access_token>`

## Impact
- Affected specs: 用户身份体系、鉴权中间件/权限控制、后续需要登录态的业务接口
- Affected code: Django/DRF 配置（settings/urls）、users 相关 app（serializer/view/permission）、全局认证配置

## ADDED Requirements

### Requirement: 用户注册
系统 SHALL 提供 `POST /api/users/register` 用于创建用户。

#### Request
- Content-Type: `application/json`
- Body（最小集合）：
  - `username`: string（必填）
  - `password`: string（必填）
- Body（可选）：
  - `email`: string（可选，若项目已有要求则按现有校验）

#### Response
- **201**：创建成功，返回用户信息（不包含明文密码）
  - `id`: number|string
  - `username`: string
  - `email`: string|null（若存在）
- **400**：参数校验失败（如用户名已存在、密码不符合规则等）

#### Scenario: Success case
- **WHEN** 客户端提交合法的 `username` 与 `password`
- **THEN** 服务器创建用户并返回 201 与用户信息

#### Scenario: Username already exists
- **WHEN** 客户端提交已存在的 `username`
- **THEN** 服务器返回 400，包含可读的错误信息

### Requirement: 用户登录（签发 JWT）
系统 SHALL 提供 `POST /api/users/login` 用于校验用户名密码并返回 JWT token。

#### Request
- Content-Type: `application/json`
- Body：
  - `username`: string（必填）
  - `password`: string（必填）

#### Response
- **200**：登录成功，返回 token
  - `access`: string（JWT access token）
  - `refresh`: string（JWT refresh token，若项目决定不返回则需在实现阶段说明并同步调整 spec）
- **401**：用户名或密码错误
- **400**：缺少字段或字段类型不正确

#### Scenario: Success case
- **WHEN** 客户端提交正确的用户名与密码
- **THEN** 服务器返回 200，包含 `access`（以及 `refresh`）

#### Scenario: Invalid credentials
- **WHEN** 客户端提交错误的用户名或密码
- **THEN** 服务器返回 401

### Requirement: 获取当前用户信息（鉴权验证）
系统 SHALL 提供 `GET /api/users/me` 用于验证鉴权是否正常，并返回当前登录用户信息。

#### Auth
- 必须携带 Header：`Authorization: Bearer <access>`

#### Response
- **200**：返回当前用户信息
  - `id`: number|string
  - `username`: string
  - `email`: string|null
- **401**：未携带 token、token 无效或过期

#### Scenario: Success case
- **WHEN** 客户端携带有效 `access` 访问 `/api/users/me`
- **THEN** 服务器返回 200 与当前用户信息

#### Scenario: Missing token
- **WHEN** 客户端未携带 `Authorization` 访问 `/api/users/me`
- **THEN** 服务器返回 401

## MODIFIED Requirements
### Requirement: 后续接口可带 token 访问
系统 SHALL 支持后续受保护接口通过 `Authorization: Bearer <access>` 访问，并能在请求上下文中识别当前用户。

## REMOVED Requirements
无
