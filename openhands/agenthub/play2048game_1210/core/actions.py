# core/actions.py
from dataclasses import dataclass, field
from typing import ClassVar, Optional

from ..tools.tool_constants import (
    ActionType,
    TOOL_TYPE_MOVE,
    TOOL_TYPE_GET_STATE,
    TOOL_TYPE_REFRESH,
    ActionSecurityRisk,
    ActionConfirmationStatus
)


@dataclass
class ToolCallMetadata:
    tool_call_id: Optional[str] = None
    function_name: Optional[str] = None
    model_response: Optional[any] = None
    total_calls_in_response: Optional[int] = None


@dataclass
class Action:
    action: str = ActionType["RUN"]
    security_risk: ActionSecurityRisk = ActionSecurityRisk.LOW
    thought: str = ""
    runnable: ClassVar[bool] = True
    confirmation_state: ActionConfirmationStatus = ActionConfirmationStatus.CONFIRMED
    tool_call_metadata: Optional[ToolCallMetadata] = None
    response_id: Optional[str] = None
    source : str = 'user'


@dataclass(kw_only=True)
class Move2048Action(Action):
    """2048方向键操作专属Action（适配tools调用）"""
    direction: str  
    tool_type: str = TOOL_TYPE_MOVE
    security_risk: ActionSecurityRisk = ActionSecurityRisk.LOW
    thought: str = ""
    runnable: ClassVar[bool] = True
    confirmation_state: ActionConfirmationStatus = ActionConfirmationStatus.CONFIRMED
    tool_call_metadata: Optional[ToolCallMetadata] = None

    def __str__(self) -> str:
        ret = f"**Move2048Action (direction={self.direction.upper()})**\n"
        if self.thought:
            ret += f"THOUGHT: {self.thought}\n"
        ret += f"SECURITY RISK: {self.security_risk}"
        return ret

    @property
    def message(self) -> str:
        return f"2048 Game: Press {self.direction.upper()} arrow key"


@dataclass
class GetGameState2048Action(Action):
    """获取游戏状态Action"""
    tool_type: str = TOOL_TYPE_GET_STATE
    security_risk: ActionSecurityRisk = ActionSecurityRisk.LOW
    thought: str = ""

    def __str__(self) -> str:
        ret = "**GetGameState2048Action**\n"
        if self.thought:
            ret += f"THOUGHT: {self.thought}\n"
        ret += f"SECURITY RISK: {self.security_risk}"
        return ret

    @property
    def message(self) -> str:
        return "2048 Game: Get current game state (score/board)"


@dataclass
class RefreshGame2048Action(Action):
    """重置游戏Action"""
    tool_type: str = TOOL_TYPE_REFRESH
    security_risk: ActionSecurityRisk = ActionSecurityRisk.MEDIUM
    thought: str = ""

    def __str__(self) -> str:
        ret = "**RefreshGame2048Action**\n"
        if self.thought:
            ret += f"THOUGHT: {self.thought}\n"
        ret += f"SECURITY RISK: {self.security_risk}"
        return ret

    @property
    def message(self) -> str:
        return "2048 Game: Refresh game (start new round)"


@dataclass
class AgentThinkAction(Action):
    """思考Action"""
    thought: str = ""

@dataclass
class MessageAction(Action):
    """消息Action"""
    content: str = ""
    wait_for_response: bool = True
    source : str = 'user'


@dataclass
class AgentFinishAction(Action):
    """结束Action"""
    content: str = ""