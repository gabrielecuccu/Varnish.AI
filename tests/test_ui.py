from app.main import MyWidget
from PySide6.QtCore import Qt
from PySide6 import QtWidgets


def test_initial_state(qtbot):
    widget = MyWidget()

    qtbot.addWidget(widget)

    # Check that comboboxes are clickable
    qtbot.mouseClick(widget.iamCombo, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(widget.recipientsCombo, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(widget.msgLevelCombo, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(widget.msgTypeCombo, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(widget.toneCombo, Qt.MouseButton.LeftButton)

    # Check that buttons are presents but not enabled
    check_button(widget.polishButton, False)
    check_button(widget.cleanButton, False)
    check_button(widget.copyButton, False)


def check_button(button, enabled):
    assert button is not None
    assert isinstance(button, QtWidgets.QPushButton)
    assert enabled == button.isEnabled()
