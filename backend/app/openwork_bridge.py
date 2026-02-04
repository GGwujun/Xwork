"""
OpenWork桥接模块
用于从OpenWork获取OpenCode服务URL
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class OpenWorkBridge:
    """OpenWork桥接器，用于获取OpenCode服务信息"""

    def __init__(self):
        # OpenWork服务信息文件路径
        # Windows: %APPDATA%/openwork/engine-info.json
        # macOS/Linux: ~/.config/openwork/engine-info.json
        self.info_file = self._get_info_file_path()

    def _get_info_file_path(self) -> Path:
        """获取服务信息文件路径"""
        if os.name == 'nt':  # Windows
            appdata = os.getenv('APPDATA', '')
            base_dir = Path(appdata) / 'openwork'
        else:  # macOS/Linux
            home = Path.home()
            base_dir = home / '.config' / 'openwork'

        return base_dir / 'engine-info.json'

    def get_opencode_url(self) -> Optional[str]:
        """
        从OpenWork获取OpenCode服务URL

        Returns:
            OpenCode服务URL，如果服务未运行则返回None
        """
        try:
            if not self.info_file.exists():
                logger.warning(f"OpenWork服务信息文件不存在: {self.info_file}")
                return None

            with open(self.info_file, 'r', encoding='utf-8') as f:
                info = json.load(f)

            if not info.get('running'):
                logger.warning("OpenCode服务未运行")
                return None

            base_url = info.get('base_url')
            if not base_url:
                logger.warning("OpenCode服务URL为空")
                return None

            logger.info(f"从OpenWork获取到OpenCode服务URL: {base_url}")
            return base_url

        except Exception as e:
            logger.error(f"读取OpenWork服务信息失败: {str(e)}")
            return None

    def get_service_info(self) -> Optional[Dict[str, Any]]:
        """
        获取完整的服务信息

        Returns:
            服务信息字典，包含running, base_url, port, project_dir等
        """
        try:
            if not self.info_file.exists():
                return None

            with open(self.info_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"读取OpenWork服务信息失败: {str(e)}")
            return None


# 全局实例
_bridge_instance = None


def get_openwork_bridge() -> OpenWorkBridge:
    """获取OpenWork桥接器实例"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = OpenWorkBridge()
    return _bridge_instance
