"""
Magic Enhancer - 最简命令序列
"""

import subprocess
from pathlib import Path
from typing import Optional


class MagicEnhancer:
    def __init__(self, project_path: Path, project_name: str):
        self.project_path = project_path
        self.project_name = project_name

    def magic_init(self, config_path: Optional[str] = None, force: bool = False):
        """最简单的魔法初始化"""
        
        # 构建命令序列
        cmd = f"micro-gen init {self.project_name}{' --force' if force else ''} && "
        cmd += f"cd {self.project_name} && micro-gen es && micro-gen session && micro-gen task && micro-gen saga"
        
        if config_path:
            cmd += f" && micro-gen projection --config {config_path} --module {self.project_name}"
        
        # 一次性执行
        subprocess.run(cmd, shell=True, check=True)