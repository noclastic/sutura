import sys
import os
import time
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QIcon, QPainter, QFont, QColor, QLinearGradient
from PySide6.QtCore import Qt, QTimer
from src.ui.main_window import MainWindow
from src.utils.logger import logger
from src.utils.resource_path import get_resource_path

def ensure_assets():
    """Ensure minimal assets exist to avoid crash if images are missing."""
    # When bundled, we don't want to try to create folders inside the internal structure
    # This function is mostly for dev mode now.
    pass

def main():
    app = QApplication(sys.argv)
    
    # El estilo Fusion es excelente para adaptarse al color de acento del sistema
    # y permite que los menús y diálogos no se vean forzados por el QSS.
    app.setStyle("Fusion")
    
    app.setApplicationName("Sutura")
    app.setOrganizationName("PulchraTech Dev")
    
    ensure_assets()

    # Splash Screen programático (Sutura)
    splash_pix = QPixmap(600, 400)
    splash_pix.fill(Qt.transparent)
    
    painter = QPainter(splash_pix)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Fondo con degradado
    grad = QLinearGradient(0, 0, 600, 400)
    grad.setColorAt(0, QColor("#1e293b"))
    grad.setColorAt(1, QColor("#0f172a"))
    painter.fillRect(0, 0, 600, 400, grad)
    
    # Texto principal
    painter.setPen(QColor("#38bdf8"))
    font = QFont("Arial", 50, QFont.Bold)
    painter.setFont(font)
    painter.drawText(splash_pix.rect(), Qt.AlignCenter, "SUTURA")
    
    # Subtítulo
    painter.setPen(QColor("#94a3b8"))
    font_sub = QFont("Arial", 16)
    painter.setFont(font_sub)
    painter.drawText(0, 260, 600, 50, Qt.AlignCenter, "Fusionador de PDFs Profesional")
    
    painter.end()
    
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    
    # Optional message on splash
    splash.showMessage("Cargando sutura...", Qt.AlignBottom | Qt.AlignCenter, Qt.gray)
    
    # Process events to show splash
    app.processEvents()
    
    # Wait a bit to show splash (aesthetic choice for a modern feel)
    time.sleep(1.5)

    window = MainWindow()
    window.show()
    
    splash.finish(window)
    
    logger.info("Aplicación Sutura iniciada correctamente.")
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Error fatal al iniciar la aplicación: {str(e)}")
        sys.exit(1)
