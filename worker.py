from PySide6 import QtCore
from openai import APIConnectionError


class Worker(QtCore.QObject):
    finished = QtCore.Signal()
    partial = QtCore.Signal(object)
    error = QtCore.Signal(object, object, bool)

    def __init__(self, client, prompt, userMessage, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.userMessage = userMessage
        self.client = client

    def run(self):
        try:
            with self.client.responses.stream(
                model="gpt-5",
                reasoning={"effort": "low"},
                instructions=self.prompt,
                input=self.userMessage,
            ) as stream:
                for event in stream:
                    if event.type == "response.output_text.delta":
                        self.partial.emit(event.delta)

                self.finished.emit()
        except APIConnectionError:
            self.error.emit("Error", "Connection error", False)
            self.finished.emit()
        except Exception as e:
            self.error.emit("Error", f"Unexpected error: {e}", False)
            self.finished.emit()
