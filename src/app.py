import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QWidget, QMessageBox, QComboBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from menubar import Menubar
from conexion import register_data, get_user_role  # Usamos funciones modularizadas

# Ajustar el directorio de trabajo al directorio donde está ubicado el archivo app.py
if getattr(sys, 'frozen', False):
    # Si es un ejecutable generado (por ejemplo, con PyInstaller)
    script_dir = os.path.dirname(sys.executable)
else:
    # Si es un archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)
print(f"Directorio de trabajo actualizado a: {os.getcwd()}")

# Ventana de Registro
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuarios")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Agregar la imagen en la parte superior
        self.label_image = QLabel()
        image_path = os.path.join(os.path.dirname(os.getcwd()),"uleam.png")
        if not os.path.exists(image_path):
            print(f"Error: La imagen no existe en la ruta: {image_path}")
        else:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print("Error: La imagen no se cargó correctamente.")
            else:
                self.label_image.setPixmap(pixmap.scaled(100, 100))
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_image)

        self.label_username = QLabel("Nombre de Usuario:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Contraseña:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.label_role = QLabel("Rol:")
        self.combo_role = QComboBox()
        self.combo_role.addItems(["admin", "estudiante", "docente"])
        layout.addWidget(self.label_role)
        layout.addWidget(self.combo_role)

        self.button_register = QPushButton("Registrar")
        self.button_register.clicked.connect(self.register_data)
        layout.addWidget(self.button_register)

        self.button_to_login = QPushButton("Ir a Login")
        self.button_to_login.clicked.connect(self.go_to_login)
        layout.addWidget(self.button_to_login)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def register_data(self):
        username = self.input_username.text()
        password = self.input_password.text()
        role = self.combo_role.currentText()

        if not username or not password or not role:  # Verifica que todos los campos estén llenos
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        # Crear el diccionario con los datos que se van a insertar
        data = {
            'username': username,
            'password': password,
            'user_role': role
        }

        # Llama a la función modularizada que guarda los datos en la base de datos
        register_data('evaluacionesTI.usuarios', data)

        QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
        self.input_username.clear()
        self.input_password.clear()

    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# Ventana de Login
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ingreso")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Agregar la imagen en la parte superior
        self.label_image = QLabel()
        image_path = os.path.join(os.path.dirname(os.getcwd()),"uleam.png")
        if not os.path.exists(image_path):
            print(f"Error: La imagen no existe en la ruta: {image_path}")
        else:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print("Error: La imagen no se cargó correctamente.")
            else:
                self.label_image.setPixmap(pixmap.scaled(100, 100))
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_image)

        self.label_username = QLabel("Nombre de Usuario:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Contraseña:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Iniciar Sesión")
        self.button_login.clicked.connect(self.login_user)
        layout.addWidget(self.button_login)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login_user(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        user_role = get_user_role(username, password)  # Llamada modularizada
        if user_role:
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
            self.main_window = MainWindow(user_role)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Credenciales incorrectas.")

# Ventana principal con Menú
class MainWindow(QMainWindow, Menubar):
    def __init__(self, user_role):
        super().__init__()
        self.user_role = user_role  # Guardamos el rol del usuario
        self.setupUi(self)
        self.configure_menubar()  # Configuramos el Menubar según el rol

    def configure_menubar(self):
        if self.user_role != "admin":
            # Desactivamos las opciones que no son de consulta o actualización
            self.menuRegistrar.setDisabled(True)
            self.menuReporte.setDisabled(True)

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    register_window = RegisterWindow()  # Crear la ventana de registro
    register_window.show()  # Mostrar la ventana de registro
    sys.exit(app.exec_())
