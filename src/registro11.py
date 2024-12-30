from PyQt5 import QtCore, QtGui, QtWidgets
from conexion import register_data, check_if_exists

class registro11(QtWidgets.QDialog):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 412)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 330, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Cambiar el texto del botón "OK" a "Registrar"
        button_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if button_ok:
            button_ok.setText("Registrar")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 10, 191, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 141, 16))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 160, 141, 16))
        self.label_3.setObjectName("label_3")
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(50, 110, 301, 22))
        self.lineEdit.setObjectName("lineEdit")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 180, 301, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 230, 141, 16))
        self.label_4.setObjectName("label_4")
        
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(50, 250, 301, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.register_evaluacion)  # Usamos la función de registro
        self.buttonBox.rejected.connect(Dialog.reject)  # Mantener la acción de cancelar
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Registrar Evaluación"))
        self.label.setText(_translate("Dialog", "Registro de Evaluación Asignada"))
        self.label_2.setText(_translate("Dialog", "ID Evaluación Asignada:"))
        self.label_3.setText(_translate("Dialog", "Tipo de Evaluación:"))
        self.label_4.setText(_translate("Dialog", "Nombre de Evaluación:"))

    def register_evaluacion(self):
        # Obtener los datos de los campos de texto
        id_evaluacion = self.lineEdit.text()
        tipo_evaluacion = self.lineEdit_2.text()
        nombre_evaluacion = self.lineEdit_3.text()

    

        # Verificar que los campos no estén vacíos
        if not id_evaluacion or not tipo_evaluacion or not nombre_evaluacion:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Todos los campos son obligatorios.")
            return
        
        # Verificar si el id_evaluacion_asignada ya existe
        if self.id_evaluacion_exists(id_evaluacion):
            QtWidgets.QMessageBox.warning(None, "Error", "El ID de Evaluación Asignada ya existe.")
            return

        # Crear el diccionario de datos que se insertarán en la base de datos
        data = {
            'id_evaluacion_asignada': id_evaluacion,
            'tipo_evaluacion': tipo_evaluacion,
            'nombre_evaluacion': nombre_evaluacion
        }

        # Llamar a la función de registro de datos
        register_data("evaluacionesTI.Evaluacion_Asignada", data)

        # Mostrar un mensaje de éxito
        QtWidgets.QMessageBox.information(None, "Éxito", "Evaluación registrada correctamente.")
        

        # Limpiar los campos de entrada
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()

    def id_evaluacion_exists(self, id_evaluacion):
        """Función que verifica si el id_evaluacion_asignada ya existe en la base de datos."""
        query = f"SELECT COUNT(*) FROM evaluacionesTI.Evaluacion_Asignada WHERE id_evaluacion_asignada = %s"
        result = check_if_exists(query, (id_evaluacion,))  # Asumiendo que esta función devuelve un valor True/False
        return result


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = registro11()
    main_window.exec_()
    sys.exit(app.exec_())
