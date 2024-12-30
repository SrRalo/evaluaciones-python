from PyQt5 import QtCore, QtGui, QtWidgets
from conexion import join_tables
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors

class reporte11(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 450)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 390, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Visualizar")

        # Botón adicional para generar PDF
        self.generate_pdf_button = QtWidgets.QPushButton(Dialog)
        self.generate_pdf_button.setGeometry(QtCore.QRect(150, 350, 100, 30))
        self.generate_pdf_button.setObjectName("generate_pdf_button")

        # Label principal
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 481, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # Etiqueta para ID de Evaluación
        self.label_id = QtWidgets.QLabel(Dialog)
        self.label_id.setGeometry(QtCore.QRect(50, 80, 150, 20))
        self.label_id.setObjectName("label_id")
        
        # Campo de entrada para ID de Evaluación
        self.input_id = QtWidgets.QLineEdit(Dialog)
        self.input_id.setGeometry(QtCore.QRect(200, 80, 150, 20))
        self.input_id.setObjectName("input_id")

        # Lista para mostrar resultados
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(50, 120, 300, 200))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.visualizar_datos)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.generate_pdf_button.clicked.connect(self.generar_pdf)  # Conectar el botón para PDF
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Reporte Evaluaciones a Estudiante"))
        self.label.setText(_translate("Dialog", "Generar Reporte de Evaluaciones a Estudiantes:"))
        self.label_id.setText(_translate("Dialog", "ID de Evaluación Asignada:"))
        self.generate_pdf_button.setText(_translate("Dialog", "Generar PDF"))

    def visualizar_datos(self):
        # Obtener el ID de Evaluación ingresado
        id_evaluacion_asignada = self.input_id.text()

        if not id_evaluacion_asignada.isdigit():
            QtWidgets.QMessageBox.warning(None, "Error", "Por favor, ingrese un ID de Evaluación válido.")
            return

        # Llamar a la función join_tables
        self.results = join_tables(
            table1="evaluacionesTI.Detalle_EvaEstudiante",
            table2="evaluacionesTI.Evaluacion_Asignada",
            common_column="id_evaluacion_asignada",
            columns_to_select=["detalle_evaestudiante.*", "evaluacion_asignada.nombre_evaluacion"],
            conditions=f"detalle_evaestudiante.id_evaluacion_asignada = {id_evaluacion_asignada}"
        )

        if self.results:
            self.listWidget.clear()  # Limpiar la lista antes de agregar nuevos resultados
            for row in self.results:
                item_text = (
                    f"ID Evaluación Estudiante: {row['id_evaestudiante']}\n"
                    f"Nota: {row['nota_evaestudiante']}\n"
                    f"ID Evaluación Asignada: {row['id_evaluacion_asignada']}\n"
                    f"Nombre Evaluación: {row['nombre_evaluacion']}\n\n"
                )
                self.listWidget.addItem(item_text)  # Agregar el item formateado a la lista
        else:
            QtWidgets.QMessageBox.information(None, "Resultados", "No se encontraron datos para el ID proporcionado.")

    def generar_pdf(self):
        # Verificar si hay resultados disponibles
        if not hasattr(self, 'results') or not self.results:
            QtWidgets.QMessageBox.warning(None, "Error", "No hay datos para generar el PDF. Realice una consulta primero.")
            return

        # Dialog para seleccionar ubicación del archivo
        archivo, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar como", "", "PDF files (*.pdf);;All files (*)")
        if not archivo:
            return

        # Crear documento PDF
        pdf = SimpleDocTemplate(archivo, pagesize=letter)
        datos = [["ID Estudiante", "Nota", "ID Evaluación", "Nombre Evaluación"]]

        # Agregar filas de datos
        for row in self.results:
            datos.append([
                row['id_evaestudiante'],
                row['nota_evaestudiante'],
                row['id_evaluacion_asignada'],
                row['nombre_evaluacion']
            ])

        # Configurar estilo de la tabla
        tabla = Table(datos)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Guardar el PDF
        pdf.build([tabla])
        QtWidgets.QMessageBox.information(None, "Éxito", f"Reporte guardado en: {archivo}")

    def validar_id(self, id_evaluacion_asignada):
        if not id_evaluacion_asignada.isdigit():
            return False
        return True

    def obtener_resultados(self, id_evaluacion_asignada):
        self.results = join_tables(
            table1="evaluacionesTI.Detalle_EvaEstudiante",
            table2="evaluacionesTI.Evaluacion_Asignada",
            common_column="id_evaluacion_asignada",
            columns_to_select=["detalle_evaestudiante.*", "evaluacion_asignada.nombre_evaluacion"],
            conditions=f"detalle_evaestudiante.id_evaluacion_asignada = {id_evaluacion_asignada}"
        )
        return self.results

    def mostrar_resultados(self, resultados):
        if resultados:
            self.listWidget.clear()  # Limpiar la lista antes de agregar nuevos resultados
            for row in resultados:
                item_text = (
                    f"ID Evaluación Estudiante: {row['id_evaestudiante']}\n"
                    f"Nota: {row['nota_evaestudiante']}\n"
                    f"ID Evaluación Asignada: {row['id_evaluacion_asignada']}\n"
                    f"Nombre Evaluación: {row['nombre_evaluacion']}\n\n"
                )
                self.listWidget.addItem(item_text)  # Agregar el item formateado a la lista
        else:
            QtWidgets.QMessageBox.information(None, "Resultados", "No se encontraron datos para el ID proporcionado.")

    def generar_pdf(self):
        # Verificar si hay resultados disponibles
        if not hasattr(self, 'results') or not self.results:
            QtWidgets.QMessageBox.warning(None, "Error", "No hay datos para generar el PDF. Realice una consulta primero.")
            return

        # Dialog para seleccionar ubicación del archivo
        archivo, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar como", "", "PDF files (*.pdf);;All files (*)")
        if not archivo:
            return

        # Crear documento PDF
        pdf = SimpleDocTemplate(archivo, pagesize=letter)
        datos = [["ID Estudiante", "Nota", "ID Evaluación", "Nombre Evaluación"]]

        # Agregar filas de datos
        for row in self.results:
            datos.append([
                row['id_evaestudiante'],
                row['nota_evaestudiante'],
                row['id_evaluacion_asignada'],
                row['nombre_evaluacion']
            ])

        # Configurar estilo de la tabla
        tabla = Table(datos)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Guardar el PDF
        pdf.build([tabla])
        QtWidgets.QMessageBox.information(None, "Éxito", f"Reporte guardado en: {archivo}")

# Código para abrir la ventana
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = reporte11()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
            