import sys
import os
import time
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer
from src.ui.main_window import MainWindow
from src.utils.logger import logger

def ensure_assets():
    """Ensure minimal assets exist to avoid crash if images are missing."""
    os.makedirs("src/assets", exist_ok=True)
    # If icons or splash were not copied correctly, create empty or use system defaults if possible
    # We assumed they were copied via powershell in previous step.

def main():
    app = QApplication(sys.argv)
    
    # El estilo Fusion es excelente para adaptarse al color de acento del sistema
    # y permite que los menús y diálogos no se vean forzados por el QSS.
    app.setStyle("Fusion")
    
    app.setApplicationName("Sutura")
    app.setOrganizationName("PulchraTech Dev")
    
    ensure_assets()

    # Splash Screen
    splash_pix = QPixmap("src/assets/splash.png")
    if splash_pix.isNull():
        # Fallback if splash is missing
        splash_pix = QPixmap(600, 400)
        splash_pix.fill(Qt.white)
    
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
