import os
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
openaiApiKey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = openaiApiKey)

class Worker(QtCore.QObject):
    finished = QtCore.Signal(object)
    
    def __init__(self, prompt, userMessage, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.userMessage = userMessage

    def run(self):
        response = client.responses.create(
            model="gpt-5",
            reasoning={"effort": "low"},
            instructions=self.prompt,
            input=self.userMessage,
        )
        
        self.finished.emit(response.output_text)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(self.initHeaderLayout(), 0)
        layout.addLayout(self.initCentralLayout(), 1)
        layout.addLayout(self.initFooterLayout(), 0)
        
        self.setLayout(layout)
        
    def initHeaderLayout(self):
        iamLayout, self.iamCombo = self.initComboBoxLayout("I am a:", sorted(["software engineer", "person", "student", "friend", "patient", "customer", "neighbour"]))
        recipientLayout, self.recipientsCombo = self.initComboBoxLayout("I am writing to a:", sorted(["software engineer", "person", "student", "friend", "patient", "customer", "neighbour"]))
        msgTypeLayout, self.msgTypeCombo = self.initComboBoxLayout("Polish my:", sorted(["email", "chat", "SMS", "social media post", "comment", "blog post", "article", "letter", "memo"]))
        toneLayout, self.toneCombo = self.initComboBoxLayout("Keeping the tone:", sorted(["plain", "objective", "professional", "technical", "polite", "friendly", "encouraging", "optimistic", "playful", "ironic", "sarcastic", "witty", "poetic", "authoritative", "cautious", "respectful", "sincere", "irritated", "aggressive", "judgmental"]))
        
        headerLayout = QtWidgets.QHBoxLayout()
        headerLayout.addLayout(iamLayout)
        headerLayout.addLayout(recipientLayout)        
        headerLayout.addLayout(msgTypeLayout)
        headerLayout.addLayout(toneLayout)
        
        return headerLayout
    
    def initCentralLayout(self): 
        self.inputTextEdit = QtWidgets.QPlainTextEdit()
        self.outputTextEdit = QtWidgets.QPlainTextEdit()
        self.outputTextEdit.setReadOnly(True)
        textLayout = QtWidgets.QHBoxLayout()
        textLayout.addWidget(self.inputTextEdit)
        textLayout.addWidget(self.outputTextEdit)
        
        return textLayout
    
    def initFooterLayout(self):
        footerLayout = QtWidgets.QHBoxLayout()
        self.progressBar = QtWidgets.QProgressBar()
        self.goButton = QtWidgets.QPushButton("Go")
        self.goButton.clicked.connect(self.goClicked)
        footerLayout.addWidget(self.progressBar, 1)
        footerLayout.addWidget(self.goButton, 0)
        
        return footerLayout
    
    def initComboBoxLayout(self, text, items):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        
        label = QtWidgets.QLabel(text)
        label.setBuddy(combo)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(combo)
        
        return layout, combo
    
    @QtCore.Slot()
    def goClicked(self):
        iam = self.iamCombo.currentText()
        recipient = self.recipientsCombo.currentText()
        msgType = self.msgTypeCombo.currentText()
        tone = self.toneCombo.currentText()
        userMessage = self.inputTextEdit.toPlainText()
        prompt = f"I am a {iam}, I am writing to a {recipient}, polish the following {msgType} keeping the tone {tone}"
        
        self.goButton.setEnabled(False)
        self.iamCombo.setEnabled(False)
        self.recipientsCombo.setEnabled(False)        
        self.msgTypeCombo.setEnabled(False)
        self.toneCombo.setEnabled(False)
        self.inputTextEdit.setEnabled(False)
        self.progressBar.setRange(0, 0)
        
        self.thread = QtCore.QThread()
        self.worker = Worker(prompt, userMessage)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.task_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        
    def task_finished(self, result):
        self.outputTextEdit.setPlainText(result)
        self.goButton.setEnabled(True)
        self.iamCombo.setEnabled(True)
        self.recipientsCombo.setEnabled(True)        
        self.msgTypeCombo.setEnabled(True)
        self.toneCombo.setEnabled(True)
        self.inputTextEdit.setEnabled(True)
        self.progressBar.setRange(0, 100)       

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setWindowTitle("Polish my writing")
    widget.show()

    sys.exit(app.exec())
