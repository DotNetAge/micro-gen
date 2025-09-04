"""
基础生成器类 - 为所有子命令提供统一接口
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict
import logging

class BaseGenerator(ABC):
    """所有生成器的基类"""
    
    def __init__(self, config: Any, base_path: Path):
        self.config = config
        self.base_path = Path(base_path)
        self.output_path = self.base_path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.project_name = config.project_name
        self.module_name = config.module_name
        self.package_name = config.package_name
    
    @abstractmethod
    def generate(self) -> None:
        """执行生成功能的抽象方法"""
        pass
    
    def ensure_directory(self, path: Path) -> None:
        """确保目录存在"""
        path.mkdir(parents=True, exist_ok=True)
    
    def write_file(self, file_path: Path, content: str) -> None:
        """写入文件，确保目录存在"""
        self.ensure_directory(file_path.parent)
        file_path.write_text(content, encoding='utf-8')
        self.logger.debug(f"已生成文件: {file_path}")
    
    def file_exists(self, file_path: Path) -> bool:
        """检查文件是否存在"""
        return file_path.exists()
    
    def get_template_context(self) -> Dict[str, Any]:
        """获取模板渲染上下文"""
        return {
            'config': self.config,
            'project_name': self.config.project_name,
            'module_name': self.config.module_name,
            'package_name': self.config.package_name,
        }