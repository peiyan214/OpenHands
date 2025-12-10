# core/observation.py
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Game2048Observation:
    """自主设计的2048 Observation（含url+name核心字段）"""
    # LLM核心字段
    url: str  # 游戏页面URL
    name: str = "2048 Game"  # 游戏名
    # 游戏状态字段
    text: str = ""  # 描述文本
    is_error: bool = False
    score: Optional[int] = 0
    board: List[List[int]] = field(default_factory=lambda: [[0]*4 for _ in range(4)])
    game_over: Optional[bool] = False
    # 扩展字段
    title: Optional[str] = None  # 页面标题

    @property
    def to_llm_content(self) -> str:
        """转为LLM可理解的文本"""
        llm_text = f"【2048游戏状态】\n"
        llm_text += f"- 游戏URL：{self.url}\n"
        llm_text += f"- 游戏名称：{self.name}\n"
        if self.title:
            llm_text += f"- 页面标题：{self.title}\n"
        llm_text += f"- 当前得分：{self.score}\n"
        llm_text += f"- 棋盘布局：\n  {chr(10).join(['  '.join(map(str, row)) for row in self.board])}\n"
        llm_text += f"- 游戏是否结束：{self.game_over}\n"
        if self.is_error:
            llm_text += f"- 错误信息：{self.text}\n"
        else:
            llm_text += f"- 状态描述：{self.text}\n"
        return llm_text