import sys
from PySide6 import QtWidgets
from app.main_widget import MainWidget
from app.gpt import init_ai_client

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    ai_client = init_ai_client()
    widget = MainWidget(ai_client)
    widget.resize(800, 600)
    widget.setWindowTitle("Varnish.AI - varnish my writing")
    widget.show()

    sys.exit(app.exec())
