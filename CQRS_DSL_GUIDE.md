# 🏗️ CQRS DSL 完整指南

> 基于聚合根的CQRS配置DSL，支持命令、事件、读模型的统一配置

## 📋 目录

1. [快速开始](#快速开始)
2. [值对象定义](#值对象定义)
3. [聚合根配置](#聚合根配置)
4. [命令定义](#命令定义)
5. [事件定义](#事件定义)
6. [读模型配置](#读模型配置)
7. [完整示例](#完整示例)
8. [最佳实践](#最佳实践)
9. [常见问题](#常见问题)

---

## 🚀 快速开始

```yaml
# cqrs-config.yaml
module: ecommerce

# 值对象定义
value_objects:
  - name: OrderItem
    fields:
      - name: productId
        type: string
        required: true
      - name: productName
        type: string
        required: true
      - name: quantity
        type: int
        required: true
      - name: price
        type: float64
        required: true
  
  - name: Address
    fields:
      - name: street
        type: string
        required: true
      - name: city
        type: string
        required: true
      - name: zipCode
        type: string
        required: true

aggregates:
  - name: Order
    projection: true  # 启用读模型
    
    # 聚合状态（写模型）
    fields:
      - name: customerId
        type: string
      - name: items
        type: "[]OrderItem"
      - name: shippingAddress
        type: Address
      - name: status
        type: string
    
    # 命令定义（业务动机）
    commands:
      - name: CreateOrder
        fields:
          - name: customerId
            type: string
            required: true
          - name: items
            type: "[]OrderItem"
            required: true
          - name: shippingAddress
            type: Address
            required: true
      
      - name: ConfirmOrder
        fields:
          - name: orderId
            type: string
            required: true
    
    # 事件定义（状态变化）
    events:
      - name: OrderCreated
        fields:
          - name: orderId
            type: string
          - name: customerId
            type: string
          - name: items
            type: "[]OrderItem"
          - name: shippingAddress
            type: Address
          - name: createdAt
            type: time.Time
      
      - name: OrderConfirmed
        fields:
          - name: orderId
            type: string
          - name: confirmedAt
            type: time.Time
    
    # 读模型配置（查询优化）
    read_model:
      name: OrderSummary
      fields:
        - name: orderId
          type: string
        - name: customerName
          type: string
        - name: totalAmount
          type: float64
        - name: itemCount
          type: int
        - name: status
          type: string
```

---

## 💎 值对象定义

值对象（Value Object）是DDD中的重要概念，用于表示没有身份标识的领域概念，如地址、金额等。

### 基本结构

```yaml
value_objects:
  - name: [值对象名称]
    description: [描述]           # 可选
    fields:
      - name: [字段名]
        type: [类型]
        required: [true/false]   # 默认为false
        validation: [规则]       # 可选验证规则
```

### 值对象特点

- **不可变性**：值对象一旦创建，属性不可更改
- **相等性**：基于属性值而非身份标识
- **无副作用**：方法不会改变对象状态
- **可组合**：值对象可以嵌套其他值对象

### 示例

```yaml
value_objects:
  - name: Email
    description: "邮箱地址"
    fields:
      - name: value
        type: string
        required: true
        validation: email
  
  - name: Money
    description: "货币金额"
    fields:
      - name: amount
        type: float64
        required: true
        validation: "min:0"
      - name: currency
        type: string
        required: true
        validation: "in:USD,EUR,CNY"
  
  - name: Address
    description: "邮寄地址"
    fields:
      - name: street
        type: string
        required: true
      - name: city
        type: string
        required: true
      - name: zipCode
        type: string
        required: true
        validation: "regex:^\\d{5}$"
      - name: country
        type: string
        required: true
```

### 使用场景

| 场景 | 示例 |
|------|------|
| **标识符** | 用户ID、订单号 |
| **度量** | 金额、重量、长度 |
| **描述** | 地址、颜色、尺寸 |
| **时间段** | 日期范围、时间间隔 |

### 嵌套值对象

值对象可以嵌套使用，形成复杂的领域概念：

```yaml
value_objects:
  - name: GeoLocation
    fields:
      - name: latitude
        type: float64
        required: true
      - name: longitude
        type: float64
        required: true
  
  - name: FullAddress
    fields:
      - name: street
        type: string
        required: true
      - name: city
        type: string
        required: true
      - name: location
        type: GeoLocation
        required: false
```

---

## 🏛️ 聚合根配置

### 基础结构

```yaml
# 值对象定义（可复用的数据结构）
value_objects:
  - name: Address
    fields:
      - name: street
        type: string
        required: true
      - name: city
        type: string
        required: true
      - name: zipCode
        type: string
        required: true
  
  - name: Money
    fields:
      - name: amount
        type: float64
        required: true
      - name: currency
        type: string
        required: true

# 聚合根定义
aggregates:
  - name: [聚合名称]
    projection: [true/false]    # 是否启用读模型
    
    # 聚合状态字段（写模型）
    fields:
      - name: [字段名]
        type: [类型]              # 可以是值对象名称
        required: [true/false]   # 可选
    
    # 命令定义
    commands: [...]
    
    # 事件定义
    events: [...]
    
    # 读模型配置
    read_model: [...]
```

### 支持的字段类型

| 类型 | Go类型 | 说明 |
|------|--------|------|
| `string` | `string` | 字符串 |
| `int` | `int` | 整数 |
| `int64` | `int64` | 64位整数 |
| `float64` | `float64` | 浮点数 |
| `bool` | `bool` | 布尔值 |
| `time.Time` | `time.Time` | 时间类型 |
| `[]T` | `[]T` | 切片类型 |
| `map[string]T` | `map[string]T` | 映射类型 |

---

## ⚡ 命令定义

命令代表业务意图，驱动聚合状态变化。

### 命令结构

```yaml
commands:
  - name: [命令名称]
    description: [描述]           # 可选
    fields:
      - name: [字段名]
        type: [类型]
        required: [true/false]   # 默认为false
        validation: [规则]       # 可选，如: "email", "min:1", "max:100"
```

### 命名规范

- 使用**动词+名词**格式：如 `CreateOrder`、`CancelPayment`
- 避免CRUD命名：使用业务语言而非技术语言
- 体现业务意图：`ConfirmOrder` 而非 `UpdateOrderStatus`

### 示例

```yaml
commands:
  - name: PlaceOrder
    description: "客户下单"
    fields:
      - name: customerId
        type: string
        required: true
      - name: items
        type: "[]OrderItem"
        required: true
      - name: shippingAddress
        type: Address
        required: true
  
  - name: CancelOrder
    description: "取消订单"
    fields:
      - name: orderId
        type: string
        required: true
      - name: reason
        type: string
        required: false
```

---

## 📊 事件定义

事件表示已发生的事实，是聚合间通信的媒介。

### 事件结构

```yaml
events:
  - name: [事件名称]
    description: [描述]           # 可选
    fields:
      - name: [字段名]
        type: [类型]
```

### 命名规范

- 使用**过去时态**：如 `OrderCreated`、`PaymentConfirmed`
- 体现事实：`OrderShipped` 而非 `OrderShip`
- 保持简洁：事件应该只包含必要信息

### 事件类型

| 事件类型 | 示例 | 说明 |
|----------|------|------|
| 创建事件 | `OrderCreated` | 聚合创建时发出 |
| 状态事件 | `OrderConfirmed` | 状态变化时发出 |
| 删除事件 | `OrderCancelled` | 聚合删除时发出 |

### 示例

```yaml
events:
  - name: OrderPlaced
    description: "订单已创建"
    fields:
      - name: orderId
        type: string
      - name: customerId
        type: string
      - name: items
        type: "[]OrderItem"
      - name: totalAmount
        type: float64
      - name: placedAt
        type: time.Time
  
  - name: OrderShipped
    description: "订单已发货"
    fields:
      - name: orderId
        type: string
      - name: trackingNumber
        type: string
      - name: shippedAt
        type: time.Time
```

---

## 📖 读模型配置

读模型优化查询性能，支持多种查询场景。

### 读模型结构

```yaml
read_model:
  name: [读模型名称]
  description: [描述]           # 可选
  fields:
    - name: [字段名]
      type: [类型]
      source: [来源]            # 可选，说明数据来源
  
  # 查询优化
  indexes:
    - [字段1, 字段2]            # 复合索引
  
  # 缓存配置
  cache:
    ttl: [时长]                # 如: "5m", "1h"
```

### 读模型设计原则

1. **去规范化**：为了查询性能，可以冗余存储数据
2. **查询导向**：根据实际查询需求设计字段
3. **版本演进**：支持字段添加，避免破坏性变更

### 示例

```yaml
read_model:
  name: OrderListView
  description: "订单列表查询视图"
  fields:
    - name: orderId
      type: string
    - name: customerName      # 去规范化存储
      type: string
    - name: totalAmount
      type: float64
    - name: status
      type: string
    - name: createdAt
      type: time.Time
  
  indexes:
    - [customerId, createdAt]
    - [status]
```

---

## 🎯 完整示例

### 电商系统 - 订单聚合

```yaml
module: ecommerce

description: "电商订单系统CQRS配置"

# 值对象定义
value_objects:
  - name: Address
    fields:
      - name: street
        type: string
        required: true
      - name: city
        type: string
        required: true
      - name: zipCode
        type: string
        required: true
      - name: country
        type: string
        required: true
  
  - name: Money
    fields:
      - name: amount
        type: float64
        required: true
      - name: currency
        type: string
        required: true
  
  - name: OrderItem
    fields:
      - name: productId
        type: string
        required: true
      - name: productName
        type: string
        required: true
      - name: quantity
        type: int
        required: true
      - name: price
        type: Money
        required: true

aggregates:
  - name: Order
    projection: true
    
    # 聚合状态
    fields:
      - name: id
        type: string
      - name: customerId
        type: string
      - name: items
        type: "[]OrderItem"
      - name: shippingAddress
        type: Address
      - name: status
        type: string
      - name: totalAmount
        type: Money
    
    # 命令
    commands:
      - name: CreateOrder
        fields:
          - name: customerId
            type: string
            required: true
          - name: items
            type: "[]OrderItem"
            required: true
          - name: shippingAddress
            type: Address
            required: true
      
      - name: ConfirmOrder
        fields:
          - name: orderId
            type: string
            required: true
      
      - name: CancelOrder
        fields:
          - name: orderId
            type: string
            required: true
          - name: reason
            type: string
    
    # 事件
    events:
      - name: OrderCreated
        fields:
          - name: orderId
            type: string
          - name: customerId
            type: string
          - name: items
            type: "[]OrderItem"
          - name: shippingAddress
            type: Address
          - name: totalAmount
            type: float64
          - name: createdAt
            type: time.Time
      
      - name: OrderConfirmed
        fields:
          - name: orderId
            type: string
          - name: confirmedAt
            type: time.Time
      
      - name: OrderCancelled
        fields:
          - name: orderId
            type: string
          - name: reason
            type: string
          - name: cancelledAt
            type: time.Time
    
    # 读模型
    read_model:
      name: OrderSummary
      fields:
        - name: orderId
          type: string
        - name: customerName
          type: string
        - name: itemCount
          type: int
        - name: totalAmount
          type: float64
        - name: status
          type: string
        - name: createdAt
          type: time.Time
```

---

## 🏆 最佳实践

### 1. 命令设计
- **单一职责**：每个命令只做一件事
- **业务语言**：使用领域术语，避免技术术语
- **验证前置**：在命令层面进行输入验证

### 2. 事件设计
- **不可变**：事件一旦发出，不可更改
- **自足性**：事件包含所有必要信息
- **版本化**：支持事件版本演进

### 3. 读模型设计
- **查询驱动**：根据UI/查询需求设计
- **去规范化**：适当冗余以提升性能
- **渐进演进**：支持字段添加，避免破坏

### 4. 聚合边界
- **一致性边界**：聚合内保证强一致性
- **业务边界**：基于业务规则划分
- **大小适中**：避免过大或过小的聚合

---

## ❓ 常见问题

### Q1: 什么时候需要读模型？

**A**: 当以下情况时：
- 需要复杂查询或报表
- 查询性能成为瓶颈
- 需要不同数据视图
- 需要缓存优化

### Q2: 命令和事件的区别？

**A**: 
- **命令** = 业务意图（可能失败）
- **事件** = 已发生事实（不会失败）

### Q3: 如何处理事件版本演进？

**A**: 
- 事件版本化：`OrderCreated_v1`, `OrderCreated_v2`
- 向上兼容：新事件处理器处理旧事件
- 迁移策略：逐步迁移，支持回滚

### Q4: 读模型如何保持同步？

**A**: 
- **最终一致性**：接受短暂不一致
- **重试机制**：处理网络/系统故障
- **监控告警**：及时发现同步延迟

---

## 🚀 使用命令

```bash
# 生成完整CQRS代码
micro-gen cqrs --config cqrs-config.yaml

# 查看帮助
micro-gen cqrs --help
```

---

**记住**：CQRS不是银弹，只有在**读写差异大**、**查询复杂**、**性能要求高**的场景下才推荐使用！