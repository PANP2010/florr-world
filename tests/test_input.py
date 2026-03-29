"""
测试输入控制系统
"""
import pygame
import pytest
from unittest.mock import patch, MagicMock
from src.input import InputHandler, InputState, _KEY_MAP


@pytest.fixture(autouse=True)
def init_pygame():
    """确保 pygame 已初始化"""
    pygame.init()


@pytest.fixture
def handler():
    return InputHandler()


class MockKeyEvent:
    """模拟 pygame.key.get_pressed 返回"""

    def __init__(self, pressed_keys: set = None):
        self._pressed = pressed_keys or set()

    def __getitem__(self, key_code):
        return key_code in self._pressed


def _mock_pressed(key_codes: list[int]):
    """返回一个模拟的 pressed 数组，只响应 key_codes 中的按键"""
    keys = [0] * 1024
    for k in key_codes:
        if 0 <= k < 1024:
            keys[k] = 1
    return keys


class TestInputState:
    def test_default_state(self):
        state = InputState()
        assert state.left is False
        assert state.right is False
        assert state.up is False
        assert state.down is False
        assert state.space is False
        assert state.escape is False


class TestInputHandlerMovement:
    @patch("pygame.key.get_pressed")
    def test_no_movement_when_idle(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == 0
        assert dy == 0

    @patch("pygame.key.get_pressed")
    def test_move_right(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_d])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == 300
        assert dy == 0

    @patch("pygame.key.get_pressed")
    def test_move_left(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_a])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == -300
        assert dy == 0

    @patch("pygame.key.get_pressed")
    def test_move_up(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_w])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == 0
        assert dy == -300

    @patch("pygame.key.get_pressed")
    def test_move_down(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_s])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == 0
        assert dy == 300

    @patch("pygame.key.get_pressed")
    def test_diagonal_movement(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_d, pygame.K_w])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == 300
        assert dy == -300

    @patch("pygame.key.get_pressed")
    def test_custom_speed(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_d])
        handler.update()
        dx, dy = handler.get_movement(speed=500)
        assert dx == 500

    @patch("pygame.key.get_pressed")
    def test_arrow_keys(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_RIGHT, pygame.K_DOWN])
        handler.update()
        dx, dy = handler.get_movement()
        assert dx == 300
        assert dy == 300


class TestPhaseState:
    @patch("pygame.key.get_pressed")
    def test_space_not_pressed(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([])
        handler.update()
        assert not handler.is_phase_just_pressed()

    @patch("pygame.key.get_pressed")
    def test_phase_just_pressed(self, mock_get_pressed, handler):
        # 第一帧按下空格
        mock_get_pressed.return_value = _mock_pressed([pygame.K_SPACE])
        handler.update()
        assert handler.is_phase_just_pressed()
        # 第二帧仍然按住，不应再触发 just_pressed
        mock_get_pressed.return_value = _mock_pressed([pygame.K_SPACE])
        handler.update()
        assert not handler.is_phase_just_pressed()

    @patch("pygame.key.get_pressed")
    def test_phase_released(self, mock_get_pressed, handler):
        # 按下空格
        mock_get_pressed.return_value = _mock_pressed([pygame.K_SPACE])
        handler.update()
        assert handler.is_phase_just_pressed()
        # 松开空格
        mock_get_pressed.return_value = _mock_pressed([])
        handler.update()
        assert not handler.is_phase_just_pressed()
        assert "space" in handler.just_released


class TestEscapeState:
    @patch("pygame.key.get_pressed")
    def test_escape_just_pressed(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_ESCAPE])
        handler.update()
        assert handler.is_escape_just_pressed()

    @patch("pygame.key.get_pressed")
    def test_escape_held(self, mock_get_pressed, handler):
        mock_get_pressed.return_value = _mock_pressed([pygame.K_ESCAPE])
        handler.update()
        assert handler.is_escape_just_pressed()
        mock_get_pressed.return_value = _mock_pressed([pygame.K_ESCAPE])
        handler.update()
        assert not handler.is_escape_just_pressed()
