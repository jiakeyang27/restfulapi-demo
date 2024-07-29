## API 文档

### 1. 获取 TOKEN 接口

**URL**: `/api/get-token`

**方法**: POST

**描述**: 获取访问 API 的 TOKEN，TOKEN 有效期为 6 小时。

**请求示例**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**响应示例**:
```json
{
    "token": "your_generated_token",
    "expires_in": 21600
}
```

### 2. 获取全量告警评级

**URL**: `/api/alerts`

**方法**: GET

**描述**: 获取全量告警评级，以 JSON 格式返回。需要 TOKEN 验证。

**请求头**:
```http
Authorization: Bearer your_generated_token
```

**响应示例**:
```json
[
    {
        "alert_id": 1,
        "alert_level": "Critical",
        "description": "Critical level alert"
    },
    {
        "alert_id": 2,
        "alert_level": "Warning",
        "description": "Warning level alert"
    }
]
```

### 3. 获取任意告警评级

**URL**: `/api/alerts/{alert_id}`

**方法**: GET

**描述**: 获取指定告警 ID 的告警评级，以 JSON 格式返回。需要 TOKEN 验证。

**请求头**:
```http
Authorization: Bearer your_generated_token
```

**响应示例**:
```json
{
    "alert_id": 1,
    "alert_level": "Critical",
    "description": "Critical level alert"
}
```

### 4. 添加告警评级

**URL**: `/api/alerts`

**方法**: POST

**描述**: 通过接口添加新的告警评级。需要 TOKEN 验证。

**请求示例**:
```json
{
    "alert_level": "Critical",
    "description": "Critical level alert"
}
```

**响应示例**:
```json
{
    "alert_id": 3,
    "alert_level": "Critical",
    "description": "Critical level alert",
    "message": "Alert added successfully"
}
```

## 1. 程序框架图

```plaintext
- app
  - controllers
    - authController.js
    - alertController.js
  - middlewares
    - authMiddleware.js
  - models
    - alertModel.js
    - userModel.js
  - routes
    - authRoutes.js
    - alertRoutes.js
  - app.js
  - config.js
  - database.js
- Dockerfile
- docker-compose.yml
- tests
  - auth.test.js
  - alert.test.js
```

## 2. 简单开发文档

### 简介

该项目是一个用于管理告警评级的 RESTful API 服务，提供获取 TOKEN、获取全量告警评级、获取任意告警评级及添加告警评级的功能，并通过 TOKEN 进行访问控制。

### 程序架构设计

该项目使用 Node.js 和 Express 框架进行开发，采用 MVC 模式进行架构设计。

### 模块详细设计

- **controllers**: 负责处理请求并返回响应。
  - `authController.js`: 处理 TOKEN 获取。
  - `alertController.js`: 处理告警评级的获取和添加。
- **middlewares**: 负责中间件逻辑。
  - `authMiddleware.js`: 处理 TOKEN 验证。
- **models**: 定义数据库模型。
  - `alertModel.js`: 定义告警评级模型。
  - `userModel.js`: 定义用户模型。
- **routes**: 定义路由。
  - `authRoutes.js`: 定义 TOKEN 获取相关路由。
  - `alertRoutes.js`: 定义告警评级相关路由。
- **config.js**: 配置文件，包含数据库连接信息及其他配置信息。
- **database.js**: 数据库连接逻辑。

### 接口说明

见上文 API 文档。

### 数据库设计

数据库使用 MongoDB，包含两个集合：

- **users**: 存储用户信息，包括 `username` 和 `password`。
- **alerts**: 存储告警评级信息，包括 `alert_id`、`alert_level` 和 `description`。

### 部署说明

1. 安装 Docker 和 Docker Compose。
2. 复制项目代码到服务器。
3. 执行以下命令构建并启动容器：
   ```sh
   docker-compose up --build
   ```

## 3. 完成 RESTful 接口开发并容器化部署

**Dockerfile**:
```Dockerfile
FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]
```

**docker-compose.yml**:
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - mongo
  mongo:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

## 4. 完成单元测试

**tests/auth.test.js**:
```javascript
const request = require('supertest');
const app = require('../app');
const assert = require('assert');

describe('Auth API', function() {
  it('should get a token', function(done) {
    request(app)
      .post('/api/get-token')
      .send({ username: 'test', password: 'test' })
      .expect(200)
      .end(function(err, res) {
        if (err) return done(err);
        assert(res.body.token);
        done();
      });
  });
});
```

**tests/alert.test.js**:
```javascript
const request = require('supertest');
const app = require('../app');
const assert = require('assert');

describe('Alert API', function() {
  it('should get all alerts', function(done) {
    request(app)
      .get('/api/alerts')
      .set('Authorization', 'Bearer test_token')
      .expect(200)
      .end(function(err, res) {
        if (err) return done(err);
        assert(Array.isArray(res.body));
        done();
      });
  });

  it('should get a single alert', function(done) {
    request(app)
      .get('/api/alerts/1')
      .set('Authorization', 'Bearer test_token')
      .expect(200)
      .end(function(err, res) {
        if (err) return done(err);
        assert(res.body.alert_id === 1);
        done();
      });
  });

  it('should add an alert', function(done) {
    request(app)
      .post('/api/alerts')
      .set('Authorization', 'Bearer test_token')
      .send({ alert_level: 'Critical', description: 'Test alert' })
      .expect(201)
      .end(function(err, res) {
        if (err) return done(err);
        assert(res.body.alert_id);
        done();
      });
  });
});
```

## 5. 完成用户侧接口使用文档

### 简介

该文档介绍如何使用告警评级管理 API，包括获取 TOKEN、获取全量告警评级、获取任意告警评级及添加告警评级的详细步骤。

### 获取 TOKEN

1. 发送 POST 请求到 `/api/get-token`，请求体包含 `username` 和 `password`。
2. 响应体将包含一个 `token` 和 `expires_in` 字段，`token` 用于后续接口的授权，`expires_in` 表示 TOKEN 的有效期（单位：秒）。

### 获取全量告警评级

1. 发送 GET 请求到 `/api/alerts`。
2. 在请求头中添加 `Authorization` 字段，值为 `Bearer your_generated_token`。
3. 响应体将包含所有告警评级的 JSON 数组。

### 获取任意告警评级

1. 发送 GET 请求到 `/api/alerts/{alert_id}`，将 `{alert_id}` 替换为要获取的告警 ID。
2. 在请求头中添加 `Authorization` 字段，值为 `Bearer your_generated_token`。
3. 响应体将包含指定告警 ID 的告警评级。

### 添加告警评级

1. 发送 POST 请求到 `/api/alerts`，请求体包含 `alert_level` 和 `description` 字段。
2. 在请求头中添加 `Authorization` 字段，值为 `Bearer your_generated_token`。
3. 响应体将包含新添加的告警评级的详细信息。

### 示例代码

**获取 TOKEN**:
```javascript
fetch('/api/get-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'your_username', password: 'your_password' })
})
.then(response => response.json())
.then(data => console.log(data.token));
```

**获取全量告警评级**:
```javascript
fetch('/api/alerts', {
  method: 'GET',
  headers: { 'Authorization': 'Bearer your_generated_token' }
})
.then(response => response.json())
.then(data => console.log(data));
```

**获取任意告警评级**

:
```javascript
fetch('/api/alerts/1', {
  method: 'GET',
  headers: { 'Authorization': 'Bearer your_generated_token' }
})
.then(response => response.json())
.then(data => console.log(data));
```

**添加告警评级**:
```javascript
fetch('/api/alerts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_generated_token'
  },
  body: JSON.stringify({ alert_level: 'Critical', description: 'Test alert' })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

这份文档涵盖了从获取 TOKEN 到使用各个告警评级 API 的详细步骤，并包括了示例代码，帮助用户更好地理解和使用 API。