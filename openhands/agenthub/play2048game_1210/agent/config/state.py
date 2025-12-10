
# agent/config/state.py
from typing import List, Any, Dict, Optional
from openhands.agenthub.play2048game_1210.core.observation import Game2048Observation
from openhands.agenthub.play2048game_1210.tools.tool_constants import GAME_URL

class State:
    """OpenHands风格的State类（独立模块）"""
    def __init__(self, history: List[Any] = None, current_obs: Game2048Observation = None):
        self.history = history or []
        self.current_obs = current_obs or Game2048Observation(url=GAME_URL)

    def get_last_user_message(self) -> Optional[Any]:
        """获取最后一条用户消息"""
        for event in reversed(self.history):
            if hasattr(event, 'source') and event.source == 'user':
                return event
        return None

    def to_llm_metadata(self, model_name: str, agent_name: str) -> Dict[str, Any]:
        """生成LLM元数据"""
        return {
            "model_name": model_name,
            "agent_name": agent_name,
            "game_url": self.current_obs.url,
            "timestamp": self.current_obs.text[:20] if self.current_obs.text else ""
        }