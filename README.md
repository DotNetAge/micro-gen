# Micro-Gen - Go微服务代码生成器

> 15秒生成企业级Go微服务，支持整洁架构、CQRS、事件溯源、DDD

## 简介

Micro-Gen是一个Python编写的Go微服务代码生成器，通过简单的YAML配置或命令行参数，快速生成符合整洁架构、CQRS、事件溯源等模式的完整Go微服务项目。

**核心特性：**
- ✅ 整洁架构 + DDD + 六边形架构
- ✅ CQRS + 事件溯源 + 投影系统
- ✅ 零依赖核心，生成即可运行
- ✅ 一键部署到Docker/Kubernetes
- ✅ 完整的Makefile开发工具链

## 快速开始

### 安装

```bash
# pip安装
pip install micro-gen

# 源码安装
git clone https://github.com/micro-gen/micro-gen.git
cd micro-gen && pip install -e .
```

### 基本用法

```bash
# 1. 初始化新项目
micro-gen init my-service
cd my-service

# 2. 安装依赖并运行
go mod tidy
make dev

# 3. 访问健康检查
open http://localhost:8080/health
```

### 魔法初始化（一键完成所有功能）

```bash
# 使用魔法配置一键生成完整微服务
micro-gen magic --name my-service --config examples/magic-config.yaml

# 进入项目并启动
cd my-service
make dev
```



## 指令速查

| 指令 | 作用 | 示例 |
|---|---|---|
| `init` | 初始化最轻量微服务框架 | `micro-gen init my-service` |
| `es` | 为现有项目添加事件溯源机制 | `micro-gen es` |
| `session` | 为现有项目添加会话管理 | `micro-gen session` |
| `task` | 为现有项目添加任务系统 | `micro-gen task` |
| `saga` | 为现有项目添加Saga事务 | `micro-gen saga` |
| `crud` | 生成完整CRUD API | `micro-gen crud --config config.yaml` |
| `deploy` | 生成部署配置 | `micro-gen deploy --name my-app` |
| `projection` | 基于配置生成投影机制 | `micro-gen projection --config config.yaml` |
| `magic` | 魔法初始化 - 一键完成所有功能 | `micro-gen magic --name my-service` |

## 指令详细用法

### init - 初始化微服务

在当前目录创建新的微服务项目：

```bash
# 基本用法
micro-gen init my-service

# 结果：在当前目录生成 my-service/ 项目
```

### es - 添加事件溯源

为已存在的Go项目添加事件溯源机制：

```bash
# 在项目根目录执行
cd my-existing-project
micro-gen es
```

### session - 添加会话管理

为已存在的项目添加分布式会话管理：

```bash
cd my-existing-project
micro-gen session
```

### task - 添加任务系统

为已存在的项目添加异步任务处理：

```bash
cd my-existing-project
micro-gen task
```

### saga - 添加分布式事务

为已存在的项目添加Saga事务管理：

```bash
cd my-existing-project
micro-gen saga
```

### crud - 生成CRUD API

根据配置生成完整的CRUD API：

```bash
# 配置文件模式
micro-gen crud --config examples/crud-config.yaml

# 简单模式
micro-gen crud --entity User --fields "username:string,email:string,age:int"

# 指定项目路径
micro-gen crud --path ./my-project --entity Product --fields "name:string,price:float"
```

### deploy - 生成部署配置

生成Docker和Kubernetes部署配置：

```bash
# 基本用法
micro-gen deploy --name my-service

# 指定环境
micro-gen deploy --name my-service --env prod

# 指定项目路径
micro-gen deploy --path ./my-project --name my-service
```

### projection - 生成投影机制

基于配置文件生成投影代码：

```bash
micro-gen projection --config examples/magic-config.yaml
```

### magic - 魔法初始化

一键完成所有功能集成：

```bash
# 基本用法
micro-gen magic --name my-service

# 使用配置文件
micro-gen magic --config examples/magic-config.yaml --name my-service

# 指定路径
micro-gen magic --path ./my-project --name my-service
```

## DSL配置说明

### 1. 聚合配置 (CQRS)

```yaml
# aggregate.yaml
project:
  name: order-service
  module: github.com/your-org/order-service

aggregates:
  - name: Order
    fields:
      - name: customerId
        type: string
        validate: required
      - name: totalAmount
        type: float64
        validate: required,min=0
    
    events:
      - name: OrderCreated
        fields:
          - name: orderId
            type: string
          - name: customerId
            type: string
      
      - name: OrderPaid
        fields:
          - name: paymentId
            type: string
    
    readModel:
      name: OrderReadModel
      fields:
        - name: orderNumber
          type: string
        - name: status
          type: string
```

### 2. CRUD实体配置

```yaml
# crud-config.yaml
project:
  name: user-api
  port: 8080

entities:
  - name: User
    table: users
    fields:
      - name: id
        type: uuid
        primary: true
      - name: username
        type: string
        validate: required,min=3,max=50
      - name: email
        type: string
        validate: required,email
      - name: age
        type: int
        validate: min=18,max=120
    
    endpoints:
      - method: GET
        path: /users
        description: 获取用户列表
      - method: POST
        path: /users
        description: 创建用户
```

### 3. 部署配置

```yaml
# deploy-config.yaml
project:
  name: my-service
  version: 1.0.0

deployment:
  platform: kubernetes
  replicas: 3
  
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
  
  environment:
    - name: DATABASE_URL
      value: postgres://user:pass@localhost:5432/mydb
    - name: REDIS_URL
      value: redis://localhost:6379
```

## 示例

### 示例1：基础微服务

```bash
# 1. 生成服务
micro-gen init user-service

# 2. 进入项目目录
cd user-service

# 3. 安装依赖并启动
go mod tidy
make dev

# 4. 测试
curl http://localhost:8080/health
```

### 示例2：完整CRUD API

```bash
# 1. 先初始化项目
micro-gen init product-api
cd product-api

# 2. 使用配置文件生成CRUD
cat > crud-config.yaml << EOF
project:
  name: product-api
  port: 8080

entities:
  - name: Product
    fields:
      - name: name
        type: string
        validate: required
      - name: price
        type: float64
        validate: required,min=0
      - name: stock
        type: int
        validate: min=0
EOF

# 3. 生成CRUD API
micro-gen crud --config crud-config.yaml

# 4. 启动服务
make dev

# 5. 测试
curl -X POST http://localhost:8080/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone","price":999.99,"stock":100}'
```

### 示例3：魔法初始化（一键完成所有功能）

```bash
# 1. 使用魔法配置一键生成
micro-gen magic --name ecommerce --config examples/magic-config.yaml

# 2. 进入项目并启动
cd ecommerce
make dev

# 3. 查看生成的完整架构
# 包含：事件溯源、CQRS、投影、值对象、聚合等
```

### 示例4：为现有项目添加功能

```bash
# 1. 先创建基础项目
micro-gen init existing-service
cd existing-service

# 2. 添加事件溯源
micro-gen es

# 3. 添加会话管理
micro-gen session

# 4. 添加任务系统
micro-gen task

# 5. 添加分布式事务
micro-gen saga

# 6. 生成部署配置
micro-gen deploy --name existing-service
```

### 事件溯源电商系统

```bash
# 1. 使用魔法配置
micro-gen micro --config examples/magic-config.yaml --name ecommerce

# 2. 启动服务
cd ecommerce && make dev

# 3. 查看生成的聚合
# Order聚合、User聚合、Product聚合
# 包含完整的CQRS实现
```

### 示例4：一键部署到云

```bash
# 1. 生成部署配置
micro-gen deploy --name my-app --platform k8s --output ./deploy

# 2. 本地测试
cd deploy
make deploy-local

# 3. 生产部署
make deploy-k8s
```

## 更多资源

- [CLI指南](CLI_GUIDE.md) - 详细命令行用法
- [CQRS DSL指南](CQRS_DSL_GUIDE.md) - CQRS配置详解
- [CRUD指南](CRUD_GUIDE.md) - CRUD生成教程
- [部署指南](DEPLOY_GUIDE.md) - 一键部署教程
- [魔法指南](MAGIC_GUIDE.md) - 魔法初始化教程

## 许可证

MIT License - 开源免费