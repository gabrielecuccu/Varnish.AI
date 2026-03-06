from app.main import MyWidget
from app.widgets import HintTextEdit
import app.constants
from PySide6.QtCore import Qt
from PySide6 import QtWidgets


def test_initial_state(qtbot):
    widget = MyWidget()

    qtbot.addWidget(widget)

    # Check that comboboxes are enabled
    check_combo_box(widget.iamCombo, True)
    check_combo_box(widget.recipientsCombo, True)
    check_combo_box(widget.msgLevelCombo, True)
    check_combo_box(widget.msgTypeCombo, True)
    check_combo_box(widget.toneCombo, True)

    # Check that buttons are presents but not enabled
    check_button(widget.varnishButton, False)
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


def test_writing_text(qtbot):
    widget = MyWidget()

    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitExposed(widget)

    # Write something in the text area
    widget.inputTextEdit.setFocus()
    qtbot.keyClicks(widget.inputTextEdit, "Hello Varnish!")
    assert widget.inputTextEdit.toPlainText() == "Hello Varnish!"

    # Check that comboboxes are still enabled
    check_combo_box(widget.iamCombo, True)
    check_combo_box(widget.recipientsCombo, True)
    check_combo_box(widget.msgLevelCombo, True)
    check_combo_box(widget.msgTypeCombo, True)
    check_combo_box(widget.toneCombo, True)

    # Check that buttons are still presents with correct enable state
    check_button(widget.varnishButton, True)
    check_button(widget.cleanButton, True)
    check_button(widget.copyButton, False)

    # Check that the status bar is present, enabled and with the initial text
    check_label(widget.statusBar, True, app.constants.statusBarMessages["initial"])

    # Check that the progress bar is present, enabled and in the idle state
    check_progress_bar(widget.progressBar, True, 0, 100)

    check_text_area(
        text_area=widget.inputTextEdit,
        enabled=True,
        readOnly=False,
        text="Hello Varnish!",
        hint="Write something here",
    )
    check_text_area(
        text_area=widget.outputTextEdit, enabled=True, readOnly=True, text="", hint=""
    )


def test_varnishing(qtbot):
    widget = MyWidget()

    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitExposed(widget)

    # Write something in the text area
    widget.inputTextEdit.setFocus()
    qtbot.keyClicks(widget.inputTextEdit, "Hello Varnish!")
    assert widget.inputTextEdit.toPlainText() == "Hello Varnish!"

    # Click the Varnish button
    qtbot.mouseClick(widget.varnishButton, Qt.MouseButton.LeftButton)
    qtbot.wait(2000)

    # Check that comboboxes are no longer enabled
    check_combo_box(widget.iamCombo, False)
    check_combo_box(widget.recipientsCombo, False)
    check_combo_box(widget.msgLevelCombo, False)
    check_combo_box(widget.msgTypeCombo, False)
    check_combo_box(widget.toneCombo, False)

    # Check that buttons are still presents but not enabled
    check_button(widget.varnishButton, False)
    check_button(widget.cleanButton, False)
    check_button(widget.copyButton, False)

    # Check that the status bar is present, enabled and with the initial text
    check_label(widget.statusBar, True, app.constants.statusBarMessages["varnishing"])

    # Check that the progress bar is present, enabled and in progress state
    check_progress_bar(widget.progressBar, True, 0, 0)

    check_text_area(
        text_area=widget.inputTextEdit,
        enabled=False,
        readOnly=False,
        text="Hello Varnish!",
        hint="Write something here",
    )
    check_text_area(
        text_area=widget.outputTextEdit, enabled=True, readOnly=True, text="", hint=""
    )

    with qtbot.waitSignal(widget.worker.finished, timeout=50000):
        pass

    # Check that comboboxes are enabled
    check_combo_box(widget.iamCombo, True)
    check_combo_box(widget.recipientsCombo, True)
    check_combo_box(widget.msgLevelCombo, True)
    check_combo_box(widget.msgTypeCombo, True)
    check_combo_box(widget.toneCombo, True)

    # Check that buttons are still presents and enabled
    check_button(widget.varnishButton, True)
    check_button(widget.cleanButton, True)
    check_button(widget.copyButton, True)

    # Check that the status bar is present, enabled and with the initial text
    check_label(widget.statusBar, True, app.constants.statusBarMessages["initial"])

    # Check that the progress bar is present, enabled and in idle state
    check_progress_bar(widget.progressBar, True, 0, 100)


def check_button(button, enabled):
    assert button is not None
    assert isinstance(button, QtWidgets.QPushButton)
    assert enabled == button.isEnabled()


def check_combo_box(combo, enabled):
    assert combo is not None
    assert isinstance(combo, QtWidgets.QComboBox)
    assert enabled == combo.isEnabled()


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
