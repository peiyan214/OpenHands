# agent/config/llm_registry.py
import litellm
from litellm import ModelResponse
from typing import Dict, Any, Optional
from .agent_config import AgentConfig

class LLMClient:
    """精简版LLM客户端（独立模块）"""
    def __init__(self, model_name: str):
        # LLM基础配置
        self.config = type('LLMConfig', (object,), {
            'model': model_name,
            'max_message_chars': 4000,
            'vision_is_active': lambda: False
        })

    def completion(self, **kwargs) -> ModelResponse:
        """核心LLM调用方法"""
        return litellm.completion(
            model=self.config.model,
            messages=kwargs['messages'],
            tools=kwargs.get('tools', []),
            tool_choice=kwargs.get('tool_choice', "auto"),
            temperature=kwargs.get('temperature', 0.7),
            max_tokens=kwargs.get('max_tokens', 1000)
        )
    
    def is_caching_prompt_active(self) -> bool:
        """是否启用Prompt缓存"""
        return False
    

class LLMRegistry:
    """LLM注册器（独立模块）"""
    def __init__(self, config: AgentConfig):
        self.config = config
        # 全局配置litellm
        litellm.api_base = config.api_url
        litellm.api_key = config.api_key

    def get_router(self, config: AgentConfig) -> LLMClient:
        """获取LLM客户端实例"""
        return LLMClient(config.model_name)