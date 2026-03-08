from app.widgets import HintTextEdit


def test_hint_text_initialization(qtbot):
    """Verify the hint text is stored correctly."""
    hint = "Type your message here..."
    widget = HintTextEdit(hint_text=hint)
    qtbot.addWidget(widget)

    assert widget.hint_text == hint
    assert widget.toPlainText() == ""


def test_hint_text_rendering_logic(qtbot):
    """
    Since we can't easily test the painter output, we verify
    the widget state triggers the paintEvent without errors.
    """
    widget = HintTextEdit(hint_text="Hint")
    qtbot.addWidget(widget)
    widget.show()

    # 1. Test empty state (Hint should be visible)
    # This force-triggers a paint event to ensure no crashes
    widget.repaint()
    assert widget.toPlainText() == ""

    # 2. Test with text (Hint should NOT be drawn)
    qtbot.keyClicks(widget, "Hello Varnish")
    widget.repaint()
    assert widget.toPlainText() == "Hello Varnish"


def test_hint_text_clearing(qtbot):
    """Verify that clearing the text brings the widget back to the 'hint' state."""
    widget = HintTextEdit(hint_text="Placeholder")
    qtbot.addWidget(widget)

    # Type something
    qtbot.keyClicks(widget, "Temporary text")
    assert widget.toPlainText() != ""

    # Clear it
    widget.clear()

    # After clearing, the internal condition for painting the hint
    # (toPlainText() == "") will be true again.
    assert widget.toPlainText() == ""
