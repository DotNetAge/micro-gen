"""
配置管理模块
"""

import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """配置管理类"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.config_data = config_data
        self.project_name = config_data.get('project', {}).get('name', 'app')
        self.module_name = config_data.get('project', {}).get('module', 'app')
        self.package_name = config_data.get('project', {}).get('package', 'app')
        self.aggregates = config_data.get('aggregates', [])
        self.events = config_data.get('events', [])
        self.repositories = config_data.get('repositories', [])
        self.projections = config_data.get('projections', [])
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'Config':
        """从文件加载配置"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return cls(config_data)
    
    def get_aggregate_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取聚合配置"""
        for aggregate in self.aggregates:
            if aggregate['name'] == name:
                return aggregate
        return {}
    
    def get_events_for_aggregate(self, aggregate_name: str) -> list:
        """获取特定聚合的事件"""
        return [event for event in self.events 
                if event.get('aggregate') == aggregate_name]