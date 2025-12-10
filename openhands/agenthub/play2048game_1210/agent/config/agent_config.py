# agent/config/agent_config.py
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class AgentConfig:
    """OpenHands风格的Agent配置类（独立模块）"""
    # LLM核心配置
    api_url: str
    model_name: str
    api_key: str
    
    # 工具配置
    use_short_tool_desc: bool = False
    
    # 提示词配置
    resolved_system_prompt_filename: Optional[str] = "system_prompt.txt"
    
    # 压缩器配置（默认禁用）
    condenser: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.condenser is None:
            self.condenser = {"type": "none"}  # 禁用对话压缩