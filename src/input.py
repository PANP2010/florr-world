"""
InputHandler - 输入控制系统
支持：键盘WASD、鼠标、方向键、空格（相位态）
"""
import pygame
from dataclasses import dataclass, field
from typing import Set

# pygame 需要初始化才能使用
pygame.init()


@dataclass
class InputState:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False
    space: bool = False  # 相位态
    escape: bool = False


# 按键到方向状态的映射
_KEY_MAP = {
    pygame.K_LEFT: "left",
    pygame.K_a: "left",
    pygame.K_RIGHT: "right",
    pygame.K_d: "right",
    pygame.K_UP: "up",
    pygame.K_w: "up",
    pygame.K_DOWN: "down",
    pygame.K_s: "down",
    pygame.K_SPACE: "space",
    pygame.K_ESCAPE: "escape",
}

# 相位态按键
_PHASE_KEYS = {pygame.K_SPACE}


class InputHandler:
    """
    输入控制器，支持：
    - 键盘 WASD / 方向键
    - 空格（相位态）
    - ESC
    """

    def __init__(self):
        self.state = InputState()
        self.just_pressed: Set[str] = set()
        self.just_released: Set[str] = set()
        self._prev_keys: Set[int] = set()

    def update(self):
        """每帧调用，检测按键的按下/松开状态"""
        self.just_pressed.clear()
        self.just_released.clear()

        keys = pygame.key.get_pressed()
        current_keys = {k for k, pressed in enumerate(keys) if pressed}
        pressed_keys = current_keys - self._prev_keys
        released_keys = self._prev_keys - current_keys

        # 重置所有方向状态
        self.state.left = False
        self.state.right = False
        self.state.up = False
        self.state.down = False
        self.state.space = False
        self.state.escape = False

        # 应用当前按下的按键
        for key_code in current_keys:
            direction = _KEY_MAP.get(key_code)
            if direction:
                setattr(self.state, direction, True)

        # 记录 just_pressed / just_released
        for key_code in pressed_keys:
            direction = _KEY_MAP.get(key_code)
            if direction:
                self.just_pressed.add(direction)

        for key_code in released_keys:
            direction = _KEY_MAP.get(key_code)
            if direction:
                self.just_released.add(direction)

        self._prev_keys = current_keys

    def get_movement(self, speed: float = 300.0) -> tuple:
        """
        返回 (dx, dy) 移动向量，单位：像素/秒
        speed 参数可调整默认移动速度
        """
        dx = (self.state.right - self.state.left) * speed
        dy = (self.state.down - self.state.up) * speed
        return (dx, dy)

    def is_phase_just_pressed(self) -> bool:
        """相位态是否刚刚触发"""
        return "space" in self.just_pressed

    def is_escape_just_pressed(self) -> bool:
        """ESC 是否刚刚触发"""
        return "escape" in self.just_pressed
