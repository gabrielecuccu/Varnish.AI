from app.main import MyWidget
from app.widgets import HintTextEdit
import app.constants
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

    # Check that the status bar is present, enabled and with the initial text
    check_label(widget.statusBar, True, app.constants.statusBarMessages["initial"])

    # Check that the progress bar is present, enabled and in the idle state
    check_progress_bar(widget.progressBar, True, 0, 100)

    check_text_area(
        text_area=widget.inputTextEdit,
        enabled=True,
        readOnly=False,
        text="",
        hint="Write something here",
    )
    check_text_area(
        text_area=widget.outputTextEdit, enabled=True, readOnly=True, text="", hint=""
    )


def check_button(button, enabled):
    assert button is not None
    assert isinstance(button, QtWidgets.QPushButton)
    assert enabled == button.isEnabled()


def check_label(label, enabled, text):
    assert label is not None
    assert isinstance(label, QtWidgets.QLabel)
    assert enabled == label.isEnabled()
    assert label.text() == text


def check_progress_bar(progress_bar, enabled, minimum, maximum):
    assert progress_bar is not None
    assert isinstance(progress_bar, QtWidgets.QProgressBar)
    assert enabled == progress_bar.isEnabled()
    assert (
        progress_bar.minimum() == minimum
    ), f"Expected min {minimum}, got {progress_bar.minimum()}"
    assert (
        progress_bar.maximum() == maximum
    ), f"Expected max {maximum}, got {progress_bar.maximum()}"


def check_text_area(text_area, enabled, readOnly, text, hint):
    assert text_area is not None
    assert isinstance(text_area, QtWidgets.QPlainTextEdit)
    assert enabled == text_area.isEnabled()
    assert readOnly == text_area.isReadOnly()
    assert text_area.toPlainText() == text
    if isinstance(text_area, HintTextEdit):
        assert text_area.hint_text == hint
