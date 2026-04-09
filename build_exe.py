import subprocess
import sys
import os

def build():
    print("Iniciando proceso de empaquetado para Sutura...")
    
    # Asegurarse de que PyInstaller está instalado
    try:
        import PyInstaller
        print("PyInstaller detectado.")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Comando para construir usando el archivo .spec
    # Usamos python -m PyInstaller para ser más robustos en Windows
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "Sutura.spec"
    ]
    
    print(f"Ejecutando: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print("ÉXITO: Aplicación empaquetada correctamente.")
        print("El archivo ejecutable se encuentra en: dist/Sutura.exe")
        print("="*50)
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Falló el proceso de empaquetado. {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
