# 工具名常量
TOOL_NAMES = [
    "press_up_2048",
    "press_down_2048",
    "press_left_2048",
    "press_right_2048",
    "get_game_state_2048",
    "refresh_game_2048"
]

# 具体工具名
PRESS_UP_TOOL_NAME = "press_up_2048"
PRESS_DOWN_TOOL_NAME = "press_down_2048"
PRESS_LEFT_TOOL_NAME = "press_left_2048"
PRESS_RIGHT_TOOL_NAME = "press_right_2048"
GET_GAME_STATE_TOOL_NAME = "get_game_state_2048"
REFRESH_GAME_TOOL_NAME = "refresh_game_2048"

# 风险等级
RISK_LEVELS = ["low", "medium", "high", "critical"]
SECURITY_RISK_DESC = "操作安全风险等级：low(低风险)、medium(中风险)、high(高风险)、critical(极高风险)"

# 基础模板
BASE_TOOL_DESCRIPTION = "2048游戏工具：操作目标URL={url}"
GAME_URL = "https://www.2048.org/"

# 定位符常量
RESTART_BUTTON_LOCATOR_STR = "//a[text()='New Game']"

# 安全风险枚举（替代OpenHands SDK）
class ActionSecurityRisk:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

# Action类型常量
ActionType = {
    "RUN": "run"
}
TOOL_TYPE_MOVE = "move_2048"
TOOL_TYPE_GET_STATE = "get_state_2048"
TOOL_TYPE_REFRESH = "refresh_2048"

# 确认状态枚举
class ActionConfirmationStatus:
    CONFIRMED = "confirmed"
    PENDING = "pending"
    REJECTED = "rejected"