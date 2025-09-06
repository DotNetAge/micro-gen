# 🎯 micro-gen CLI 完整指南

## 🚀 核心命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `micro-gen init` | 创建整洁架构微服务项目 | `<project_name>` | `micro-gen init user-service` |
| `micro-gen magic` | 魔法一键生成完整项目 | `--name` | `micro-gen magic --name api-gateway` |

## 🔧 增强功能命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `micro-gen es` | 添加事件溯源系统 | `--force` | `micro-gen es --force` |
| `micro-gen session` | 添加会话管理 | `--force` | `micro-gen session --force` |
| `micro-gen task` | 添加任务调度系统 | `--force` | `micro-gen task --force` |
| `micro-gen saga` | 添加Saga分布式事务 | `--force` | `micro-gen saga --force` |
| `micro-gen projection` | 添加投影机制 | `--force` | `micro-gen projection --force` |

## 🛠️ 实用工具命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `micro-gen crud` | 一键CRUD代码生成 | `--entity`, `--fields` | `micro-gen crud --entity user --fields "name:string,age:int,email:string"` |
| `micro-gen deploy` | 生成部署配置 | `--name`, `--env` | `micro-gen deploy --name my-service --env prod` |

## 📊 高级配置命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `micro-gen projection` | 基于配置生成投影机制 | `--config` | `micro-gen projection --config cqrs_config.yaml` |

## 🎯 参数详解

### 通用参数
- `--force`: 强制覆盖现有文件
- `--verbose`: 显示详细日志
- `--dry-run`: 预览生成内容

### CRUD参数
- `--entity`: 实体名称
- `--fields`: 字段定义（格式：`name:type,age:int`）
- `--repo`: 仓库类型（postgres/redis）
- `--handler`: 是否生成HTTP处理器

### 部署参数
- `--name`: 服务名称
- `--env`: 环境（dev/staging/prod）
- `--port`: 服务端口
- `--namespace`: K8s命名空间

## 🎪 组合使用示例

### 完整工作流
```bash
# 1. 创建项目
micro-gen init order-service

# 2. 进入项目
cd order-service

# 3. 添加事件溯源
micro-gen es --force

# 4. 添加CRUD实体
micro-gen crud --entity order --fields "id:string,user_id:string,amount:float,status:string"

# 5. 生成部署配置
micro-gen deploy --name order-service --env prod --port 8080

# 6. 一键魔法（替代以上所有步骤）
micro-gen magic --name order-service --with-crud --with-deploy
```

### 高级用法
```bash
# 会话管理 + 任务调度
micro-gen init auth-service
micro-gen session --force
micro-gen task --force

# 完整CQRS系统
micro-gen cqrs --config examples/clean-arch-config.yaml

# 微服务集群部署
micro-gen deploy --name user-service --env staging --namespace micro-services
```

## 🔍 配置文件示例

### CRUD配置
```yaml
# examples/crud-config.yaml
entity: user
fields:
  - name: id
    type: string
    primary: true
  - name: username
    type: string
    unique: true
  - name: email
    type: string
    validate: email
```

### CQRS配置
```yaml
# examples/clean-arch-config.yaml
module: user-service

# 值对象定义
value_objects:
  - name: Email
    fields:
      - name: value
        type: string
        required: true
        validation: email
  
  - name: Username
    fields:
      - name: value
        type: string
        required: true
        validation: "min:3,max:50"

aggregates:
  - name: User
    projection: true
    
    fields:
      - name: id
        type: string
      - name: username
        type: Username
      - name: email
        type: Email
      - name: createdAt
        type: time.Time
    
    commands:
      - name: CreateUser
        fields:
          - name: username
            type: Username
            required: true
          - name: email
            type: Email
            required: true
      
      - name: UpdateUserEmail
        fields:
          - name: userId
            type: string
            required: true
          - name: newEmail
            type: Email
            required: true
    
    events:
      - name: UserCreated
        fields:
          - name: userId
            type: string
          - name: username
            type: Username
          - name: email
            type: Email
          - name: createdAt
            type: time.Time
      
      - name: UserEmailUpdated
        fields:
          - name: userId
            type: string
          - name: newEmail
            type: Email
    
    read_model:
      name: UserSummary
      fields:
        - name: userId
          type: string
        - name: username
          type: string
        - name: email
          type: string
        - name: createdAt
          type: time.Time
```

## 🎨 使用建议

为了简化使用，建议创建shell别名：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
alias mg="micro-gen"

# 然后可以这样使用
mg init my-service
mg magic --name api-gateway
```

## 🎯 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `MICRO_GEN_VERBOSE` | 详细日志 | `false` |
| `MICRO_GEN_FORCE` | 强制模式 | `false` |
| `MICRO_GEN_DRY_RUN` | 预览模式 | `false` |

## 🚨 故障排除

### 常见错误及解决
```bash
# 模块未找到
pip install -e .

# 权限问题
sudo micro-gen init my-service

# 路径问题
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 🎭 开发者模式

### 本地开发
```bash
# 克隆项目
git clone https://github.com/DotNetAge/micro-gen.git
cd micro-gen

# 开发安装
pip install -e .

# 测试命令
micro-gen --help
```

### 调试技巧
- 使用`-v`或`--verbose`查看详细日志
- 使用`--force`强制覆盖现有文件
- 使用`--dry-run`预览生成内容

## 🏗️ 架构设计

### 整洁架构层次
```
cmd/api/          # 应用入口层
internal/         # 业务逻辑层
├── entity/       # 实体层
└── usecase/      # 用例层
adapter/          # 适配器层
├── handler/      # HTTP处理器
└── repo/         # 数据仓库
pkg/              # 公共库
data/             # 数据层
deploy/           # 部署配置
```

### 技术栈
- **语言**: Go 1.21+
- **架构**: 整洁架构 + 事件驱动
- **消息**: NATS JetStream
- **数据库**: PostgreSQL + Redis
- **监控**: Prometheus + Grafana
- **部署**: Docker + Kubernetes