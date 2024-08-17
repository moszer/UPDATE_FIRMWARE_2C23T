import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QProgressBar, QWidget, QLabel, QFileDialog, QPlainTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class SlowFileCopyThread(QThread):
    progress = pyqtSignal(int)
    hex_log = pyqtSignal(str)

    def __init__(self, source_file, destination_file):
        super().__init__()
        self.source_file = source_file
        self.destination_file = destination_file

    def run(self):
        total_size = os.path.getsize(self.source_file)
        copied_size = 0
        buffer_size = 64 * 64  # 4096 bytes
        delay = 0.1  # 100ms delay to slow down the copy

        with open(self.source_file, 'rb') as src, open(self.destination_file, 'wb') as dst:
            while True:
                buffer = src.read(buffer_size)
                if not buffer:
                    break
                dst.write(buffer)
                copied_size += len(buffer)
                progress_percent = int((copied_size / total_size) * 100)
                self.progress.emit(progress_percent)
                hex_representation = ' '.join(f'{byte:02x}' for byte in buffer)
                self.hex_log.emit(hex_representation)
                time.sleep(delay)  # Introduce delay to slow down the copy process

class FileCopyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slow File Copy with Progress")
        self.setGeometry(100, 100, 600, 400)  # Increased window size

        self.source_file = None
        self.destination_file = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Select a file and destination to start copying", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.select_file_button = QPushButton("Select File", self)
        self.select_file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_button)

        self.select_dest_button = QPushButton("Select Destination", self)
        self.select_dest_button.clicked.connect(self.select_destination)
        self.layout.addWidget(self.select_dest_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)

        self.copy_button = QPushButton("Copy File", self)
        self.copy_button.clicked.connect(self.copy_file)
        self.layout.addWidget(self.copy_button)

        self.hex_log_edit = QPlainTextEdit(self)
        self.hex_log_edit.setReadOnly(True)
        self.hex_log_edit.setMaximumHeight(150)
        self.layout.addWidget(self.hex_log_edit)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Source File", "", "All Files (*);;Bin Files (*.bin)", options=options)
        if file_name:
            self.source_file = file_name
            self.label.setText(f"Selected file: {self.source_file}")

    def select_destination(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory", "", options=options)
        if directory:
            self.destination_file = os.path.join(directory, os.path.basename(self.source_file))
            self.label.setText(f"Selected destination: {self.destination_file}")

    def copy_file(self):
        if self.source_file and self.destination_file:
            self.thread = SlowFileCopyThread(self.source_file, self.destination_file)
            self.thread.progress.connect(self.update_progress)
            self.thread.hex_log.connect(self.update_hex_log)
            self.thread.finished.connect(self.on_finished)
            self.thread.start()
        else:
            self.label.setText("Please select a source file and destination directory.")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_hex_log(self, hex_data):
        self.hex_log_edit.appendPlainText(hex_data)

    def on_finished(self):
        self.label.setText("File copy completed!")
        self.progress_bar.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCopyApp()
    window.show()
    sys.exit(app.exec_())
