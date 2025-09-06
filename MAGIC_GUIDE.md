# 🪄 Magic 魔法初始化指南

## 一键生成完整微服务

`magic` 命令让你只需一行代码就能创建包含所有功能的完整微服务！

## 🚀 快速开始

### 基础用法
```bash
# 在当前目录创建魔法微服务
micro-gen magic --name my-awesome-service

# 指定路径和名称
micro-gen magic --path ./projects --name full-stack-service

# 使用配置文件（推荐）
micro-gen magic --config ./examples/magic-config.yaml --name enterprise-service
```

### 完整参数
```bash
micro-gen magic [OPTIONS]

选项:
  --path TEXT    项目路径 (默认: 当前目录)
  --name TEXT    项目名称 (默认: magic-service)
  --config TEXT  配置文件路径 (可选，支持值对象和聚合投影)
  --force        强制覆盖现有文件
  --help         显示帮助信息
```

## 🎯 生成的功能

魔法初始化会自动集成以下所有功能：

| 功能 | 描述 | 技术栈 | 配置支持 |
|---|---|---|---|
| **项目结构** | 整洁架构 + Go官方实践 | Go 1.21+ | ✅ |
| **ES事件系统** | 事件溯源 + CQRS | NATS JetStream | ✅ |
| **会话管理** | 分布式会话存储 | Redis + Memory | ✅ |
| **任务系统** | 异步任务调度 | 内置调度器 | ✅ |
| **Saga事务** | 分布式事务管理 | Saga模式 | ✅ |
| **投影机制** | CQRS读模型 + 值对象 | 实时投影更新 | ✅ 完整配置 |
| **Docker部署** | 生产就绪的容器化 | Docker + Compose | ✅ |
| **Kubernetes部署** | 云原生部署清单 | K8s YAML | ✅ |
| **CI/CD流水线** | GitHub Actions自动化 | GitHub Actions | ✅ |
| **监控告警** | Prometheus + Grafana | 监控栈 | ✅ |
| **一键部署脚本** | Makefile快捷命令 | Make | ✅ |

## 📋 使用示例

### 1. 创建标准微服务（默认配置）
```bash
mkdir my-service && cd my-service
micro-gen magic --name my-service
```

### 2. 使用配置文件（完整功能）
创建 `magic-config.yaml`:
```yaml
# 项目名称
project:
  name: "user-service"
  description: "用户管理服务 - 完整的CQRS微服务"

# 值对象定义
value_objects:
  - name: "Email"
    fields:
      - name: "address"
        type: "string"
      - name: "verified"
        type: "bool"
  - name: "Address"
    fields:
      - name: "street"
        type: "string"
      - name: "city"
        type: "string"
      - name: "zipCode"
        type: "string"
        json: "zip_code"

# 聚合定义
aggregates:
  - name: "User"
    readModel:
      name: "UserReadModel"
      projection: true
      fields:
        - name: "userId"
          type: "string"
          json: "user_id"
        - name: "username"
          type: "string"
        - name: "email"
          type: "Email"  # 使用值对象
        - name: "address"
          type: "Address"  # 使用值对象
        - name: "createdAt"
          type: "time.Time"
          json: "created_at"

  - name: "Order"
    readModel:
      name: "OrderReadModel"
      projection: true
      fields:
        - name: "orderId"
          type: "string"
          json: "order_id"
        - name: "userId"
          type: "string"
          json: "user_id"
        - name: "totalAmount"
          type: "float64"
          json: "total_amount"
        - name: "shippingAddress"
          type: "Address"  # 使用值对象
        - name: "status"
          type: "string"

# 事件溯源配置
event_sourcing:
  nats:
    url: "nats://localhost:4222"

# 会话配置
session:
  redis:
    addr: "localhost:6379"
```

然后运行：
```bash
micro-gen magic --config magic-config.yaml --name user-service
```

### 3. 强制重新生成
```bash
micro-gen magic --force --name fresh-service
```

## 🔧 项目结构

执行后生成的目录结构：

```
my-service/
├── cmd/api/
│   └── main.go
├── internal/
│   ├── entity/
│   │   ├── email.go          # 值对象
│   │   ├── address.go        # 值对象
│   │   ├── user_read_model.go    # 聚合投影
│   │   └── order_read_model.go   # 聚合投影
│   ├── usecase/
│   │   ├── event/
│   │   ├── session/
│   │   ├── task/
│   │   ├── saga/
│   │   └── projection/     # 投影用例
├── pkg/
│   ├── config/
│   ├── event/
│   ├── session/
│   ├── task/
│   ├── saga/
│   └── projection/         # 投影基础设施
├── adapter/
│   ├── handler/
│   └── repo/
├── data/snapshots/
├── go.mod
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚦 启动步骤

生成项目后：

```bash
cd your-project

# 1. 安装依赖
go mod tidy

# 2. 启动基础设施
docker-compose up -d

# 3. 运行服务
go run cmd/api/main.go
```

## 🎨 配置文件示例

查看 `examples/magic-config.yaml` 获取完整配置示例，包含：

- 值对象定义（Email, Address, Phone等）
- 聚合投影配置（User, Order等）
- 事件溯源集成
- 会话管理配置
- 任务调度设置
- Saga事务管理
- 数据库连接
- 日志配置

## ✨ 特性亮点

- **零配置启动**：默认配置即可运行
- **完整投影支持**：值对象 + 聚合读模型
- **生产就绪**：包含Docker、监控、日志
- **可扩展**：基于整洁架构，易于扩展
- **文档齐全**：每个模块都有详细文档
- **测试覆盖**：包含完整的测试用例

## 🎪 一句话总结

> 一行命令，一个完整的微服务帝国！

```bash
micro-gen magic --name my-empire
```

或者使用配置文件：

```bash
micro-gen magic --config examples/magic-config.yaml --name my-empire
```