from PySide6 import QtCore, QtWidgets, QtGui


class HintTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, hint_text="", parent=None):
        super().__init__(parent)
        self.hint_text = hint_text

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.toPlainText() == "":
            painter = QtGui.QPainter(self.viewport())
            painter.setPen(QtGui.QColor("gray"))
            painter.setFont(self.font())
            margin = self.document().documentMargin()
            painter.drawText(
                self.viewport().rect().adjusted(int(margin), int(margin), 0, 0),
                QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft,
                self.hint_text,
            )
