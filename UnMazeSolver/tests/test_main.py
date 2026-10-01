import pytest
import os
import sys

def test_main_imports():
    # PyGetWindow doesn't support Linux, so we mock it along with pyautogui for testing
    import unittest.mock as mock
    with mock.patch.dict('sys.modules', {'pyautogui': mock.MagicMock(), 'pygetwindow': mock.MagicMock()}):
        try:
            import main
            assert hasattr(main, 'main')
        except Exception as e:
            pytest.fail(f"main.py import failed: {e}")
