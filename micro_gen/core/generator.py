#!/usr/bin/env python3
"""
整洁架构事件驱动微服务核心生成器
基于Python的通用工具，无需Go环境
支持事件溯源 + CQRS + Projection完整实现
"""

import os
import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import argparse

from .domain_generator import DomainGenerator
from .usecase_generator import UseCaseGenerator
from .adapter_generator import AdapterGenerator
from .infrastructure_generator import InfrastructureGenerator
from .config_generator import ConfigGenerator
from .utils import *

class CleanArchitectureGenerator:
    """整洁架构事件驱动微服务生成器"""
    
    def __init__(self, config: Dict[str, Any], output_path: Path = None):
        self.config = config
        self.project_name = self.config['project']['name']
        self.base_path = output_path if output_path else Path.cwd() / self.project_name
        
        # 添加配置选项
        self.force = False
        self.dry_run = False
        
        # 类型映射
        self.go_type_mapping = {
            'string': 'string',
            'int': 'int',
            'float': 'float64',
            'bool': 'bool',
            'time': 'time.Time',
            'uuid': 'string'
        }
        
        self.proto_type_mapping = {
            'string': 'string',
            'int': 'int32',
            'float': 'float32',
            'bool': 'bool',
            'time': 'int64',
            'uuid': 'string'
        }
        
        # 初始化子生成器
        self.domain_generator = DomainGenerator(self.config, self.base_path)
        self.usecase_generator = UseCaseGenerator(self.config, self.base_path)
        self.adapter_generator = AdapterGenerator(self.config, self.base_path)
        self.infrastructure_generator = InfrastructureGenerator(self.config, self.base_path)
        self.config_generator = ConfigGenerator(self.config, self.base_path)
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate(self):
        """生成完整项目结构"""
        print(f"🚀 正在生成 {self.project_name} 整洁架构项目...")
        
        # 创建项目结构
        self.create_project_structure()
        
        # 生成核心代码
        self.domain_generator.generate()
        self.usecase_generator.generate()
        self.adapter_generator.generate()
        self.infrastructure_generator.generate()
        
        # 生成配置和脚本
        self.config_generator.generate()
        self.generate_readme()
        
        # 清理空目录
        self.cleanup_empty_dirs()
        
        print(f"✅ 项目生成完成！路径: {self.base_path}")
        print(f"🌐 支持HTTP RESTful API和gRPC双协议")
        print(f"⚡ gRPC端口: 50051, HTTP端口: 8080")
    
    def cleanup_empty_dirs(self):
        """清理空目录"""
        print("🧹 清理空目录...")
        removed_count = 0
        
        # 从深层目录开始，向上遍历
        for root, dirs, files in os.walk(self.base_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    # 检查目录是否为空
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        removed_count += 1
                        print(f"   删除空目录: {dir_path.relative_to(self.base_path)}")
                except (OSError, PermissionError):
                    # 忽略无法删除的目录
                    continue
        
        if removed_count > 0:
            print(f"   ✅ 已删除 {removed_count} 个空目录")
        else:
            print("   ✅ 没有发现空目录")
        
    def create_project_structure(self):
        """创建整洁架构项目结构"""
        structure = {
            'cmd': {
                'api': {},
                'consumer': {},
                'projection': {}
            },
            'internal': {
                'domain': {
                    'aggregate': {},
                    'event': {},
                    'repository': {},
                    'projection': {}
                },
                'usecase': {
                    'command': {},
                    'query': {},
                    'event': {}
                },
                'adapter': {
                    'inbound': {
                        'http': {},
                        'grpc': {}
                    },
                    'outbound': {
                        'repository': {},
                        'event': {},
                        'projection': {}
                    }
                },
                'infrastructure': {
                    'config': {},
                    'database': {},
                    'eventstore': {},
                    'projection': {},
                    'cache': {},
                    'session': {}
                }
            },
            'api': {
                'proto': {}
            },
            'configs': {},
            'migrations': {},
            'scripts': {},
            'tests': {}
        }
        
        for path, content in structure.items():
            self.create_nested_dirs(self.base_path / path, content)
    
    def create_nested_dirs(self, base: Path, structure: Dict[str, Any]):
        """递归创建目录结构"""
        for name, content in structure.items():
            path = base / name
            path.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict) and content:
                self.create_nested_dirs(path, content)
    
    def generate_readme(self):
        """生成README文档"""
        readme_content = f'''# {self.project_name}

Clean Architecture Go microservice project with HTTP RESTful API and gRPC dual protocol support

## Quick Start

### 1. Install Dependencies
```bash
go mod tidy
```

### 2. Install Protobuf Compiler
```bash
# macOS
brew install protobuf protoc-gen-go protoc-gen-go-grpc

# Ubuntu/Debian
sudo apt-get install protobuf-compiler protoc-gen-go protoc-gen-go-grpc
```

### 3. Generate gRPC Code
```bash
make proto-gen
```

### 4. Start Infrastructure Services
```bash
docker-compose up -d
```

### 5. Run Database Migration
```bash
make migrate-up
```

### 6. Start Application
```bash
make run
```

## API Endpoints

### HTTP RESTful API
- POST /api/v1/{self.config['aggregates'][0]['name'].lower()} - Create {self.config['aggregates'][0]['name']}
- GET /api/v1/{self.config['aggregates'][0]['name'].lower()}/:id - Get {self.config['aggregates'][0]['name']}

### gRPC Service
- Port: 50051
- Service Discovery Support (using grpcurl)

```bash
# List all services
grpcurl -plaintext localhost:50051 list

# Call service
grpcurl -plaintext -d '{{"id":"123"}}' localhost:50051 {self.config['aggregates'][0]['name'].lower()}.{self.config['aggregates'][0]['name']}Service/Get{self.config['aggregates'][0]['name']}
```

## Project Structure

```
{self.project_name}/
- cmd/api/main.go          # Application entry point
- internal/
  - domain/              # Domain layer
  - usecase/             # Use case layer
  - adapter/             # Adapter layer
    - http/            # HTTP adapter
    - grpc/            # gRPC adapter
  - infrastructure/        # Infrastructure layer
- api/proto/               # gRPC proto files
- migrations/              # Database migrations
- configs/config.yaml      # Configuration files
- docker-compose.yml       # Infrastructure services
- Makefile                # Build scripts
- README.md               # Project documentation
```

## Development

```bash
# Run tests
make test

# Build application
make build

# Clean build files
make clean

# Generate proto code
make proto-gen

# Database migration
make migrate-up
make migrate-down
```

## Protocol Support

### HTTP RESTful
- Based on Gin framework
- Standard RESTful design
- Suitable for external APIs and web frontend

### gRPC
- Based on Protocol Buffers
- High-performance binary protocol
- Suitable for internal service communication
- Supports streaming (extensible)
- Built-in service discovery and reflection

## Configuration

Configure in `configs/config.yaml`:
```yaml
server:
  port: 8080      # HTTP port
  grpc_port: 50051  # gRPC port
```

## Deployment

### Docker Deployment
```bash
make docker-build
make docker-run
```

### Environment Variables
Copy `configs/.env.example` to `configs/.env` and configure related environment variables.

## Technology Stack

- **Framework**: Gin (HTTP), gRPC-Go (gRPC)
- **Database**: PostgreSQL + GORM
- **Cache**: Redis
- **Message Queue**: NATS
- **Configuration**: Viper
- **Logging**: Zap
- **Migration**: golang-migrate
- **Testing**: testify

## Development Guidelines

1. **Prioritize gRPC for internal service communication**: gRPC excels in performance, type safety, and development efficiency compared to HTTP
2. **HTTP API for external interfaces**: Maintain RESTful design for easy third-party integration
3. **Use proto files as API contracts**: Define service interfaces via proto files to auto-generate client and server code
4. **Leverage gRPC middleware**: Use grpc-middleware for authentication, logging, rate limiting, and other features'''
        
        self.write_file(self.base_path / 'README.md', readme_content)
    
    def write_file(self, path: Path, content: str):
        """写入文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)