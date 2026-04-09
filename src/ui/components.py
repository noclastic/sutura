from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
import os

class DragDropArea(QFrame):
    files_dropped = Signal(list)
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DropArea")
        self.setAcceptDrops(True)
        self.setMinimumHeight(80)
        self.setMaximumHeight(100)

        layout = QHBoxLayout()
        self.label = QLabel("Arrastra PDFs aquí o pulsa para añadir")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #64748B; font-size: 13px; background: transparent; font-weight: 500;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet("border-color: #3B82F6; background-color: #EFF6FF;")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("")

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".pdf"):
                files.append(file_path)
        
        self.setStyleSheet("")
        if files:
            self.files_dropped.emit(files)
        event.accept()

    def mousePressEvent(self, event):
        # Allow clicking as well
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
