from PyQt5 import QtCore, QtGui, QtWidgets
from conexion import query_data  # Importar la función
import sys

class consulta11(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 414)
        
        Dialog.setStyleSheet("background-color: #f2f2f2;")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Consultar")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 20, 300, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(40, 100, 301, 22))
        self.lineEdit.setObjectName("lineEdit")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 300, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.consultar_datos)  # Conectar el botón Ok
        self.buttonBox.rejected.connect(Dialog.reject)  # Conectar el botón Cancel
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Consultar Evaluación Estudiante"))
        self.label.setText(_translate("Dialog", "Consultar Evaluación a Estudiante"))
        self.label_2.setText(_translate("Dialog", "ID Estudiante a Consultar:"))

    def consultar_datos(self):
        # Obtener el ID del estudiante desde el campo de texto
        id_estudiante = self.lineEdit.text()

        if not id_estudiante.isdigit():
            QtWidgets.QMessageBox.warning(None, "Error", "Por favor, ingrese un ID de estudiante válido.")
            return

        # Preparar la condición para la consulta
        conditions = f"id_estudiante = {id_estudiante}"

        # Llamar a la función query_data para hacer la consulta en la base de datos
        results = query_data("evaluacionesTI.Detalle_EvaEstudiante", conditions)

        # Consulta adicional para obtener el nombre del estudiante
        nombre_estudiante = self.obtener_nombre_estudiante(id_estudiante)

        # Mostrar los resultados en la interfaz
        if results:
            result_string = f"Nombre del Estudiante: {nombre_estudiante}\n\n"  # Mostrar el nombre del estudiante
            for row in results:
                result_string += f"ID Evaluación Estudiante: {row[0]}\n"
                result_string += f"Nota: {row[1]}\n"
                result_string += f"ID Evaluación Asignada: {row[2]}\n\n"  # Mostrar el ID de evaluación asignada
            QtWidgets.QMessageBox.information(None, "Resultados", f"Resultados encontrados:\n{result_string}")
        else:
            QtWidgets.QMessageBox.information(None, "Resultados", "No se encontraron datos para el ID proporcionado.")

    def obtener_nombre_estudiante(self, id_estudiante):
        """Consulta la base de datos para obtener el nombre del estudiante"""
        try:
            conditions = f"id_estudiante = {id_estudiante}"
            results = query_data("evaluacionesTI.Estudiante", conditions)  # Cambia la tabla según tu estructura

            if results:
                return results[0][1]  # Asumiendo que el nombre está en la segunda columna
            else:
                return "Estudiante no encontrado"
        except Exception as e:
            print(f"Error al consultar el nombre del estudiante: {e}")
            return "Error al obtener el nombre"

# Código para abrir la ventana
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = consulta11()  # Instanciar la clase del diálogo
    ui.setupUi(Dialog)  # Configurar la interfaz
    Dialog.exec_()  # Mostrar la ventana de manera modal
    sys.exit(app.exec_())  # Iniciar el bucle de eventos de la aplicación
