# agent/llm_client.py
import litellm
from typing import Optional, Dict, Any

class LLMClient:
    """LLM通用客户端（适配url+name+api形式）"""
    def __init__(self, api_base: str, model_name: str, api_key: str):
        self.api_base = api_base  # LLM的url
        self.model_name = model_name  # LLM的name
        self.api_key = api_key  # LLM的api

        # 配置litellm
        litellm.api_base = self.api_base
        litellm.api_key = self.api_key

    def call(self, messages: list[Dict[str, Any]], tools: Optional[list[Dict[str, Any]]] = None) -> any:
        """
        通用LLM调用
        :param messages: Prompt列表（system+user）
        :param tools: 工具元数据（FC规范）
        :return: litellm的ModelResponse
        """
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1000
            )
            return response
        except Exception as e:
            raise Exception(f"LLM调用失败：{e}")