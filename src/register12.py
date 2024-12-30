from PyQt5 import QtCore, QtGui, QtWidgets
from conexion import register_data  # Asegúrate de tener la función importada correctamente

class register12(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 414)
        Dialog.setStyleSheet("background-color: #f2f2f2;")
        # Configuración del botón de acción
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Registrar")
        
        # Etiqueta de encabezado
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 10, 231, 41))
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # Campos de entrada (Nota, ID Estudiante, ID Evaluación Asignada)
        self.lineEdit_nota = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_nota.setGeometry(QtCore.QRect(40, 110, 301, 22))
        self.lineEdit_nota.setObjectName("lineEdit_nota")
        
        self.label_nota = QtWidgets.QLabel(Dialog)
        self.label_nota.setGeometry(QtCore.QRect(40, 90, 141, 16))
        self.label_nota.setObjectName("label_nota")
        
        self.lineEdit_estudiante = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_estudiante.setGeometry(QtCore.QRect(40, 180, 301, 22))
        self.lineEdit_estudiante.setObjectName("lineEdit_estudiante")
        
        self.label_estudiante = QtWidgets.QLabel(Dialog)
        self.label_estudiante.setGeometry(QtCore.QRect(40, 160, 141, 16))
        self.label_estudiante.setObjectName("label_estudiante")
        
        self.lineEdit_evaluacion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_evaluacion.setGeometry(QtCore.QRect(40, 250, 301, 22))
        self.lineEdit_evaluacion.setObjectName("lineEdit_evaluacion")
        
        self.label_evaluacion = QtWidgets.QLabel(Dialog)
        self.label_evaluacion.setGeometry(QtCore.QRect(40, 230, 141, 16))
        self.label_evaluacion.setObjectName("label_evaluacion")

        # Llamada a la función de traducción
        self.retranslateUi(Dialog)

        # Conectar el botón "Ok" con la acción de guardar los datos
        self.buttonBox.accepted.connect(self.save_data)  # Usamos self.save_data para guardar los datos

        # Conectar el botón "Cancel" para cerrar el formulario sin hacer nada
        self.buttonBox.rejected.connect(Dialog.reject)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Registro Detalle Evaluación Estudiante"))
        self.label.setText(_translate("Dialog", "Registro Detalle Evaluación Estudiante"))
        self.label_nota.setText(_translate("Dialog", "Nota de Evaluación:"))
        self.label_estudiante.setText(_translate("Dialog", "ID Estudiante:"))
        self.label_evaluacion.setText(_translate("Dialog", "ID Evaluación Asignada:"))

    def save_data(self):
        # Capturar los datos del formulario
        nota = self.lineEdit_nota.text()  # Obtener la Nota
        id_estudiante = self.lineEdit_estudiante.text()  # Obtener el ID Estudiante
        id_evaluacion_asignada = self.lineEdit_evaluacion.text()  # Obtener el ID Evaluación Asignada

        # Crear el diccionario con los datos que se van a insertar en la base de datos
        data = {
            'nota_evaEstudiante': nota,  # Nota de la evaluación
            'id_estudiante': id_estudiante,  # ID del estudiante
            'id_evaluacion_asignada': id_evaluacion_asignada  # ID de la evaluación asignada
        }

        # Llamar a la función register_data para insertar los datos en la base de datos
        table_name = "evaluacionesTI.Detalle_EvaEstudiante"  # Nombre de la tabla en la base de datos
        register_data(table_name, data)  # Insertar los datos

        # Mostrar mensaje de éxito
        QtWidgets.QMessageBox.information(None, "Éxito", "Los datos fueron registrados correctamente.")

# Para abrir la ventana en una aplicación PyQt5
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = register12()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
