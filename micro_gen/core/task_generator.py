#!/usr/bin/env python3
"""
任务机制生成器
为项目添加长时处理任务机制和定时任务机制
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any
from jinja2 import Template
from micro_gen.core.base_generator import BaseGenerator
from micro_gen.core.config import Config


class TaskGenerator(BaseGenerator):
    """任务机制生成器"""
    
    def __init__(self, project_path: str, project_name: str):
        super().__init__(project_path, project_name)
        self.template_dir = Path(__file__).parent / "templates" / "task"
        
    def generate(self, config: Config = None) -> Dict[str, Any]:
        """生成任务机制代码"""
        results = {
            "generated_files": [],
            "updated_files": [],
            "instructions": []
        }
        
        # 创建任务目录
        task_dir = Path(self.project_path) / "pkg" / "task"
        task_dir.mkdir(parents=True, exist_ok=True)
        
        internal_task_dir = Path(self.project_path) / "internal" / "usecase" / "task"
        internal_task_dir.mkdir(parents=True, exist_ok=True)
        
        entity_task_dir = Path(self.project_path) / "internal" / "entity"
        entity_task_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成实体文件
        entity_file = entity_task_dir / "task_data.go"
        self._generate_file(
            "entity_task.go.tmpl",
            entity_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(entity_file))
        
        # 生成任务存储接口和实现
        store_file = task_dir / "task_store.go"
        self._generate_file(
            "task_store.go.tmpl",
            store_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(store_file))
        
        # 生成Redis存储实现
        redis_store_file = task_dir / "redis_store.go"
        self._generate_file(
            "redis_store.go.tmpl",
            redis_store_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(redis_store_file))
        
        # 生成Badger存储实现
        badger_store_file = task_dir / "badger_store.go"
        self._generate_file(
            "badger_store.go.tmpl",
            badger_store_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(badger_store_file))
        
        # 生成任务服务用例
        usecase_file = internal_task_dir / "usecase_task.go"
        self._generate_file(
            "usecase_task.go.tmpl",
            usecase_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(usecase_file))
        
        # 生成任务管理器
        manager_file = task_dir / "task_manager.go"
        self._generate_file(
            "task_manager.go.tmpl",
            manager_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(manager_file))
        
        # 生成使用示例
        example_file = task_dir / "example_usage.go"
        self._generate_file(
            "example_usage.go.tmpl",
            example_file,
            {"project_name": self.project_name}
        )
        results["generated_files"].append(str(example_file))
        
        # 更新配置文件
        config_file = Path(self.project_path) / "pkg" / "config" / "config.go"
        if config_file.exists():
            self._update_config(config_file)
            results["updated_files"].append(str(config_file))
        
        # 生成使用说明
        results["instructions"] = [
            "🚀 任务机制添加完成！",
            "",
            "📁 生成的文件:",
            f"   • 实体定义: {entity_file}",
            f"   • 任务存储: {store_file}",
            f"   • Redis存储: {redis_store_file}",
            f"   • Badger存储: {badger_store_file}",
            f"   • 任务服务: {usecase_file}",
            f"   • 任务管理器: {manager_file}",
            f"   • 使用示例: {example_file}",
            "",
            "🔧 下一步:",
            "   1. 安装依赖:",
            "      go get github.com/redis/go-redis/v9",
            "      go get github.com/dgraph-io/badger/v4",
            "      go get github.com/robfig/cron/v3",
            "",
            "   2. 配置任务存储:",
            "      设置环境变量 TASK_LEVEL=low|normal|high",
            "      TASK_LEVEL=low (内存存储) - 开发/测试环境",
            "      TASK_LEVEL=normal (Badger存储) - 中小型项目",
            "      TASK_LEVEL=high (Redis存储) - 大型项目",
            "",
            "   3. 使用任务管理器:",
            "      查看 pkg/task/example_usage.go 了解使用方法",
            "",
            "   4. 任务类型示例:",
            "      • email_notification - 邮件通知",
            "      • report_generation - 报告生成",
            "      • data_cleanup - 数据清理",
            "      • backup_database - 数据库备份",
            "      • sync_data - 数据同步",
            "",
            "   5. 定时任务配置:",
            "      使用 cron 表达式设置定时任务",
            "      例如: '0 2 * * *' 每天凌晨2点执行"
        ]
        
        return results
    
    def _generate_file(self, template_name: str, output_path: Path, context: Dict[str, Any]):
        """生成单个文件"""
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        content = template.render(**context)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _update_config(self, config_file: Path):
        """更新配置文件以支持任务机制"""
        if not config_file.exists():
            return
        
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加任务配置
        task_config = """
	// 任务配置
	TaskLevel    string `yaml:"task_level" env:"TASK_LEVEL" env-default:"low"`
	TaskTimeout  int    `yaml:"task_timeout" env:"TASK_TIMEOUT" env-default:"30"` // 分钟
	TaskWorkers  int    `yaml:"task_workers" env:"TASK_WORKERS" env-default:"3"`
	TaskRetries  int    `yaml:"task_retries" env:"TASK_RETRIES" env-default:"3"`
"""
        
        # 在Config结构体中添加任务配置
        if 'TaskLevel' not in content:
            # 找到最后一个字段并添加新配置
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if line.strip().endswith('`yaml:"redis_db" env:"REDIS_DB" env-default:"0"`') or \
                   line.strip().endswith('`yaml:"session_timeout" env:"SESSION_TIMEOUT" env-default:"24"`') or \
                   line.strip().endswith('`yaml:"session_level" env:"SESSION_LEVEL" env-default:"low"`'):
                    new_lines.append(task_config.strip())
                    break
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python task_generator.py <project_path> <project_name>")
        sys.exit(1)
    
    generator = TaskGenerator(sys.argv[1], sys.argv[2])
    results = generator.generate()
    
    print("🚀 任务机制生成完成！")
    for instruction in results["instructions"]:
        print(instruction)