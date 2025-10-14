import os
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError
from constants import actors, messageTypes, levels, tones, statusBarMessages
from worker import Worker
from widgets import HintTextEdit

load_dotenv()
openaiApiKey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = openaiApiKey)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(self.initHeaderLayout(), 0)
        layout.addLayout(self.initCentralLayout(), 1)
        layout.addLayout(self.initFooterLayout(), 0)
        
        self.setLayout(layout)
            
    def checkConnection(self):
        try:
            client.models.list()  # Lightweight check
        except AuthenticationError:
            self.showError("Error", "Authentication error", True)
        except APIConnectionError:
            self.showError("Error", "Connection error", True)
        
    def showError(self, title, error, terminate):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(error)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)

        # Modal dialog — blocks until user responds
        msg.exec()
        
        if terminate == True:
            QtWidgets.QApplication.quit()
        else:
            self.progressBar.setRange(0, 100)
            self.enableUI(True)
        
    def initHeaderLayout(self):
        iamLayout, self.iamCombo = self.initComboBoxLayout("I am a:", actors)
        recipientLayout, self.recipientsCombo = self.initComboBoxLayout("I am writing to a:", actors)
        msgLevelLayout, self.msgLevelCombo = self.initComboBoxLayout("Level:", levels)
        msgTypeLayout, self.msgTypeCombo = self.initComboBoxLayout("Polish my:", messageTypes)
        toneLayout, self.toneCombo = self.initComboBoxLayout("Keeping the tone:", tones)
        
        headerLayout = QtWidgets.QHBoxLayout()
        headerLayout.addLayout(iamLayout)
        headerLayout.addLayout(recipientLayout)
        headerLayout.addLayout(msgLevelLayout)
        headerLayout.addLayout(msgTypeLayout)
        headerLayout.addLayout(toneLayout)
        
        return headerLayout
    
    def initCentralLayout(self):
        centralLayout = QtWidgets.QHBoxLayout()
        
        self.inputTextEdit = HintTextEdit("Write something here")
        centralLayout.addWidget(self.inputTextEdit)
        
        buttonsLayout = self.initButtonsLayout()
        centralLayout.addLayout(buttonsLayout)
        
        self.outputTextEdit = QtWidgets.QPlainTextEdit()
        self.outputTextEdit.setReadOnly(True)
        centralLayout.addWidget(self.outputTextEdit)
        
        self.inputTextEdit.textChanged.connect(self.textHasChanged)
        self.outputTextEdit.textChanged.connect(self.textHasChanged)
        
        return centralLayout
    
    def initButtonsLayout(self):
        buttonsLayout = QtWidgets.QVBoxLayout()
        
        self.polishButton = QtWidgets.QPushButton("Polish")
        self.polishButton.setEnabled(False)
        self.polishButton.clicked.connect(self.polishClicked)
        buttonsLayout.addWidget(self.polishButton)
        
        self.cleanButton = QtWidgets.QPushButton("Clean")
        self.cleanButton.setEnabled(False)
        self.cleanButton.clicked.connect(self.cleanClicked)
        buttonsLayout.addWidget(self.cleanButton)
        
        self.copyButton = QtWidgets.QPushButton("Copy")
        self.copyButton.setEnabled(False)
        self.copyButton.clicked.connect(self.copyClicked)
        buttonsLayout.addWidget(self.copyButton)
        
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        buttonsLayout.addSpacerItem(spacer)
        
        return buttonsLayout
    
    def initFooterLayout(self):
        footerLayout = QtWidgets.QVBoxLayout()
        
        self.progressBar = QtWidgets.QProgressBar()
        footerLayout.addWidget(self.progressBar)
        
        self.statusBar = QtWidgets.QLabel(statusBarMessages["initial"])
        footerLayout.addWidget(self.statusBar)
        
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
    
    def textHasChanged(self):
        inputText = self.inputTextEdit.toPlainText()
        outputText = self.outputTextEdit.toPlainText()
        
        self.polishButton.setEnabled(inputText != "")
        self.cleanButton.setEnabled(inputText != "" or outputText != "")
        self.copyButton.setEnabled(outputText != "")
    
    @QtCore.Slot()
    def polishClicked(self):
        self.outputTextEdit.setPlainText("")
        self.statusBar.setText(statusBarMessages["polishing"])
        iam = self.iamCombo.currentText()
        recipient = self.recipientsCombo.currentText()
        level = self.msgLevelCombo.currentText()
        msgType = self.msgTypeCombo.currentText()
        tone = self.toneCombo.currentText()
        userMessage = self.inputTextEdit.toPlainText()
        prompt = f"I am a {iam}, I am writing to a {recipient}, polish {level} the following {msgType} keeping the tone {tone}"
        
        self.enableUI(False)
        self.progressBar.setRange(0, 0)
        
        self.thread = QtCore.QThread()
        self.worker = Worker(client, prompt, userMessage)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.partial.connect(self.partialReplyAvailable)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.showError)
        self.thread.start()
        
    @QtCore.Slot()
    def cleanClicked(self):
        self.inputTextEdit.setPlainText("")
        self.outputTextEdit.setPlainText("")
    
    @QtCore.Slot()
    def copyClicked(self):
        cursor = self.outputTextEdit.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            QtWidgets.QApplication.clipboard().setText(selected_text)
        else:
            full_text = self.outputTextEdit.toPlainText()
            QtWidgets.QApplication.clipboard().setText(full_text)
        
    def partialReplyAvailable(self, partialText):
        self.outputTextEdit.moveCursor(QtGui.QTextCursor.End)
        self.outputTextEdit.insertPlainText(partialText)
        self.outputTextEdit.ensureCursorVisible() 
        self.enableUI(True)
        self.progressBar.setRange(0, 100)
        self.statusBar.setText(statusBarMessages["initial"])
        
    def enableUI(self, enabled):
        self.polishButton.setEnabled(enabled)
        self.cleanButton.setEnabled(enabled)
        self.iamCombo.setEnabled(enabled)
        self.recipientsCombo.setEnabled(enabled)
        self.msgLevelCombo.setEnabled(enabled)
        self.msgTypeCombo.setEnabled(enabled)
        self.toneCombo.setEnabled(enabled)
        self.inputTextEdit.setEnabled(enabled)        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setWindowTitle("Polish my writing")
    widget.show()
    
    QtCore.QTimer.singleShot(0, widget.checkConnection)

    sys.exit(app.exec())
    
    
