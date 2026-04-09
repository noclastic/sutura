import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QListWidgetItem, QFileDialog, 
                             QLabel, QLineEdit, QProgressBar, QMessageBox, QMenu,
                             QApplication, QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from src.ui.components import DragDropArea
from src.core.pdf_processor import PDFMergeThread
from src.utils.config import get_last_folder, set_last_folder
from src.utils.logger import logger, get_log_file_path
from src.utils.resource_path import get_resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sutura - Fusionador de PDFs seguro")
        self.setMinimumSize(850, 650)
        self.setWindowIcon(QIcon(get_resource_path("src/assets/icon.png")))
        
        self.init_ui()
        self.init_menu()
        self._load_styles()

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Left Column: Controls and List
        left_column = QVBoxLayout()

        # Header
        header = QLabel("Sutura")
        header.setObjectName("AppTitle")
        left_column.addWidget(header)
        
        info_label = QLabel("Fusiona, ordena y organiza tus archivos PDF sin conexión.")
        info_label.setStyleSheet("color: #64748B; font-size: 14px; margin-bottom: 20px;")
        left_column.addWidget(info_label)

        # Drag & Drop Area
        self.drop_area = DragDropArea(self)
        self.drop_area.files_dropped.connect(self.add_files)
        self.drop_area.clicked.connect(self._on_add_pdf_clicked)
        left_column.addWidget(self.drop_area)

        # File List Group
        list_layout = QVBoxLayout()
        list_label = QLabel("Archivos a fusionar:")
        list_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        list_layout.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        self.file_list.setDragDropMode(QListWidget.InternalMove)
        self.file_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout.addWidget(self.file_list, stretch=1) # El stretch prioritiza este espacio
        left_column.addLayout(list_layout)

        # Output Section
        output_layout = QVBoxLayout()
        output_layout.setSpacing(10)
        output_layout.setContentsMargins(0, 20, 0, 0)

        # Final Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nombre final:"))
        self.output_name = QLineEdit("documento_fusionado")
        self.output_name.setPlaceholderText("Ej: Informe_Final")
        name_layout.addWidget(self.output_name)
        name_layout.addWidget(QLabel(".pdf"))
        output_layout.addLayout(name_layout)

        # Output Folder
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Carpeta destino:"))
        self.output_folder_path = QLineEdit(get_last_folder())
        folder_layout.addWidget(self.output_folder_path)
        
        self.browse_btn = QPushButton("Cambiar")
        self.browse_btn.setObjectName("SideButton")
        self.browse_btn.clicked.connect(self._on_browse_clicked)
        folder_layout.addWidget(self.browse_btn)
        output_layout.addLayout(folder_layout)

        left_column.addLayout(output_layout)

        # Merge Button
        self.merge_btn = QPushButton("Fusionar PDFs")
        self.merge_btn.setObjectName("MergeButton")
        self.merge_btn.setMinimumHeight(50)
        self.merge_btn.clicked.connect(self._on_merge_clicked)
        left_column.addWidget(self.merge_btn)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_column.addWidget(self.progress_bar)

        # Messages/Status
        self.status_label = QLabel("Listo para trabajar")
        self.status_label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        left_column.addWidget(self.status_label)

        main_layout.addLayout(left_column, 2)

        # Right Column: Side Actions
        right_column = QVBoxLayout()
        right_column.setSpacing(10)
        
        # Spacer top
        right_column.addSpacerItem(QSpacerItem(20, 160, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.add_btn = QPushButton("Añadir PDF")
        self.add_btn.setObjectName("SideButton")
        self.add_btn.clicked.connect(self._on_add_pdf_clicked)
        right_column.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Eliminar")
        self.remove_btn.setObjectName("SideButton")
        self.remove_btn.clicked.connect(self._on_remove_pdf_clicked)
        right_column.addWidget(self.remove_btn)

        right_column.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.up_btn = QPushButton("↑ Subir")
        self.up_btn.setObjectName("SideButton")
        self.up_btn.clicked.connect(self._on_move_up_clicked)
        right_column.addWidget(self.up_btn)

        self.down_btn = QPushButton("↓ Bajar")
        self.down_btn.setObjectName("SideButton")
        self.down_btn.clicked.connect(self._on_move_down_clicked)
        right_column.addWidget(self.down_btn)

        self.clear_btn = QPushButton("Limpiar Todo")
        self.clear_btn.setObjectName("SideButton")
        self.clear_btn.clicked.connect(self.file_list.clear)
        right_column.addWidget(self.clear_btn)

        right_column.addStretch()
        main_layout.addLayout(right_column, 0)

    def init_menu(self):
        menubar = self.menuBar()
        
        # Archivo
        file_menu = menubar.addMenu("Archivo")
        
        open_action = QAction("Añadir PDFs...", self)
        open_action.triggered.connect(self._on_add_pdf_clicked)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Ayuda
        help_menu = menubar.addMenu("Ayuda")
        about_action = QAction("Acerca de Sutura", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        log_action = QAction("Ver Logs de Errores", self)
        log_action.triggered.connect(self._show_logs)
        help_menu.addAction(log_action)

    def _load_styles(self):
        try:
            with open(get_resource_path("src/ui/styles.qss"), "r") as f:
                self.setStyleSheet(f.read())
        except Exception:
            logger.error("No se pudo cargar el archivo QSS")

    # Slots
    def add_files(self, files):
        for f in files:
            # Check for duplicates or validate
            item = QListWidgetItem(os.path.basename(f))
            item.setData(Qt.UserRole, f) # Store absolute path
            self.file_list.addItem(item)
        self.status_label.setText(f"{self.file_list.count()} archivos listos")

    def _on_add_pdf_clicked(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar PDFs", get_last_folder(), "PDF Files (*.pdf)")
        if files:
            set_last_folder(os.path.dirname(files[0]))
            self.output_folder_path.setText(get_last_folder())
            self.add_files(files)

    def _on_remove_pdf_clicked(self):
        current_item = self.file_list.currentItem()
        if current_item:
            self.file_list.takeItem(self.file_list.row(current_item))
            self.status_label.setText(f"{self.file_list.count()} archivos listos")

    def _on_move_up_clicked(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def _on_move_down_clicked(self):
        row = self.file_list.currentRow()
        if row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def _on_browse_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida", self.output_folder_path.text())
        if folder:
            self.output_folder_path.setText(folder)
            set_last_folder(folder)

    def _on_merge_clicked(self):
        file_count = self.file_list.count()
        if file_count < 2:
            QMessageBox.warning(self, "Aviso", "Añade al menos 2 archivos para fusionar.")
            return

        name = self.output_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Introduce un nombre para el archivo final.")
            return

        output_path = os.path.join(self.output_folder_path.text(), f"{name}.pdf")
        
        # Prepare file paths
        pdf_paths = [self.file_list.item(i).data(Qt.UserRole) for i in range(file_count)]

        # Start fusion
        self.merge_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Fusionando archivos...")

        self.merge_thread = PDFMergeThread(pdf_paths, output_path)
        self.merge_thread.progress.connect(self.progress_bar.setValue)
        self.merge_thread.finished.connect(self._on_merge_finished)
        self.merge_thread.error.connect(self._on_merge_error)
        self.merge_thread.start()

    def _on_merge_finished(self, path):
        self.merge_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Fusionado: {os.path.basename(path)}")
        QMessageBox.information(self, "Éxito", f"PDF fusionado correctamente en:\n{path}")
        
        # Open folder
        os.startfile(os.path.dirname(path))

    def _on_merge_error(self, message):
        self.merge_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error en la fusión")
        QMessageBox.critical(self, "Error", f"Ocurrió un error:\n{message}")

    def _show_about(self):
        QMessageBox.about(self, "Acerca de Sutura", 
                        "Sutura versión Alpha\n\nDesarrollado como una alternativa profesional offline para fusionar PDFs.\n\nPulchraTech")

    def _show_logs(self):
        log_path = get_log_file_path()
        if os.path.exists(log_path):
            os.startfile(log_path)
        else:
            QMessageBox.information(self, "Logs", "Todavía no hay registros de errores.")
