# agent/game_agent.py
import os
import sys
from collections import deque
from typing import Deque, List, Optional, Dict, Any
from litellm import ModelResponse

from openhands.agenthub.play2048game_1210.agent.config import AgentConfig, LLMRegistry, State
from openhands.agenthub.play2048game_1210.tools.tool_constants import TOOL_NAMES, GAME_URL
from openhands.agenthub.play2048game_1210.tools.tools import get_tools
from openhands.agenthub.play2048game_1210.agent.function_calling import response_to_actions

from openhands.agenthub.play2048game_1210.core.actions import Action, AgentFinishAction, AgentThinkAction, MessageAction
from openhands.agenthub.play2048game_1210.core.observation import Game2048Observation

# 核心2048 Agent类（仅保留游戏相关逻辑）
class Play2048Agent:
    VERSION = '1.0'
    """2048 Game Agent（基于OpenHands框架，仅保留游戏逻辑）"""

    def __init__(self, config: AgentConfig, prompt_manager, llm_registry: LLMRegistry) -> None:
        self.config = config
        self.prompt_manager = prompt_manager
        self.llm_registry = llm_registry
        
        self.pending_actions: Deque[Action] = deque()
        self.game_over: bool = False
        self.max_score: int = 0

        self.tools = get_tools(config, config.use_short_tool_desc)

        self.llm = self.llm_registry.get_router(config)

    def reset(self) -> None:
        """重置Agent游戏状态"""
        self.pending_actions.clear()
        self.game_over = False
        self.max_score = 0
        print("✅ 2048 Agent reset successfully")

    def step(self, state: State) -> Action:
        """核心游戏步骤处理"""
        if self.pending_actions:
            return self.pending_actions.popleft()
        
        latest_user_message = state.get_last_user_message()
        if latest_user_message and latest_user_message.content.strip() in ['/exit', '/quit']:
            return AgentFinishAction()

        initial_user_message = self._get_initial_user_message(state.history)

        messages, game_state_now = self._get_messages(initial_user_message, state.current_obs)
        self._log_states(game_state_now)

        params = self._build_llm_params(messages, state)
        response = self.llm.completion(** params)

        actions = self.response_to_actions(response)

        for action in actions:
            self.pending_actions.append(action)

        return self.pending_actions.popleft()

    def _get_initial_user_message(self, history: List[Any]) -> MessageAction:
        """获取初始用户消息"""
        for event in history:
            if isinstance(event, MessageAction) and getattr(event, 'source', '') == 'user':
                return event
        return MessageAction(content="play 2048 game and get high score", source="user")

    def _get_messages(self, initial_msg: MessageAction, current_obs: Game2048Observation) -> List[Dict[str, Any]]:
        """构造2048游戏专用LLM消息"""
        system_prompt = self.prompt_manager.fixed_system_prompt
        
        messages = [{"role": "system", "content": system_prompt}]

        # 2. 初始用户指令
        messages.append({
            "role": "user",
            "content": initial_msg.content
        })

        # 3. 游戏状态（核心）
        game_state_str = current_obs.to_llm_content
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"\n## 2048游戏实时状态:\n{game_state_str}\n## 可用工具: {', '.join(TOOL_NAMES)}"
                }
            ]
        })

        return messages, game_state_str

    def _build_llm_params(self, messages: List[Dict[str, Any]], state: State) -> Dict[str, Any]:
        """构建2048游戏LLM调用参数"""
        return {
            'messages': messages,
            'tools': self.tools,
            'tool_choice': "auto",
            'temperature': 0.7,
            'extra_body': {
                'metadata': state.to_llm_metadata(
                    model_name=self.llm.config.model, 
                    agent_name=f"Play2048Agent_v{self.VERSION}"
                )
            }
        }

    def _log_states(self, game_state_now) -> None:
        print("\n" + "="*60)
        print(f"game state is {game_state_now}")
    
        print("="*60 + "\n")

    def response_to_actions(self, response: ModelResponse) -> List[Action]:
        """解析LLM响应为游戏Action"""
        return response_to_actions(response)

    def stop(self) -> None:
        """停止游戏Agent"""
        print(f"\n🎮 2048游戏结束 | 最高得分：{self.max_score}")
        print("🛑 2048 Agent stopped, resources cleaned up")