import pytest
import unittest.mock as mock

with mock.patch.dict('sys.modules', {'pygetwindow': mock.MagicMock()}):
    from capture.window_manager import WindowManager

with mock.patch.dict('sys.modules', {'mss': mock.MagicMock()}):
    from capture.screen_capture import ScreenCapture

def test_window_manager_init():
    wm = WindowManager()
    assert wm.target_window is None

def test_screen_capture_init():
    sc = ScreenCapture()
    assert sc.sct is not None
