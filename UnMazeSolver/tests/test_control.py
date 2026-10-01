import pytest
import os
import sys

# Mock pyautogui since tests run in headless CI without a display
import unittest.mock as mock

with mock.patch.dict('sys.modules', {'pyautogui': mock.MagicMock()}):
    from control.mouse_controller import MouseController

def test_mouse_controller_init():
    mc = MouseController(click_delay=0.1)
    assert mc.click_delay == 0.1
