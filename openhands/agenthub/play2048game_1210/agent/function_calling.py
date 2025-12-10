# agent/fc_parser.py
import json
from typing import List

from openhands.agenthub.play2048game_1210.core.actions import (
    Action,
    AgentThinkAction,
    MessageAction,
    AgentFinishAction,
    Move2048Action,
    GetGameState2048Action,
    RefreshGame2048Action
)
from openhands.agenthub.play2048game_1210.tools.tool_constants import (
    TOOL_NAMES,
    PRESS_UP_TOOL_NAME,
    PRESS_DOWN_TOOL_NAME,
    PRESS_LEFT_TOOL_NAME,
    PRESS_RIGHT_TOOL_NAME,
    GET_GAME_STATE_TOOL_NAME,
    REFRESH_GAME_TOOL_NAME,
    ActionSecurityRisk
)

class FunctionCallNotExistsError(Exception):
    pass

class FunctionCallValidationError(Exception):
    pass

# 复用你的combine_thought函数
def combine_thought(action: Action, thought: str) -> Action:
    """复用 CodeAct 的 combine_thought 函数 """
    if not hasattr(action, 'thought'):
        return action
    if thought and action.thought:
        action.thought = f'{thought}\n{action.thought}'
    elif thought:
        action.thought = thought
    return action

# 复用你的set_security_risk函数
def set_security_risk(action: Action, arguments: dict) -> None:
    risk_str = arguments.get("security_risk", "low").lower()
    if risk_str == "low":
        action.security_risk = ActionSecurityRisk.LOW  
    elif risk_str == "medium":
        action.security_risk = ActionSecurityRisk.MEDIUM  
    elif risk_str == "high":
        action.security_risk = ActionSecurityRisk.HIGH 
    elif risk_str == "critical":
        action.security_risk = ActionSecurityRisk.CRITICAL 
    else:
        action.security_risk = ActionSecurityRisk.UNKNOWN 

# 复用你的response_to_actions函数（仅替换SDK依赖）
def response_to_actions(
    response: any,  # 兼容litellm的ModelResponse
) -> List[Action]:
    """
    核心解析函数（完全对齐你的CodeAct结构）
    """
    actions: list[Action] = []
    # CodeAct 核心断言：只处理单 choice 响应
    assert len(response.choices) == 1, 'Only one choice is supported for now'
    choice = response.choices[0]
    assistant_msg = choice.message

    # print("\n🔍 LLM 原始响应详情：")
    # print(f"  响应类型：{type(assistant_msg.content)}")
    # print(f"  响应内容：{assistant_msg.content}")
    # print(f"  是否有工具调用：{hasattr(assistant_msg, 'tool_calls')}")

    if hasattr(assistant_msg, 'tool_calls') and assistant_msg.tool_calls:
        thought = ''
        if isinstance(assistant_msg.content, str):
            thought = assistant_msg.content
        elif isinstance(assistant_msg.content, list):
            for msg in assistant_msg.content:
                if msg['type'] == 'text':
                    thought += msg['text']

        for i, tool_call in enumerate(assistant_msg.tool_calls):
            
            # 解析参数
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.decoder.JSONDecodeError as e:
                raise FunctionCallValidationError(
                    f'Failed to parse tool call arguments: {tool_call.function.arguments}'
                ) from e

            action: Action
            tool_name = tool_call.function.name
            if tool_name not in TOOL_NAMES:
                raise FunctionCallNotExistsError(f"unknown tool:{tool_name}")
            
            # ---------------------- 方向键工具：映射到Move2048Action ----------------------
            if tool_name == PRESS_UP_TOOL_NAME:
                action = Move2048Action(direction="up", thought=thought)
                set_security_risk(action, arguments)
            elif tool_name == PRESS_DOWN_TOOL_NAME:
                action = Move2048Action(direction="down", thought=thought)
                set_security_risk(action, arguments)
            elif tool_name == PRESS_LEFT_TOOL_NAME:
                action = Move2048Action(direction="left", thought=thought)
                set_security_risk(action, arguments)
            elif tool_name == PRESS_RIGHT_TOOL_NAME:
                action = Move2048Action(direction="right", thought=thought)
                set_security_risk(action, arguments)

            # ---------------------- 获取游戏状态：映射到GetGameState2048Action ----------------------
            elif tool_name == GET_GAME_STATE_TOOL_NAME:
                action = GetGameState2048Action(thought=thought)
                set_security_risk(action, arguments)

            # ---------------------- 重置游戏：映射到RefreshGame2048Action ----------------------
            elif tool_name == REFRESH_GAME_TOOL_NAME:
                action = RefreshGame2048Action(thought=thought)
                set_security_risk(action, arguments)

            # ---------------------- 未知工具：抛错（和参考代码逻辑一致） ----------------------
            else:
                raise ValueError(
                    f'Tool {tool_name} is not registered for 2048 game. Allowed tools: '
                    f'{[PRESS_UP_TOOL_NAME, PRESS_DOWN_TOOL_NAME, PRESS_LEFT_TOOL_NAME, PRESS_RIGHT_TOOL_NAME, GET_GAME_STATE_TOOL_NAME, REFRESH_GAME_TOOL_NAME]}'
                )

            # 3. 绑定工具调用元数据（和参考代码一致）
            action.tool_call_metadata = tool_call  # 简化版，后续可完善

            # 4. 只给第一个Action添加thought（参考代码逻辑）
            if i == 0:
                action = combine_thought(action, thought)

            actions.append(action)
    else:
        # 无工具调用时返回纯文本消息
        actions.append(
            MessageAction(
                content=str(assistant_msg.content) if assistant_msg.content else '',
                wait_for_response=True,
            )
        )
    for action in actions:
        action.response_id = response.id if hasattr(response, 'id') else None

    assert len(actions) >= 1
    return actions