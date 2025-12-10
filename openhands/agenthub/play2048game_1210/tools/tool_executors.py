# env/tool_executors.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def init_browser(headless: bool = False, game_url: str = "https://www.2048.org/") -> webdriver.Chrome:
    """初始化浏览器"""
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36')
    if headless:
        chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(game_url)

    # 等待页面加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'game-container')]"))
    )
    time.sleep(2)

    return driver

def press_key(driver: webdriver.Chrome, direction: str) -> bool:
    """按下方向键"""
    direction_keys = {
        "up": Keys.ARROW_UP,
        "down": Keys.ARROW_DOWN,
        "left": Keys.ARROW_LEFT,
        "right": Keys.ARROW_RIGHT,
    }
    if direction not in direction_keys:
        return False

    try:
        driver.find_element(By.TAG_NAME, "body").click()
        driver.switch_to.active_element.send_keys(direction_keys[direction])
        time.sleep(0.5)
        return True
    except Exception:
        return False

def get_game_state(driver: webdriver.Chrome) -> tuple[int, list[list[int]], bool]:
    """获取游戏状态"""
    # 解析分数
    try:
        score_elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "score-container"))
        )
        score_text = driver.execute_script("return arguments[0].innerText;", score_elem).strip()
        score_text = score_text.split("\n")[0].replace(",", "")
        score = int(score_text) if score_text.isdigit() else 0
    except Exception:
        score = 0

    # 解析棋盘
    board = [[0]*4 for _ in range(4)]
    try:
        tile_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tile-container"))
        )
        tiles = tile_container.find_elements(By.CLASS_NAME, "tile")
        
        for tile in tiles:
            tile_class = driver.execute_script("return arguments[0].className;", tile)
            pos_classes = [c for c in tile_class.split() if "tile-position-" in c]
            if not pos_classes:
                continue
            pos_parts = pos_classes[0].split("-")
            if len(pos_parts) != 4:
                continue
            col = int(pos_parts[2]) - 1
            row = int(pos_parts[3]) - 1
            val_classes = [c for c in tile_class.split() if c.startswith("tile-") and not c.startswith("tile-position-")]
            if not val_classes:
                continue
            val = int(val_classes[0].split("-")[1])
            if 0 <= row < 4 and 0 <= col < 4:
                board[row][col] = val
    except Exception:
        pass

    # 检查游戏结束
    game_over = False
    try:
        driver.find_element(By.CLASS_NAME, "game-over")
        game_over = True
    except NoSuchElementException:
        pass

    return score, board, game_over

def refresh_game(driver: webdriver.Chrome) -> bool:
    """重置游戏"""
    try:
        new_game_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "New Game"))
        )
        new_game_btn.click()
        time.sleep(2)
        driver.execute_script("window.location.reload()")
        time.sleep(1)
        return True
    except Exception:
        return False

def close_browser(driver: webdriver.Chrome):
    """关闭浏览器"""
    driver.quit()