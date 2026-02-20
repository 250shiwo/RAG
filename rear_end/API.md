# 后端 API 文档

Base URL：`http://127.0.0.1:8000`

## 通用约定
- 请求体：除 `/admin/` 外，默认使用 JSON
- Content-Type：`application/json`
- JWT 鉴权 Header：`Authorization: Bearer <access>`
- Token 有效期：
  - `access`：60 分钟
  - `refresh`：7 天

## 1. 用户注册

**接口路径**：`POST /api/users/register`  
**是否鉴权**：否

### 请求头
- `Content-Type: application/json`

### 请求参数（JSON Body）
| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| username | string | 是 | 用户名（需唯一） |
| password | string | 是 | 密码（会按 Django 密码规则校验并 hash 存储） |
| email | string | 否 | 邮箱（允许空） |

### 返回格式
**201 Created**
```json
{
  "id": 1,
  "username": "u1",
  "email": ""
}
```

### 状态码
- `201`：创建成功
- `400`：参数校验失败（如用户名已存在、密码不符合规则等）

## 2. 用户登录（获取 access/refresh）

**接口路径**：`POST /api/users/login`  
**是否鉴权**：否

### 请求头
- `Content-Type: application/json`

### 请求参数（JSON Body）
| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

### 返回格式
**200 OK**
```json
{
  "refresh": "xxxx.yyyy.zzzz",
  "access": "aaaa.bbbb.cccc"
}
```

### 状态码
- `200`：登录成功
- `400`：缺少字段/字段格式不正确
- `401`：用户名或密码错误

## 3. 刷新 access（refresh 换新 access）

**接口路径**：`POST /api/users/refresh`  
**是否鉴权**：否（只依赖 refresh 参数）

### 请求头
- `Content-Type: application/json`

### 请求参数（JSON Body）
| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| refresh | string | 是 | 登录返回的 refresh token |

### 返回格式
**200 OK**
```json
{
  "access": "new_access_token"
}
```

### 状态码
- `200`：刷新成功
- `400`：缺少字段/字段格式不正确
- `401`：refresh 无效或过期（常见返回 `token_not_valid`）

## 4. 获取当前用户信息（验证鉴权）

**接口路径**：`GET /api/users/me`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Authorization: Bearer <access>`

### 请求参数
无

### 返回格式
**200 OK**
```json
{
  "id": 1,
  "username": "u1",
  "email": ""
}
```

### 状态码
- `200`：成功
- `401`：未携带 token / token 无效 / token 过期

## 5. Django 管理后台

**接口路径**：`/admin/`  
**请求方式**：浏览器访问（HTML 页面）  
**鉴权方式**：Django Session + CSRF（非 JWT）

## 6. 创建知识库

**接口路径**：`POST /api/kb/create`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Content-Type: application/json`
- `Authorization: Bearer <access>`

### 请求参数（JSON Body）
| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| name | string | 是 | 知识库名称（长度 <= 100） |
| description | string | 否 | 知识库描述 |

### 返回格式
**201 Created**
```json
{
  "id": 1,
  "name": "kb1",
  "description": "d1",
  "faiss_path": "E:\\code\\RAG\\rear_end\\faiss_indexes\\user_1\\kb_1.index",
  "created_at": "2026-02-20T12:34:56.123Z"
}
```

### 状态码
- `201`：创建成功（数据库新增记录，并在磁盘创建空索引文件）
- `400`：参数校验失败
- `401`：未携带 token / token 无效 / token 过期

### 备注
- 创建成功后会生成空索引文件，路径与返回的 `faiss_path` 一致
- 索引根目录可通过环境变量 `FAISS_INDEX_ROOT` 配置，默认 `BASE_DIR/faiss_indexes`

## 7. 获取我的知识库列表

**接口路径**：`GET /api/kb/list`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Authorization: Bearer <access>`

### 请求参数
无

### 返回格式
**200 OK**
```json
{
  "items": [
    {
      "id": 1,
      "name": "kb1",
      "description": "d1",
      "faiss_path": "E:\\code\\RAG\\rear_end\\faiss_indexes\\user_1\\kb_1.index",
      "created_at": "2026-02-20T12:34:56.123Z"
    }
  ]
}
```

### 状态码
- `200`：成功
- `401`：未携带 token / token 无效 / token 过期

## 8. 删除知识库

**接口路径**：`DELETE /api/kb/{id}`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Authorization: Bearer <access>`

### 路径参数
| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | number | 是 | 知识库 id |

### 返回格式
- **204 No Content**（无响应体）

### 状态码
- `204`：删除成功（删除数据库记录，并删除对应索引文件；若文件不存在也会删除成功）
- `401`：未携带 token / token 无效 / token 过期
- `404`：知识库不存在或不属于当前用户

## 9. 上传文档入库

**接口路径**：`POST /api/kb/upload`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Authorization: Bearer <access>`
- `Content-Type: multipart/form-data`

### 请求参数（Form）
| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| kb_id | number | 是 | 目标知识库 id |
| file | file | 是 | 上传文件（当前最小支持 txt） |
| on_conflict | string | 否 | 重名处理：`keep` 保留（随机文件名），`replace` 替换 |

### 返回格式
**201 Created**
```json
{
  "id": 1,
  "kb_id": 1,
  "filename": "a.txt",
  "chunk_count": 3,
  "uploaded_at": "2026-02-20T12:34:56.123Z"
}
```

### 状态码
- `201`：入库成功（保存文件、分块、向量化写入 FAISS、写入 Document/Chunk 记录）
- `400`：参数/文件校验失败（如文件无可用文本）
- `401`：未携带 token / token 无效 / token 过期
- `404`：kb_id 不存在或不属于当前用户

### 备注
- 向量化依赖 OpenAI 兼容 API（通过环境变量 `OPENAI_API_KEY` 或 `DASHSCOPE_API_KEY` 提供），并使用 LangChain 的 OpenAIEmbeddings
- 可通过 `OPENAI_EMBEDDING_MODEL`、`OPENAI_BASE_URL` 配置模型与接口地址

## 10. 获取知识库文档列表

**接口路径**：`GET /api/kb/{id}/documents`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Authorization: Bearer <access>`

### 路径参数
| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | number | 是 | 知识库 id |

### 返回格式
**200 OK**
```json
{
  "items": [
    {
      "id": 1,
      "filename": "a.txt",
      "chunk_count": 3,
      "uploaded_at": "2026-02-20T12:34:56.123Z"
    }
  ]
}
```

### 状态码
- `200`：成功
- `401`：未携带 token / token 无效 / token 过期
- `404`：知识库不存在或不属于当前用户

## 11. 删除单个文档（重建索引）

**接口路径**：`DELETE /api/document/{id}`  
**是否鉴权**：是（必须 Bearer access）

### 请求头
- `Authorization: Bearer <access>`

### 路径参数
| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | number | 是 | 文档 id |

### 返回格式
- **204 No Content**（无响应体）

### 状态码
- `204`：删除成功（删除 Document/Chunk 记录，删除原文件，重建该 kb 的 FAISS 索引）
- `401`：未携带 token / token 无效 / token 过期
- `404`：文档不存在或不属于当前用户
