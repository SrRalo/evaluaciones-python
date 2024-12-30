import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
from conexion import register_data, query_data, update_data, join_tables, connect_to_db
from registro11 import registro11
from register12 import register12
from register13 import register13
from consulta11 import consulta11 as EstudianteDialog  
from consulta12 import consulta12 as DocenteDialog  
from reporte11 import reporte11
from reporte12 import reporte12
from psycopg2.extras import RealDictCursor


#
class AsignarDetalleDocente(QtWidgets.QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion  # Conexión para utilizar la función register_data
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Asignar Detalle Docente")
        self.setGeometry(100, 100, 400, 300)

        # Etiquetas y campos de selección
        self.label_docente = QtWidgets.QLabel("Seleccionar Docente:", self)
        self.label_docente.setGeometry(50, 50, 150, 20)
        self.combo_docente = QtWidgets.QComboBox(self)  # Asegúrate de que el nombre sea combo_docente
        self.combo_docente.setGeometry(200, 50, 150, 20)
        self.load_docentes()  # Cargar docentes disponibles

        self.label_evaluacion = QtWidgets.QLabel("Seleccionar Evaluación:", self)
        self.label_evaluacion.setGeometry(50, 100, 150, 20)
        self.combo_evaluacion = QtWidgets.QComboBox(self)
        self.combo_evaluacion.setGeometry(200, 100, 150, 20)
        self.load_evaluaciones()  # Cargar evaluaciones disponibles

        # Campo para ingresar la nota
        self.label_nota = QtWidgets.QLabel("Nota del Docente:", self)
        self.label_nota.setGeometry(50, 150, 150, 20)
        self.input_nota = QtWidgets.QLineEdit(self)
        self.input_nota.setGeometry(200, 150, 150, 20)

        # Botón para asignar evaluación
        self.boton_asignar = QtWidgets.QPushButton("Asignar Evaluación", self)
        self.boton_asignar.setGeometry(150, 200, 100, 30)
        self.boton_asignar.clicked.connect(self.asignar_detalle_docente)

    def query_data(self, table, conditions=None):
        """Consulta los datos de la base de datos"""
        conn = connect_to_db()
        if conn:
            try:
                with conn.cursor() as cursor:  # No es necesario el RealDictCursor aquí
                    query = f"SELECT * FROM {table}"
                    if conditions:
                        query += f" WHERE {conditions}"
                    cursor.execute(query)
                    results = cursor.fetchall()
                    return results
            except Exception as e:
                print(f"Error al consultar datos de la tabla {table}: {e}")
                return []
            finally:
                conn.close()

    def load_docentes(self):
        """Carga los docentes disponibles en el combo box"""
        docentes = self.conexion.query_data("evaluacionesTI.Docentes")
        for docente in docentes:
            self.combo_docente.addItem(docente[1], docente[0])  # Accede usando índices

    def load_evaluaciones(self):
        """Carga las evaluaciones asignadas disponibles en el combo box"""
        evaluaciones = self.conexion.query_data("evaluacionesTI.Evaluacion_Asignada")
        for evaluacion in evaluaciones:
            self.combo_evaluacion.addItem(evaluacion[1], evaluacion[0])  # Accede usando índices

    def asignar_detalle_docente(self):
        """Asigna la evaluación al docente"""
        id_docente = self.combo_docente.currentData()  # Obtener ID del docente
        id_evaluacion = self.combo_evaluacion.currentData()  # Obtener ID de la evaluación
        nota = self.input_nota.text()

        # Validar que la nota no esté vacía
        if not nota:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "La nota es obligatoria.")
            return

        try:
            # Asignar la evaluación al detalle del docente en la base de datos
            data = {
                "nota_evaDocente": float(nota),
                "id_docente": id_docente,
                "id_evaluacion_asignada": id_evaluacion
            }
            self.conexion.register_data("evaluacionesTI.Detalle_EvaDocente", data)
            QtWidgets.QMessageBox.information(self, "Éxito", "Evaluación asignada correctamente.")
            self.close()  # Cerrar ventana después de asignar
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al asignar evaluación: {str(e)}")
#
#
class AsignarNotaEstudiante(QtWidgets.QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion  # Conexión para utilizar la función register_data
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Asignar Nota Estudiante")
        self.setGeometry(100, 100, 400, 300)

        # Etiquetas y campos de selección
        self.label_estudiante = QtWidgets.QLabel("Seleccionar Estudiante:", self)
        self.label_estudiante.setGeometry(50, 50, 150, 20)
        self.combo_estudiante = QtWidgets.QComboBox(self)  # Asegúrate de que el nombre sea combo_estudiante
        self.combo_estudiante.setGeometry(200, 50, 150, 20)
        self.load_estudiantes()  # Cargar estudiantes disponibles

        self.label_evaluacion = QtWidgets.QLabel("Seleccionar Evaluación:", self)
        self.label_evaluacion.setGeometry(50, 100, 150, 20)
        self.combo_evaluacion = QtWidgets.QComboBox(self)
        self.combo_evaluacion.setGeometry(200, 100, 150, 20)
        self.load_evaluaciones()  # Cargar evaluaciones disponibles

        # Campo para ingresar la nota
        self.label_nota = QtWidgets.QLabel("Nota del Estudiante:", self)
        self.label_nota.setGeometry(50, 150, 150, 20)
        self.input_nota = QtWidgets.QLineEdit(self)
        self.input_nota.setGeometry(200, 150, 150, 20)

        # Botón para asignar evaluación
        self.boton_asignar = QtWidgets.QPushButton("Asignar Nota", self)
        self.boton_asignar.setGeometry(150, 200, 100, 30)
        self.boton_asignar.clicked.connect(self.asignar_nota_estudiante)
    #
    def query_data(self, table, conditions=None):
        """Consulta los datos de la base de datos"""
        conn = connect_to_db()
        if conn:
            try:
                with conn.cursor() as cursor:  
                    query = f"SELECT * FROM {table}"
                    if conditions:
                        query += f" WHERE {conditions}"
                    cursor.execute(query)
                    results = cursor.fetchall()
                    return results
            except Exception as e:
                print(f"Error al consultar datos de la tabla {table}: {e}")
                return []
            finally:
                conn.close()
    #
     
    #            
    def load_estudiantes(self):
        """Carga los estudiantes disponibles en el combo box"""
        estudiantes = self.conexion.query_data("evaluacionesTI.Estudiante")
        print("Estudiantes cargados:", estudiantes)
        for estudiante in estudiantes:
            self.combo_estudiante.addItem(estudiante[1], estudiante[0])  # Accede usando índices

    def load_evaluaciones(self):
        """Carga las evaluaciones asignadas disponibles en el combo box"""
        evaluaciones = self.conexion.query_data("evaluacionesTI.Evaluacion_Asignada")
        for evaluacion in evaluaciones:
            self.combo_evaluacion.addItem(evaluacion[1], evaluacion[0])  # Accede usando índices

    def asignar_nota_estudiante(self):
        """Asigna la evaluación al estudiante con la nota"""
        id_estudiante = self.combo_estudiante.currentData()  # Obtener ID del estudiante
        id_evaluacion = self.combo_evaluacion.currentData()  # Obtener ID de la evaluación
        nota = self.input_nota.text()

        # Validar que la nota no esté vacía
        if not nota:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "La nota es obligatoria.")
            return

        try:
            # Asignar la evaluación al detalle del estudiante en la base de datos
            data = {
                "nota_evaEstudiante": float(nota),
                "id_estudiante": id_estudiante,
                "id_evaluacion_asignada": id_evaluacion
            }
            self.conexion.register_data("evaluacionesTI.Detalle_EvaEstudiante", data)
            QtWidgets.QMessageBox.information(self, "Éxito", "Nota asignada correctamente.")
            self.close()  # Cerrar ventana después de asignar
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al asignar nota: {str(e)}")
#                        

#Registro estudiante
class RegistroEstudiante(QtWidgets.QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion  # Recibe la referencia al módulo donde está `register_data`
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Registrar Estudiante")
        self.setGeometry(100, 100, 400, 300)

        # Etiquetas y campos de texto
        self.label_nombre = QtWidgets.QLabel("Nombre del Estudiante:", self)
        self.label_nombre.setGeometry(50, 50, 150, 20)
        self.input_nombre = QtWidgets.QLineEdit(self)
        self.input_nombre.setGeometry(200, 50, 150, 20)

        self.label_contacto = QtWidgets.QLabel("Contacto del Estudiante:", self)
        self.label_contacto.setGeometry(50, 100, 150, 20)
        self.input_contacto = QtWidgets.QLineEdit(self)
        self.input_contacto.setGeometry(200, 100, 150, 20)

        self.label_carrera = QtWidgets.QLabel("Carrera:", self)
        self.label_carrera.setGeometry(50, 150, 150, 20)
        self.combo_carrera = QtWidgets.QComboBox(self)
        self.combo_carrera.setGeometry(200, 150, 150, 20)

        # Cargar carreras en el combobox
        self.cargar_carreras()

        # Botón para registrar
        self.boton_registrar = QtWidgets.QPushButton("Registrar", self)
        self.boton_registrar.setGeometry(150, 200, 100, 30)
        self.boton_registrar.clicked.connect(self.registrar_estudiante)

    def cargar_carreras(self):
        # Obtener carreras de la base de datos
        try:
            conn = self.conexion.connect_to_db()
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id_carrera, nombre_carrera FROM evaluacionesTI.Carreras")
                    carreras = cursor.fetchall()
                    for carrera in carreras:
                        self.combo_carrera.addItem(carrera[1], carrera[0])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al cargar carreras: {str(e)}")

    def registrar_estudiante(self):
        # Obtener datos de los campos de texto
        nombre = self.input_nombre.text()
        contacto = self.input_contacto.text()
        id_carrera = self.combo_carrera.currentData()

        # Validar que los campos no estén vacíos
        if not nombre or not contacto:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            # Registrar datos usando la función `register_data`
            data = {
                "nombre_estudiante": nombre,
                "contacto_estudiante": contacto,
                "id_carrera": id_carrera
            }
            self.conexion.register_data("evaluacionesTI.Estudiante", data)
            QtWidgets.QMessageBox.information(self, "Éxito", "Estudiante registrado correctamente.")
            self.close()  # Cierra la ventana después de registrar
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al registrar estudiante: {str(e)}")

#Registro Docente
class RegistroDocente(QtWidgets.QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion  # Recibe la referencia al módulo donde está `register_data`
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Registrar Docente")
        self.setGeometry(100, 100, 400, 300)

        # Etiquetas y campos de texto
        self.label_cedula = QtWidgets.QLabel("Cédula del Docente:", self)
        self.label_cedula.setGeometry(50, 50, 150, 20)
        self.input_cedula = QtWidgets.QLineEdit(self)
        self.input_cedula.setGeometry(200, 50, 150, 20)

        self.label_nombre = QtWidgets.QLabel("Nombre del Docente:", self)
        self.label_nombre.setGeometry(50, 100, 150, 20)
        self.input_nombre = QtWidgets.QLineEdit(self)
        self.input_nombre.setGeometry(200, 100, 150, 20)

        self.label_contacto = QtWidgets.QLabel("Contacto del Docente:", self)
        self.label_contacto.setGeometry(50, 150, 150, 20)
        self.input_contacto = QtWidgets.QLineEdit(self)
        self.input_contacto.setGeometry(200, 150, 150, 20)

        # Botón para registrar
        self.boton_registrar = QtWidgets.QPushButton("Registrar", self)
        self.boton_registrar.setGeometry(150, 200, 100, 30)
        self.boton_registrar.clicked.connect(self.registrar_docente)

    def registrar_docente(self):
        # Obtener datos de los campos de texto
        cedula = self.input_cedula.text()
        nombre = self.input_nombre.text()
        contacto = self.input_contacto.text()

        # Validar que los campos no estén vacíos
        if not cedula or not nombre or not contacto:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            # Registrar datos usando la función `register_data`
            data = {
                "id_docente": cedula,  # Asumiendo que la cédula es el ID del docente
                "nombre_docente": nombre,
                "contacto_docente": contacto
            }
            self.conexion.register_data("evaluacionesTI.Docentes", data)
            QtWidgets.QMessageBox.information(self, "Éxito", "Docente registrado correctamente.")
            self.close()  # Cierra la ventana después de registrar
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al registrar docente: {str(e)}")

#Consulta de Carrera
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap

class consulta13(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 410)

        # Botón para registrar carreras
        self.registrar_carrera_button = QtWidgets.QPushButton("Registrar Carrera", Dialog)
        self.registrar_carrera_button.setGeometry(QtCore.QRect(50, 260, 301, 22))
        self.registrar_carrera_button.clicked.connect(self.registrar_carrera)

        # Botones OK y Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Cambiar el texto del botón "OK" a "Consultar"
        button_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if button_ok:
            button_ok.setText("Consultar")

        # Etiqueta principal
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 10, 191, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # Etiqueta para ID Carrera
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 60, 141, 16))
        self.label_3.setObjectName("label_3")

        # Campo de entrada para ID Carrera
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 80, 301, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")

        # Etiqueta para mostrar resultados
        self.resultLabel = QtWidgets.QLabel(Dialog)
        self.resultLabel.setGeometry(QtCore.QRect(50, 120, 301, 22))
        self.resultLabel.setObjectName("resultLabel")

        self.retranslateUi(Dialog)

        # Conectar señales
        self.buttonBox.accepted.connect(self.consultarDetalles)  
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def registrar_carrera(self):
        self.registrar_carrera_window = RegistrarCarreraWindow()
        self.registrar_carrera_window.exec_()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Consultar Detalles de Carrera"))
        self.label.setText(_translate("Dialog", "Consultar Detalles de Carrera"))
        self.label_3.setText(_translate("Dialog", "ID Carrera a Consultar:"))

    def consultarDetalles(self):
        id_carrera = self.lineEdit_2.text().strip()

        # Verificar si el ID de carrera es válido
        if not id_carrera:
            self.resultLabel.setText("Por favor ingrese un ID de carrera.")
            return
        
        # Llamar al método de consulta con el ID de carrera
        resultados = self.query_data(id_carrera)
        if resultados:
            self.mostrarResultados(resultados)
        else:
            self.resultLabel.setText("No se encontró la carrera.")

    @staticmethod
    def query_data(id_carrera):
        """Consulta la base de datos para obtener detalles de la carrera"""
        try:
            conn = connect_to_db()
            if conn is None:
                return None

            with conn.cursor() as cursor:
                cursor.execute("SELECT id_carrera, nombre_carrera FROM evaluacionesTI.Carreras WHERE id_carrera = %s", (id_carrera,))
                resultados = cursor.fetchall()  # Se obtienen todos los resultados

                # Consultar el número de estudiantes matriculados en la carrera
                cursor.execute("SELECT COUNT(*) FROM evaluacionesTI.Estudiante WHERE id_carrera = %s", (id_carrera,))
                num_estudiantes = cursor.fetchone()[0]

            conn.close()
            return resultados, num_estudiantes
        except Exception as e:
            print(f"Error al consultar la base de datos: {e}")
            return None

    def mostrarResultados(self, resultados):
        """Muestra los resultados en una ventana aparte"""
        resultados, num_estudiantes = resultados
        self.result_window = ResultWindow(resultados, num_estudiantes)
        self.result_window.exec_()

class RegistrarCarreraWindow(QtWidgets.QDialog):
        def __init__(self, parent=None):
            from PyQt5 import QtCore, QtGui, QtWidgets
            from PyQt5.QtWidgets import QLabel, QLineEdit
            from PyQt5.QtGui import QPixmap
            from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
            super().__init__(parent)
            self.setWindowTitle("Registrar Carrera")
            self.setGeometry(100, 100, 400, 200)

            layout = QVBoxLayout()

            # Etiqueta y campo de texto para el ID de la carrera
            self.id_carrera_label = QLabel("ID de la Carrera:")
            self.id_carrera_input = QLineEdit()
            layout.addWidget(self.id_carrera_label)
            layout.addWidget(self.id_carrera_input)

            # Etiqueta y campo de texto para el nombre de la carrera
            self.nombre_carrera_label = QLabel("Nombre de la Carrera:")
            self.nombre_carrera_input = QLineEdit()
            layout.addWidget(self.nombre_carrera_label)
            layout.addWidget(self.nombre_carrera_input)

            # Botón para registrar la carrera
            self.registrar_button = QPushButton("Registrar")
            self.registrar_button.clicked.connect(self.registrar_carrera)
            layout.addWidget(self.registrar_button)

            self.setLayout(layout)

        def registrar_carrera(self):
            id_carrera = self.id_carrera_input.text()
            nombre_carrera = self.nombre_carrera_input.text()

            if not id_carrera or not nombre_carrera:
                QMessageBox.warning(self, "Advertencia", "Por favor ingrese todos los campos.")
                return

            try:
                conn = connect_to_db()
                if conn is None:
                    return

                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO evaluacionesTI.Carreras (id_carrera, nombre_carrera) VALUES (%s, %s)", (id_carrera, nombre_carrera))
                    conn.commit()

                QMessageBox.information(self, "Éxito", "Carrera registrada correctamente.")
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al registrar carrera: {str(e)}")
   

class ResultWindow(QDialog):
    def __init__(self, results, num_estudiantes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de Búsqueda")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Lista para mostrar los resultados
        self.result_list = QListWidget()
        for result in results:
            self.result_list.addItem(f"ID: {result[0]} \nNombre: {result[1]}")
        layout.addWidget(self.result_list)

        # Etiqueta para mostrar el número de estudiantes matriculados
        self.estudiantes_label = QLabel(f"Número de estudiantes matriculados: {num_estudiantes}")
        layout.addWidget(self.estudiantes_label)

        # Botón para cerrar la ventana
        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
      
#Actualizar contraseña
class ActualizarContrasenaDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 280)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Cambiar el texto del botón Ok a "Actualizar"
        boton_actualizar = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        boton_actualizar.setText("Actualizar")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 10, 281, 41))
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 70, 71, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 70, 191, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 110, 101, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 110, 191, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Dialog)

        # Conectar el botón de "Actualizar" a la función on_actualizar_click
        self.buttonBox.accepted.connect(self.on_actualizar_click)
        self.buttonBox.rejected.connect(Dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Actualizar Contraseña"))
        self.label.setText(_translate("Dialog", "Actualizar Contraseña"))
        self.label_3.setText(_translate("Dialog", "Usuario:"))
        self.label_4.setText(_translate("Dialog", "Contraseña nueva:"))

    def on_actualizar_click(self):
        """Llamado cuando se hace clic en 'Actualizar'"""
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()

        if not username or not password:
            self.mostrar_mensaje("Error", "Por favor, completa todos los campos.")
            return

        # Llamar a la función de actualización de contraseña con los parámetros correctos
        updates = {'password': password}
        conditions = f'"username" = %s'  # Condición para filtrar por el username

        # Aquí pasas los valores correctamente, como una tupla
        values = (password, username)

        if update_data("evaluacionesTI.Usuarios", updates, conditions, values):
            self.mostrar_mensaje("Éxito", "La contraseña se actualizó correctamente.")
        else:
            self.mostrar_mensaje("Error", "No se pudo actualizar la contraseña.")

    def mostrar_mensaje(self, titulo, mensaje):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec_()

#Clase para ver usuarios
class AdminUsuariosWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrador de Usuarios")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QtWidgets.QVBoxLayout(self)

        # Label del título
        self.title_label = QtWidgets.QLabel("ADMINISTRADOR DE USUARIOS")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Formulario para ingresar usuario, clave y rol
        form_layout = QtWidgets.QFormLayout()
        self.user_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(["Estudiante, Docente", "Admin"])  # Opciones de rol
        form_layout.addRow("Usuario:", self.user_input)
        form_layout.addRow("Clave:", self.password_input)
        form_layout.addRow("Rol:", self.role_input)

        # Botones de acción
        self.save_button = QtWidgets.QPushButton("Guardar")
        self.delete_button = QtWidgets.QPushButton("Eliminar")
        self.search_button = QtWidgets.QPushButton("Buscar")
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)

        # Tabla de usuarios
        self.user_table = QtWidgets.QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Usuario", "Contraseña", "Rol"])
        self.user_table.horizontalHeader().setStretchLastSection(True)

        # Agregar al layout principal
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.user_table)

        # Conectar botones con funciones
        self.save_button.clicked.connect(self.save_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.search_button.clicked.connect(self.search_user)

        # Cargar usuarios al iniciar
        self.load_users()

    def save_user(self):
        import conexion
        usuario = self.user_input.text()
        clave = self.password_input.text()
        rol = self.role_input.currentText()

        if usuario and clave and rol:
            rol_id = 1 if rol == "Coordinador" else 0  # Mapeo de rol
            data = {
                "username": usuario,
                "password": clave,
                "user_role": rol_id
            }
            conexion.register_data("evaluacionesTI.Usuarios", data)
            self.load_users()
            QtWidgets.QMessageBox.information(self, "Éxito", "Usuario guardado correctamente.")
        else:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")

    def delete_user(self):
        import conexion
        usuario = self.user_input.text()

        if usuario:
            exists = conexion.check_if_exists(
                "SELECT COUNT(*) FROM evaluacionesTI.Usuarios WHERE username = %s", (usuario,)
            )
            if exists:
                query = "DELETE FROM evaluacionesTI.Usuarios WHERE username = %s"
                conn = conexion.connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute(query, (usuario,))
                    conn.commit()
                QtWidgets.QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
                self.load_users()
            else:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Usuario no encontrado.")
        else:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Por favor ingresa un nombre de usuario.")

    def search_user(self):
        import conexion
        consulta = self.user_input.text()

        if consulta:
            users = conexion.query_data(
                "evaluacionesTI.Usuarios", f"username LIKE '%{consulta}%'"
            )
            self.populate_user_table(users)
        else:
            self.load_users()

    def load_users(self):
        import conexion
        users = conexion.query_data("evaluacionesTI.Usuarios")
        self.populate_user_table(users)

    def populate_user_table(self, users):
        self.user_table.setRowCount(0)  # Limpiar la tabla
        for row_num, user in enumerate(users):
            self.user_table.insertRow(row_num)
            self.user_table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(user[0]))  # username
            self.user_table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(user[1]))  # password
            rol = "Admin" if user[2] == 1 else "Usuario"
            self.user_table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(rol))


class Menubar(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        #
        MainWindow.setStyleSheet("background-color:White;")


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        #
        self.menubar.setStyleSheet("background-color: white;")

        # Menús principales
        self.menuRegistrar = QtWidgets.QMenu(self.menubar)
        self.menuRegistrar.setObjectName("menuRegistrar")
        self.menuConsultar = QtWidgets.QMenu(self.menubar)
        self.menuConsultar.setObjectName("menuConsultar")
        self.menuActualizar = QtWidgets.QMenu(self.menubar)
        self.menuActualizar.setObjectName("menuActualizar")
        self.menuReporte = QtWidgets.QMenu(self.menubar)
        self.menuReporte.setObjectName("menuReporte")
        self.menuSesion = QtWidgets.QMenu(self.menubar)
        self.menuSesion.setObjectName("menuSesion")

        MainWindow.setMenuBar(self.menubar)

        # Acciones del Menú Registrar
        self.actionRegistrar_Evaluacion = QtWidgets.QAction(MainWindow)
        self.actionRegistrar_Evaluacion.setObjectName("actionRegistrar_Evaluaci_n")
        self.actionRegistrar_Evaluacion.triggered.connect(self.open_register_window)
        self.actionRegistrar_Detalle_Estudiante = QtWidgets.QAction(MainWindow)

        self.menuRegistrar.addAction(self.actionRegistrar_Evaluacion)


        self.actionRegistrar_Estudiante = QtWidgets.QAction(MainWindow)
        self.actionRegistrar_Estudiante.setObjectName("actionRegistrar_Estudiante")
        self.actionRegistrar_Estudiante.triggered.connect(self.open_register_estudiante)

        self.actionRegistrar_Docente = QtWidgets.QAction(MainWindow)
        self.actionRegistrar_Docente.setObjectName("actionRegistrar_Docente")
        self.actionRegistrar_Docente.triggered.connect(self.open_register_docente)

        self.menuRegistrar.addAction(self.actionRegistrar_Estudiante)
        self.menuRegistrar.addAction(self.actionRegistrar_Docente)
        #
        self.actionAsignar_Detalle_Docente = QtWidgets.QAction(MainWindow)
        self.actionAsignar_Detalle_Docente.setObjectName("actionAsignar_Detalle_Docente")
        self.actionAsignar_Detalle_Docente.triggered.connect(self.open_asignar_detalle_docente_window)
        self.menuRegistrar.addAction(self.actionAsignar_Detalle_Docente)
        #
        self.action_asignar_nota_estudiante = QtWidgets.QAction("Asignar Nota Estudiante", self)
        self.action_asignar_nota_estudiante.triggered.connect(self.open_asignar_nota_estudiante_window)
        self.menuRegistrar.addAction(self.action_asignar_nota_estudiante)
        #
        self.actionAdministrar_Usuarios = QtWidgets.QAction(MainWindow)
        self.actionAdministrar_Usuarios.setObjectName("actionAdministrar_Usuarios")
        self.actionAdministrar_Usuarios.setText("Administrar Usuarios")
        self.actionAdministrar_Usuarios.triggered.connect(self.open_admin_users_window)
        self.menuRegistrar.addAction(self.actionAdministrar_Usuarios)
        #
        # Acciones del Menú Consultar
        self.actionConsultar_Carrera = QtWidgets.QAction(MainWindow)
        self.actionConsultar_Carrera.setObjectName("actionConsultar_Detalles_de_Carrera")
        self.actionConsultar_Carrera.triggered.connect(self.open_consulta13)
        self.actionConsultar_Estudiante = QtWidgets.QAction(MainWindow)
        self.actionConsultar_Estudiante.setObjectName("actionConsultar_Evaluaci_n_Estudiante")
        self.actionConsultar_Estudiante.triggered.connect(self.open_consulta_estudiante)
        self.actionConsultar_Docente = QtWidgets.QAction(MainWindow)
        self.actionConsultar_Docente.setObjectName("actionConsultar_Evaluaci_n_Docente")
        self.actionConsultar_Docente.triggered.connect(self.open_consulta_docente)
        self.menuConsultar.addAction(self.actionConsultar_Carrera)
        self.menuConsultar.addAction(self.actionConsultar_Estudiante)
        self.menuConsultar.addAction(self.actionConsultar_Docente)
        

        # Acciones del Menú Actualizar
        self.actionActualizar_Contrasena = QtWidgets.QAction(MainWindow)
        self.actionActualizar_Contrasena.setObjectName("actionActualizar_Contrasena")
        self.actionActualizar_Contrasena.triggered.connect(self.open_actualizar_contrasena)
        self.menuActualizar.addAction(self.actionActualizar_Contrasena)
   
        # Acciones del Menú Reporte
        self.actionReporte_Estudiante = QtWidgets.QAction(MainWindow)
        self.actionReporte_Estudiante.setObjectName("actionReporte_Evaluaci_n_Estudiante")
        self.actionReporte_Docente = QtWidgets.QAction(MainWindow)
        self.actionReporte_Docente.setObjectName("actionReporte_Evaluaci_n_Docente")
        self.menuReporte.addAction(self.actionReporte_Estudiante)
        self.actionReporte_Estudiante.triggered.connect(self.abrir_reporte11)
        self.menuReporte.addAction(self.actionReporte_Docente)
        self.actionReporte_Docente.triggered.connect(self.abrir_reporte12)

        # Acciones del Menú Sesión
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.menuSesion.addAction(self.actionSalir)
        self.actionSalir.triggered.connect(self.close)

        # Añadir los menús al Menubar
        self.menubar.addAction(self.menuRegistrar.menuAction())
        self.menubar.addAction(self.menuConsultar.menuAction())
        self.menubar.addAction(self.menuActualizar.menuAction())
        self.menubar.addAction(self.menuReporte.menuAction())
        self.menubar.addAction(self.menuSesion.menuAction())

        import os
        # Imagen
        # Agregar QLabel para mostrar una imagen
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.imageLabel.setObjectName("imageLabel")

        # Cargar la imagen
        image_path = os.path.join(os.path.dirname(os.getcwd()),"eloy.jpg")  # Ajustar ruta relativa
        if not os.path.exists(image_path):
            print(f"Error: La imagen no existe en la ruta: {image_path}")
        else:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print("Error: La imagen no se cargó correctamente.")
            else:
                self.imageLabel.setPixmap(pixmap)
                self.imageLabel.setScaledContents(True)  # Escalar la imagen para ajustarla al QLabel
                self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
                self.imageLabel.setScaledContents(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtWidgets.QMessageBox.information(MainWindow, "Bienvenido", "¡Bienvenido a Evaluaciones TI!")

    def open_admin_users_window(self):
        # Instancia de la ventana de Administrar Usuarios
        self.admin_users_window = AdminUsuariosWindow()
        self.admin_users_window.show()

    def open_register_window(self):
        # Crear e instanciar el diálogo de registro de evaluación
        self.dialog = registro11()
        self.dialog.exec_()  

    def open_register_estudiante_window(self):
        # Abrir ventana de registro Detalle Evaluación Estudiante
        self.dialog_estudiante = QtWidgets.QDialog(self)
        self.ui_estudiante = register12()
        self.ui_estudiante.setupUi(self.dialog_estudiante)
        self.dialog_estudiante.exec_()

    def open_register_docente_window(self):
        # Abrir ventana de registro Detalle Evaluación Docente
        self.dialog_docente = QtWidgets.QDialog(self)
        self.ui_docente = register13()
        self.ui_docente.setupUi(self.dialog_docente)
        self.dialog_docente.exec_()

    def open_register_estudiante(self):
        import conexion
        self.ventana_registro_estudiante = RegistroEstudiante(conexion)
        self.ventana_registro_estudiante.show()

    def open_register_docente(self):
        import conexion    
        self.ventana_registro_docente = RegistroDocente(conexion)
        self.ventana_registro_docente.show()  

    def open_asignar_detalle_docente_window(self):
        import conexion 
        self.ventana_asignar_docente = AsignarDetalleDocente(conexion) 
        self.ventana_asignar_docente.show() 

    def open_asignar_nota_estudiante_window(self):
        """Abre la ventana de asignación de nota estudiante"""
        import conexion
        self.ventana_asignar_nota_estudiante = AsignarNotaEstudiante(conexion)
        self.ventana_asignar_nota_estudiante.show()

    def open_consulta_estudiante(self):
        # Crear la ventana para la consulta de evaluación de estudiantes
        self.dialog_estudiante = QtWidgets.QDialog(self)
        self.ui_estudiante = EstudianteDialog()  
        self.ui_estudiante.setupUi(self.dialog_estudiante)
        self.dialog_estudiante.exec_()  
    
    def open_consulta_docente(self):
        # Crear la ventana para la consulta de evaluación de docentes
        self.dialog_docente = QtWidgets.QDialog(self)
        self.ui_docente = DocenteDialog()  
        self.ui_docente.setupUi(self.dialog_docente)
        self.dialog_docente.exec_()  

    def open_consulta13(self):
        # Crear e instanciar el diálogo de consulta de carrera
        self.dialog = consulta13()
        self.dialog.exec_()  

    def open_actualizar_contrasena(self):
        # Crear e instanciar el diálogo de actualizar contraseña
        self.dialog = ActualizarContrasenaDialog()
        self.dialog.exec_() 

    def abrir_reporte11(self):
        # Crear una instancia de la clase reporte11
        self.dialogo_reporte11 = QtWidgets.QDialog()
        self.ui_reporte11 = reporte11()
        self.ui_reporte11.setupUi(self.dialogo_reporte11)
        self.dialogo_reporte11.exec_()

    def abrir_reporte12(self):
        # Crear una instancia de la clase reporte12
        self.dialogo_reporte12 = QtWidgets.QDialog()
        self.ui_reporte12 = reporte12() 
        self.ui_reporte12.setupUi(self.dialogo_reporte12) 
        self.dialogo_reporte12.exec_() 

    def configure_menu_by_role(self, role):
        if role != "admin":
            self.menuRegistrar.setDisabled(True)
            self.menuReporte.setDisabled(True)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Evaluaciones TI"))
        self.menuRegistrar.setTitle(_translate("MainWindow", "Registrar"))
        self.menuConsultar.setTitle(_translate("MainWindow", "Consultar"))
        self.menuActualizar.setTitle(_translate("MainWindow", "Actualizar"))
        self.menuReporte.setTitle(_translate("MainWindow", "Reporte"))
        self.menuSesion.setTitle(_translate("MainWindow", "Sesión"))
        self.actionRegistrar_Evaluacion.setText(_translate("MainWindow", "Registrar Evaluación"))
        self.actionAdministrar_Usuarios.setText(_translate("MainWindow", "Administrar Usuarios"))
        self.actionRegistrar_Estudiante.setText(_translate("MainWindow", "Registrar Estudiante"))
        self.actionRegistrar_Docente.setText(_translate("MainWindow", "Registrar Docente"))
        self.actionAsignar_Detalle_Docente.setText(_translate("MainWindow", "Asignar Detalle Docente"))
        self.action_asignar_nota_estudiante.setText("Asignar Nota Estudiante")
        self.actionConsultar_Carrera.setText(_translate("MainWindow", "Consultar Detalles de Carrera"))
        self.actionConsultar_Estudiante.setText(_translate("MainWindow", "Consultar Evaluación Estudiante"))
        self.actionConsultar_Docente.setText(_translate("MainWindow", "Consultar Evaluación Docente"))
        self.actionActualizar_Contrasena.setText(_translate("MainWindow", "Actualizar Contraseña"))
        self.actionReporte_Estudiante.setText(_translate("MainWindow", "Reporte Evaluación Estudiante"))
        self.actionReporte_Docente.setText(_translate("MainWindow", "Reporte Evaluación Docente"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))

class MainWindow(QtWidgets.QMainWindow, Menubar):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.username = username  # Guardamos el nombre de usuario
        self.configure_menubar()

    def configure_menubar(self):
        """
        Configura el menú dinámicamente según el rol del usuario.
        """
        user_data = query_data("evaluacionesTI.Usuarios", f"username = '{self.username}'")
        if user_data and user_data[0][3] == "admin":  # Asumimos que el tercer campo (índice 3) es el rol
            # Si el usuario es admin, habilitar todas las opciones
            self.menuRegistrar.setEnabled(True)
            self.menuConsultar.setEnabled(True)
            self.menuActualizar.setEnabled(True)
            self.menuReporte.setEnabled(True)
        else:
            # Desactivar todas las opciones excepto Consultar y Actualizar
            self.menuRegistrar.setEnabled(False)
            self.menuReporte.setEnabled(False)
            self.menuConsultar.setEnabled(True)
            self.menuActualizar.setEnabled(True)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Simulamos un inicio de sesión para obtener el nombre de usuario
    # En una integración real, este dato vendría del sistema de login
    logged_in_user = "admin"  # Cambiar según el usuario actual
    
    window = MainWindow(logged_in_user)
    window.show()
    sys.exit(app.exec_())
