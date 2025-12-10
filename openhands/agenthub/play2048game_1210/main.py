import yaml
import os
from typing import Dict
from .env.game_env import Game2048Env
from .agent.config import AgentConfig, LLMRegistry, State
from .agent.game_agent import Play2048Agent
from .core.actions import RefreshGame2048Action, MessageAction
from .tools.tools import GAME_URL
from jinja2 import Environment, FileSystemLoader

cfg_path = './openhands/agenthub/play2048game_1210/config.yaml'


def load_yaml_config(cfg_path='') -> Dict:
    """精简版YAML配置加载（仅核心逻辑，无冗余验证）"""
    cfg_path = cfg_path
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"配置文件不存在：{cfg_path}")
    
    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    
    cfg.setdefault("steps", 10)
    cfg["llm"] = cfg.get("llm", {})
    cfg["llm"].setdefault("model", "gpt-3.5-turbo")
    cfg["llm"].setdefault("api_url", "https://api.openai.com/v1")
    cfg["llm"].setdefault("short_tool_desc", False)
    cfg["game"] = cfg.get("game", {})
    cfg["game"].setdefault("url", GAME_URL)
    cfg["game"].setdefault("headless", False)

    assert cfg["llm"].get("api_key"), "配置文件缺少llm.api_key"
    return cfg


class PromptManager:
    """支持从配置读取模板路径的Prompt管理器"""
    def __init__(self):
        """
        初始化Prompt管理器
        :param prompt_config: 配置文件中的prompt节点（包含template_dir/system_template/user_template）
        """
        self.current_script_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = os.path.join(self.current_script_dir,"prompts")
        self.system_template_name = "system_prompt.j2"
        self.user_template_name = "user_prompt.j2"

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        self.system_template = self.env.get_template(self.system_template_name)
        self.user_template = self.env.get_template(self.user_template_name)
        self.system_prompt = self.render_system_prompt() 

    @property
    def fixed_system_prompt(self) -> str:
        return self.system_prompt
    
    def render_system_prompt(self, **kwargs) -> str:
        return self.system_template.render(**kwargs)

    def render_user_prompt(self, **kwargs) -> str:
        return self.user_template.render(**kwargs)
    

def main():
    cfg = load_yaml_config(cfg_path)
    print(f"📋 加载配置：步骤={cfg['steps']} | 模型={cfg['llm']['model']} | 游戏地址={cfg['game']['url']}")

    prompt_manager = PromptManager()

    env = Game2048Env(
        headless=cfg["game"]["headless"],         
        game_url=cfg["game"]["url"]
    )
    print(f"✅ 2048游戏环境初始化完成：{env.current_obs.url}")

    # 初始化Agent配置
    agent_config = AgentConfig(
        api_url=cfg["llm"]["api_url"],         
        model_name=cfg["llm"]["model"],         
        api_key=cfg["llm"]["api_key"],           
        use_short_tool_desc=cfg["llm"]["short_tool_desc"]  
    )

    # 初始化LLM注册器和Agent
    llm_registry = LLMRegistry(agent_config)
    agent = Play2048Agent(
        agent_config, 
        prompt_manager,
        llm_registry)
    agent.reset()
    print("✅ 2048游戏Agent初始化完成")

    # 4. 初始化游戏状态
    state = State(current_obs=env.current_obs)
    state.history.append(MessageAction(content="play 2048 game and get highest score", source="user"))

    try:
        for step in range(cfg["steps"]):
            print(f"\n===== 游戏步骤 {step+1} =====")
            
            # Agent生成游戏动作
            action = agent.step(state)
            print(f"🚀 执行动作: {action}")

            # 环境执行动作
            result_obs = env.execute_action(action)
            
            # 更新状态
            state.current_obs = result_obs
            env.current_obs = result_obs
            agent.max_score = max(agent.max_score, result_obs.score or 0)

            # 打印游戏状态
            print(f"📊 当前得分：{result_obs.score} | 最高得分：{agent.max_score} | 游戏结束：{result_obs.game_over}")

            # 游戏结束重置
            if result_obs.game_over:
                print("🎮 游戏结束，正在重置...")
                reset_obs = env.execute_action(RefreshGame2048Action())
                state.current_obs = reset_obs
                env.current_obs = reset_obs
                agent.game_over = False
                break

    except Exception as e:
        print(f"\n❌ 游戏执行出错：{e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        agent.stop()
        env.close()
        print("\n✅ 2048游戏环境已关闭")

if __name__ == "__main__":
    main()