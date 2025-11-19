from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QComboBox, QLabel, QPushButton, 
                               QLineEdit, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt
import sys

class ComboBoxDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComboBox PySide6 - Todas las opciones")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # ========== COMBOBOX BÁSICO ==========
        group_basico = QGroupBox("1. ComboBox Básico")
        layout_basico = QVBoxLayout()
        
        self.combo_basico = QComboBox()
        self.combo_basico.addItem("Opción 1")
        self.combo_basico.addItem("Opción 2")
        self.combo_basico.addItem("Opción 3")
        self.combo_basico.addItems(["Opción 4", "Opción 5", "Opción 6"])
        
        self.label_basico = QLabel("Selección: Ninguna")
        self.combo_basico.currentTextChanged.connect(
            lambda text: self.label_basico.setText(f"Selección: {text}")
        )
        
        layout_basico.addWidget(self.combo_basico)
        layout_basico.addWidget(self.label_basico)
        group_basico.setLayout(layout_basico)
        layout.addWidget(group_basico)
        
        # ========== COMBOBOX EDITABLE ==========
        group_editable = QGroupBox("2. ComboBox Editable")
        layout_editable = QVBoxLayout()
        
        self.combo_editable = QComboBox()
        self.combo_editable.setEditable(True)
        self.combo_editable.addItems(["Python", "JavaScript", "Java", "C++", "Ruby"])
        self.combo_editable.setPlaceholderText("Escribe o selecciona...")
        
        # Políticas de inserción
        self.combo_editable.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        
        self.label_editable = QLabel("Texto actual: ")
        self.combo_editable.currentTextChanged.connect(
            lambda text: self.label_editable.setText(f"Texto actual: {text}")
        )
        
        layout_editable.addWidget(QLabel("Puedes escribir o seleccionar:"))
        layout_editable.addWidget(self.combo_editable)
        layout_editable.addWidget(self.label_editable)
        group_editable.setLayout(layout_editable)
        layout.addWidget(group_editable)
        
        # ========== COMBOBOX CON DATOS ==========
        group_datos = QGroupBox("3. ComboBox con Datos Asociados")
        layout_datos = QVBoxLayout()
        
        self.combo_datos = QComboBox()
        # addItem(text, userData)
        self.combo_datos.addItem("Rojo", "#FF0000")
        self.combo_datos.addItem("Verde", "#00FF00")
        self.combo_datos.addItem("Azul", "#0000FF")
        self.combo_datos.addItem("Amarillo", "#FFFF00")
        
        self.label_datos = QLabel("Color seleccionado: ")
        
        def mostrar_datos():
            texto = self.combo_datos.currentText()
            dato = self.combo_datos.currentData()
            indice = self.combo_datos.currentIndex()
            self.label_datos.setText(
                f"Color: {texto} | Código: {dato} | Índice: {indice}"
            )
        
        self.combo_datos.currentIndexChanged.connect(mostrar_datos)
        
        layout_datos.addWidget(self.combo_datos)
        layout_datos.addWidget(self.label_datos)
        group_datos.setLayout(layout_datos)
        layout.addWidget(group_datos)
        
        # ========== MÉTODOS DE MANIPULACIÓN ==========
        group_metodos = QGroupBox("4. Métodos de Manipulación")
        layout_metodos = QVBoxLayout()
        
        self.combo_metodos = QComboBox()
        self.combo_metodos.addItems([f"Item {i}" for i in range(1, 6)])
        
        # Controles
        controles_layout = QHBoxLayout()
        
        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText("Nuevo item")
        
        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_item)
        
        btn_eliminar = QPushButton("Eliminar actual")
        btn_eliminar.clicked.connect(self.eliminar_item)
        
        btn_limpiar = QPushButton("Limpiar todo")
        btn_limpiar.clicked.connect(self.combo_metodos.clear)
        
        controles_layout.addWidget(self.input_item)
        controles_layout.addWidget(btn_agregar)
        controles_layout.addWidget(btn_eliminar)
        controles_layout.addWidget(btn_limpiar)
        
        self.label_count = QLabel(f"Total items: {self.combo_metodos.count()}")
        
        layout_metodos.addWidget(self.combo_metodos)
        layout_metodos.addLayout(controles_layout)
        layout_metodos.addWidget(self.label_count)
        group_metodos.setLayout(layout_metodos)
        layout.addWidget(group_metodos)
        
        # ========== CONFIGURACIONES ADICIONALES ==========
        group_config = QGroupBox("5. Configuraciones Adicionales")
        layout_config = QVBoxLayout()
        
        self.combo_config = QComboBox()
        self.combo_config.addItems(["Opción A", "Opción B", "Opción C", 
                                     "Opción D con texto muy largo para ver el comportamiento"])
        
        # Opciones de configuración
        check_duplicados = QCheckBox("Permitir duplicados")
        check_duplicados.setChecked(False)
        check_duplicados.stateChanged.connect(
            lambda state: self.combo_config.setDuplicatesEnabled(state == Qt.CheckState.Checked)
        )
        
        check_frame = QCheckBox("Mostrar marco")
        check_frame.setChecked(True)
        check_frame.stateChanged.connect(
            lambda state: self.combo_config.setFrame(state == Qt.CheckState.Checked)
        )
        
        # Tamaño máximo visible de items
        btn_max_visible = QPushButton("Max 3 items visibles")
        btn_max_visible.clicked.connect(lambda: self.combo_config.setMaxVisibleItems(3))
        
        # Establecer tamaño mínimo
        btn_min_width = QPushButton("Ancho mínimo 200px")
        btn_min_width.clicked.connect(lambda: self.combo_config.setMinimumWidth(200))
        
        config_buttons = QHBoxLayout()
        config_buttons.addWidget(btn_max_visible)
        config_buttons.addWidget(btn_min_width)
        
        layout_config.addWidget(self.combo_config)
        layout_config.addWidget(check_duplicados)
        layout_config.addWidget(check_frame)
        layout_config.addLayout(config_buttons)
        group_config.setLayout(layout_config)
        layout.addWidget(group_config)
        
        # Información de políticas de inserción
        info_label = QLabel(
            "<b>Políticas de Inserción disponibles:</b><br>"
            "• InsertAtTop - Insertar al inicio<br>"
            "• InsertAtBottom - Insertar al final<br>"
            "• InsertAtCurrent - Insertar en posición actual<br>"
            "• InsertAfterCurrent - Insertar después de actual<br>"
            "• InsertBeforeCurrent - Insertar antes de actual<br>"
            "• InsertAlphabetically - Insertar alfabéticamente<br>"
            "• NoInsert - No permitir inserción"
        )
        layout.addWidget(info_label)
        
    def agregar_item(self):
        texto = self.input_item.text()
        if texto:
            self.combo_metodos.addItem(texto)
            self.input_item.clear()
            self.label_count.setText(f"Total items: {self.combo_metodos.count()}")
    
    def eliminar_item(self):
        indice = self.combo_metodos.currentIndex()
        if indice >= 0:
            self.combo_metodos.removeItem(indice)
            self.label_count.setText(f"Total items: {self.combo_metodos.count()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ComboBoxDemo()
    ventana.show()
    sys.exit(app.exec())