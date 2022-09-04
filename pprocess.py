from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
import sys
import re


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.p = None

        self.btn = QPushButton("Execute")
        self.button =QPushButton("sendData")
        self.btn.pressed.connect(self.start_process)
        self.button.pressed.connect(self.sendData)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.button)
        l.addWidget(self.text)


        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)
    def sendData(self):
        
        self.p.write("b main")
    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("gdb", ['./simple_program'])
            #self.p.setProgram("gdb")
            # self.p.setArguments(['./simple_program'])
            # self.p.start()

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()
