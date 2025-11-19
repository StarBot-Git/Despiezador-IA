from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QComboBox, QLabel, QScrollArea)
from PySide6.QtCore import Qt
import sys

class ComboBoxEstilosDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComboBox PySide6 - Todos los Estilos CSS")
        self.setGeometry(100, 100, 1000, 800)
        
        # Scroll area para contener todo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)
        
        container = QWidget()
        scroll.setWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # ========== ESTILO BÁSICO ==========
        layout.addWidget(QLabel("<h2>1. Estilo Básico</h2>"))
        
        combo_basico = QComboBox()
        combo_basico.addItems(["Opción 1", "Opción 2", "Opción 3"])
        combo_basico.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 5px 10px;
                min-height: 30px;
                font-size: 14px;
            }
        """)
        layout.addWidget(combo_basico)
        
        # ========== ESTILO CON HOVER ==========
        layout.addWidget(QLabel("<h2>2. Con efectos Hover y Focus</h2>"))
        
        combo_hover = QComboBox()
        combo_hover.addItems(["Opción A", "Opción B", "Opción C"])
        combo_hover.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px 15px;
                min-height: 35px;
                font-size: 14px;
                color: #2c3e50;
            }
            
            QComboBox:hover {
                background-color: #ecf0f1;
                border: 2px solid #2980b9;
            }
            
            QComboBox:focus {
                background-color: #e8f4f8;
                border: 2px solid #2980b9;
                outline: none;
            }
            
            QComboBox:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        layout.addWidget(combo_hover)
        
        # ========== ESTILO CON FLECHA PERSONALIZADA ==========
        layout.addWidget(QLabel("<h2>3. Flecha desplegable personalizada</h2>"))
        
        combo_flecha = QComboBox()
        combo_flecha.addItems(["Item 1", "Item 2", "Item 3"])
        combo_flecha.setStyleSheet("""
            QComboBox {
                background-color: #9b59b6;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                min-height: 35px;
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: #8e44ad;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 2px solid white;
                width: 10px;
                height: 10px;
                border-top: none;
                border-right: none;
                transform: rotate(-45deg);
                margin-right: 8px;
            }
            
            QComboBox:hover {
                background-color: #a569bd;
            }
        """)
        layout.addWidget(combo_flecha)
        
        # ========== ESTILO MODERNO/MATERIAL ==========
        layout.addWidget(QLabel("<h2>4. Estilo Material Design</h2>"))
        
        combo_material = QComboBox()
        combo_material.addItems(["Material 1", "Material 2", "Material 3"])
        combo_material.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid #e74c3c;
                padding: 8px 5px;
                min-height: 30px;
                font-size: 15px;
                color: #2c3e50;
            }
            
            QComboBox:hover {
                border-bottom: 2px solid #c0392b;
            }
            
            QComboBox:focus {
                border-bottom: 3px solid #e74c3c;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #e74c3c;
                margin-right: 10px;
            }
        """)
        layout.addWidget(combo_material)
        
        # ========== LISTA DESPLEGABLE PERSONALIZADA ==========
        layout.addWidget(QLabel("<h2>5. Lista desplegable (QListView) personalizada</h2>"))
        
        combo_lista = QComboBox()
        combo_lista.addItems([f"Elemento {i}" for i in range(1, 8)])
        combo_lista.setStyleSheet("""
            QComboBox {
                background-color: #16a085;
                border: 2px solid #1abc9c;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 35px;
                font-size: 14px;
                color: white;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 10px solid white;
                margin-right: 10px;
            }
            
            /* Estilo de la lista desplegable */
            QComboBox QAbstractItemView {
                background-color: #1abc9c;
                border: 2px solid #16a085;
                border-radius: 6px;
                selection-background-color: #16a085;
                selection-color: white;
                color: white;
                padding: 5px;
                outline: none;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px;
                border-radius: 4px;
                min-height: 30px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #17b896;
            }
            
            QComboBox QAbstractItemView::item:selected {
                background-color: #16a085;
                font-weight: bold;
            }
        """)
        layout.addWidget(combo_lista)
        
        # ========== ESTILO DEGRADADO ==========
        layout.addWidget(QLabel("<h2>6. Con degradado y sombras</h2>"))
        
        combo_degradado = QComboBox()
        combo_degradado.addItems(["Opción Premium", "Opción Gold", "Opción Platinum"])
        combo_degradado.setStyleSheet("""
            QComboBox {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22
                );
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 40px;
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
            
            QComboBox:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5ab35, stop:1 #e98b39
                );
            }
            
            QComboBox::drop-down {
                border: none;
                width: 35px;
                background: transparent;
            }
            
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 12px solid white;
                margin-right: 12px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #e67e22;
                border-radius: 8px;
                selection-background-color: #f39c12;
                selection-color: white;
                color: #2c3e50;
                padding: 5px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 10px;
                min-height: 35px;
            }
        """)
        layout.addWidget(combo_degradado)
        
        # ========== ESTILO OSCURO/DARK MODE ==========
        layout.addWidget(QLabel("<h2>7. Modo Oscuro (Dark Mode)</h2>"))
        
        combo_dark = QComboBox()
        combo_dark.addItems(["Dark Option 1", "Dark Option 2", "Dark Option 3"])
        combo_dark.setStyleSheet("""
            QComboBox {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 8px;
                padding: 10px 15px;
                min-height: 35px;
                font-size: 14px;
                color: #ecf0f1;
            }
            
            QComboBox:hover {
                background-color: #34495e;
                border: 2px solid #4a6278;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: #34495e;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 10px solid #ecf0f1;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #34495e;
                border: 2px solid #4a6278;
                border-radius: 8px;
                selection-background-color: #4a6278;
                selection-color: #ecf0f1;
                color: #ecf0f1;
                padding: 5px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 10px;
                min-height: 30px;
                border-radius: 4px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #3d566e;
            }
        """)
        layout.addWidget(combo_dark)
        
        # ========== COMBOBOX EDITABLE ESTILIZADO ==========
        layout.addWidget(QLabel("<h2>8. ComboBox Editable con estilo</h2>"))
        
        combo_editable = QComboBox()
        combo_editable.setEditable(True)
        combo_editable.addItems(["Editable 1", "Editable 2", "Editable 3"])
        combo_editable.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 10px 15px;
                min-height: 35px;
                font-size: 14px;
                color: #2c3e50;
            }
            
            QComboBox:editable {
                background-color: #e8f8f5;
            }
            
            QComboBox:hover {
                border: 2px solid #229954;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 35px;
                background-color: #27ae60;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 10px solid white;
                margin-right: 10px;
            }
            
            /* Estilo del campo de texto interno */
            QComboBox QLineEdit {
                background-color: transparent;
                border: none;
                color: #2c3e50;
                padding: 0px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #27ae60;
                border-radius: 8px;
                selection-background-color: #27ae60;
                selection-color: white;
                color: #2c3e50;
                padding: 5px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 10px;
                min-height: 30px;
            }
        """)
        layout.addWidget(combo_editable)
        
        # ========== ESTILO MINIMALISTA ==========
        layout.addWidget(QLabel("<h2>9. Estilo Minimalista</h2>"))
        
        combo_minimal = QComboBox()
        combo_minimal.addItems(["Simple", "Clean", "Minimal"])
        combo_minimal.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                border: 1px solid #dfe6e9;
                border-radius: 4px;
                padding: 8px 12px;
                min-height: 30px;
                font-size: 14px;
                color: #2d3436;
            }
            
            QComboBox:hover {
                border: 1px solid #74b9ff;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid #636e72;
                margin-right: 8px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #dfe6e9;
                selection-background-color: #74b9ff;
                selection-color: white;
                color: #2d3436;
                outline: none;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px;
                min-height: 25px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #dfe6e9;
            }
        """)
        layout.addWidget(combo_minimal)
        
        # Información adicional
        info = QLabel("""
        <h3>Propiedades CSS principales:</h3>
        <ul>
            <li><b>QComboBox</b> - Estilo del widget principal</li>
            <li><b>QComboBox::drop-down</b> - Botón de la flecha</li>
            <li><b>QComboBox::down-arrow</b> - Icono de la flecha</li>
            <li><b>QComboBox QAbstractItemView</b> - Lista desplegable</li>
            <li><b>QComboBox QAbstractItemView::item</b> - Items individuales</li>
            <li><b>QComboBox QLineEdit</b> - Campo editable (si es editable)</li>
        </ul>
        <h3>Estados disponibles:</h3>
        <ul>
            <li><b>:hover</b> - Cuando el mouse está encima</li>
            <li><b>:focus</b> - Cuando tiene el foco</li>
            <li><b>:disabled</b> - Cuando está deshabilitado</li>
            <li><b>:editable</b> - Cuando es editable</li>
            <li><b>:on</b> - Cuando está abierto</li>
            <li><b>:selected</b> - Item seleccionado</li>
        </ul>
        """)
        layout.addWidget(info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ComboBoxEstilosDemo()
    ventana.show()
    sys.exit(app.exec())