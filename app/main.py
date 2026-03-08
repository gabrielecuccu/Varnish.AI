import os
import sys
from PySide6 import QtCore, QtWidgets
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError
from app.main_widget import MainWidget

load_dotenv()
openaiApiKey = os.getenv("OPENAI_API_KEY")
ai_client = OpenAI(api_key=openaiApiKey)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWidget(ai_client)
    widget.resize(800, 600)
    widget.setWindowTitle("Varnish.AI - varnish my writing")
    widget.show()

    sys.exit(app.exec())
