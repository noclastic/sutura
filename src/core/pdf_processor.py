import os
from pypdf import PdfReader, PdfWriter
from PySide6.QtCore import QObject, Signal, QThread
from src.utils.logger import logger

class PDFMergeThread(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, pdf_list, output_path):
        super().__init__()
        self.pdf_list = pdf_list
        self.output_path = output_path

    def run(self):
        try:
            writer = PdfWriter()
            total_pages = 0
            current_page = 0

            # Calculate total pages for progress bar
            for pdf_path in self.pdf_list:
                try:
                    reader = PdfReader(pdf_path)
                    total_pages += len(reader.pages)
                except Exception as e:
                    self.error.emit(f"No se pudo leer {os.path.basename(pdf_path)}: {str(e)}")
                    return

            if total_pages == 0:
                self.error.emit("No hay páginas para fusionar.")
                return

            for pdf_path in self.pdf_list:
                reader = PdfReader(pdf_path)
                
                # Check for encryption
                if reader.is_encrypted:
                    logger.warning(f"Archivo protegido: {os.path.basename(pdf_path)}")
                    # For now, we omit it or warn. A real app would ask for password.
                    # Simplification: we expect non-protected or handled via skill instructions if needed.
                    # In this generic tool, we will just try to read or emit error.

                for page in reader.pages:
                    writer.add_page(page)
                    current_page += 1
                    self.progress.emit(int((current_page / total_pages) * 100))

            with open(self.output_path, "wb") as output_file:
                writer.write(output_file)

            self.finished.emit(self.output_path)
        except Exception as e:
            logger.error(f"Error fusionando PDFs: {str(e)}")
            self.error.emit(f"Error crítico: {str(e)}")

def validate_pdf(file_path):
    if not file_path.lower().endswith(".pdf"):
        return False
    try:
        PdfReader(file_path)
        return True
    except Exception:
        return False
