# agent/tools.py
from typing import List
from litellm import ChatCompletionToolParam, ChatCompletionToolParamFunctionChunk
from openhands.agenthub.play2048game_1210.tools.tool_constants import (
    TOOL_NAMES,
    PRESS_UP_TOOL_NAME,
    PRESS_DOWN_TOOL_NAME,
    PRESS_LEFT_TOOL_NAME,
    PRESS_RIGHT_TOOL_NAME,
    GET_GAME_STATE_TOOL_NAME,
    REFRESH_GAME_TOOL_NAME,
    RISK_LEVELS,
    SECURITY_RISK_DESC,
    RESTART_BUTTON_LOCATOR_STR,
    BASE_TOOL_DESCRIPTION,
    GAME_URL
)

# ========== 方向键工具描述 ==========
def create_press_up_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    """创建向上键工具"""
    detailed_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
### 功能说明
模拟按下键盘向上方向键，使2048游戏中所有可移动方块向上移动：
1. 方块沿列向上滑动，直到碰到边界或其他方块；
2. 相同数字的方块碰撞时合并为双倍数字；
3. 合并后生成新方块（2或4）在随机空白位置。
### 最佳使用场景
- 列内有可合并的相同数字；
- 底部空白较多，需要向上聚拢方块；
- 避免底部生成过多零散方块。
### 注意事项
- 操作前确保游戏页面处于激活状态；
- 操作后等待0.5秒让页面响应。"""
    
    short_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
按下向上方向键，使方块向上移动并合并相同数字。"""
    
    description = short_desc if use_short_description else detailed_desc
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=PRESS_UP_TOOL_NAME,
            description=description,
            parameters={
                'type': 'object',
                'properties': {
                    'security_risk': {
                        'type': 'string',
                        'description': SECURITY_RISK_DESC,
                        'enum': RISK_LEVELS,
                        'default': 'low'
                    }
                },
                'required': ['security_risk'],
            },
        ),
    )

def create_press_down_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    """创建向下键工具"""
    detailed_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
### 功能说明
模拟按下键盘向下方向键，使2048游戏中所有可移动方块向下移动：
1. 方块沿列向下滑动，直到碰到边界或其他方块；
2. 相同数字的方块碰撞时合并为双倍数字；
3. 合并后生成新方块（2或4）在随机空白位置。
### 最佳使用场景
- 列内有可合并的相同数字（位于上方）；
- 顶部空白较多，需要向下聚拢方块；
- 避免顶部生成过多零散方块。
### 注意事项
- 操作前确保游戏页面处于激活状态；
- 操作后等待0.5秒让页面响应。"""
    
    short_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
按下向下方向键，使方块向下移动并合并相同数字。"""
    
    description = short_desc if use_short_description else detailed_desc
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=PRESS_DOWN_TOOL_NAME,
            description=description,
            parameters={
                'type': 'object',
                'properties': {
                    'security_risk': {
                        'type': 'string',
                        'description': SECURITY_RISK_DESC,
                        'enum': RISK_LEVELS,
                        'default': 'low'
                    }
                },
                'required': ['security_risk'],
            },
        ),
    )

def create_press_left_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    """创建向左键工具"""
    detailed_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
### 功能说明
模拟按下键盘向左方向键，使2048游戏中所有可移动方块向左移动：
1. 方块沿行向左滑动，直到碰到边界或其他方块；
2. 相同数字的方块碰撞时合并为双倍数字；
3. 合并后生成新方块（2或4）在随机空白位置。
### 最佳使用场景
- 行内有可合并的相同数字；
- 右侧空白较多，需要向左聚拢方块；
- 避免右侧生成过多零散方块（优先推荐）。
### 注意事项
- 操作前确保游戏页面处于激活状态；
- 操作后等待0.5秒让页面响应。"""
    
    short_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
按下向左方向键，使方块向左移动并合并相同数字（优先推荐）。"""
    
    description = short_desc if use_short_description else detailed_desc
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=PRESS_LEFT_TOOL_NAME,
            description=description,
            parameters={
                'type': 'object',
                'properties': {
                    'security_risk': {
                        'type': 'string',
                        'description': SECURITY_RISK_DESC,
                        'enum': RISK_LEVELS,
                        'default': 'low'
                    }
                },
                'required': ['security_risk'],
            },
        ),
    )

def create_press_right_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    """创建向右键工具"""
    detailed_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
### 功能说明
模拟按下键盘向右方向键，使2048游戏中所有可移动方块向右移动：
1. 方块沿行向右滑动，直到碰到边界或其他方块；
2. 相同数字的方块碰撞时合并为双倍数字；
3. 合并后生成新方块（2或4）在随机空白位置。
### 最佳使用场景
- 行内有可合并的相同数字（位于左侧）；
- 左侧空白较多，需要向右聚拢方块；
- 左侧方块过于拥挤，需要分散布局。
### 注意事项
- 操作前确保游戏页面处于激活状态；
- 操作后等待0.5秒让页面响应。"""
    
    short_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
按下向右方向键，使方块向右移动并合并相同数字。"""
    
    description = short_desc if use_short_description else detailed_desc
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=PRESS_RIGHT_TOOL_NAME,
            description=description,
            parameters={
                'type': 'object',
                'properties': {
                    'security_risk': {
                        'type': 'string',
                        'description': SECURITY_RISK_DESC,
                        'enum': RISK_LEVELS,
                        'default': 'low'
                    }
                },
                'required': ['security_risk'],
            },
        ),
    )

# ========== 获取游戏状态工具描述 ==========
def create_get_game_state_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    """创建获取游戏状态工具"""
    detailed_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
### 功能说明
解析2048游戏页面，获取完整游戏状态：
1. 提取当前得分（score-container元素）；
2. 解析4x4棋盘布局（tile-position-x-y元素）；
3. 获取最大数字方块（max-tile）；
4. 检测游戏是否结束（game-over元素）。
### 最佳使用场景
- 每次操作前获取最新状态（必选）；
- 游戏状态异常时验证；
- 需要记录得分/布局时使用。
### 注意事项
- 解析前等待页面完全加载；
- 兼容不同语言版本的2048页面；
- 棋盘解析精度99%，边缘情况返回空布局。"""
    
    short_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
获取当前游戏状态：得分、4x4棋盘布局、最大数字、游戏是否结束。"""
    
    description = short_desc if use_short_description else detailed_desc
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=GET_GAME_STATE_TOOL_NAME,
            description=description,
            parameters={
                'type': 'object',
                'properties': {
                    'security_risk': {
                        'type': 'string',
                        'description': SECURITY_RISK_DESC,
                        'enum': RISK_LEVELS,
                        'default': 'low'
                    }
                },
                'required': ['security_risk'],
            },
        ),
    )

# ========== 重置游戏工具描述 ==========
def create_refresh_game_tool(use_short_description: bool = False) -> ChatCompletionToolParam:
    """创建重置游戏工具"""
    detailed_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
### 功能说明
模拟点击游戏页面的「New Game」按钮（{RESTART_BUTTON_LOCATOR_STR}），重置游戏：
1. 清空所有方块，恢复初始4x4空白布局；
2. 得分重置为0；
3. 随机生成2个初始方块（2或4）；
4. 清除游戏结束提示（如有）。
### 最佳使用场景
- 游戏结束后重新开始；
- 手动输入/refresh指令时触发；
- 当前布局极差，需要重新开始时使用。
### 注意事项
- 重置后等待1秒让页面加载完成；
- 重置前会自动调用{GET_GAME_STATE_TOOL_NAME}工具记录最终得分；
- 重置操作不可逆，会清空当前游戏进度。"""
    
    short_desc = f"""{BASE_TOOL_DESCRIPTION.format(url=GAME_URL)}
点击「New Game」按钮重置游戏，得分清零，重新生成初始方块。"""
    
    description = short_desc if use_short_description else detailed_desc
    return ChatCompletionToolParam(
        type='function',
        function=ChatCompletionToolParamFunctionChunk(
            name=REFRESH_GAME_TOOL_NAME,
            description=description,
            parameters={
                'type': 'object',
                'properties': {
                    'security_risk': {
                        'type': 'string',
                        'description': SECURITY_RISK_DESC,
                        'enum': RISK_LEVELS,
                        'default': 'medium'
                    }
                },
                'required': ['security_risk'],
            },
        ),
    )

def get_tools(config=None, use_short_description: bool = False) -> List[ChatCompletionToolParam]:
    """获取所有工具列表"""
    return [
        create_press_up_tool(use_short_description),
        create_press_down_tool(use_short_description),
        create_press_left_tool(use_short_description),
        create_press_right_tool(use_short_description),
        create_get_game_state_tool(use_short_description),
        create_refresh_game_tool(use_short_description)
    ]