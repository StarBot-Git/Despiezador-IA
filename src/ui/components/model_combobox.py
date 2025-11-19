from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PySide6.QtCore import Qt, QModelIndex, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPainter, QFont

class IconComboBoxDelegate(QStyledItemDelegate):
    """Delegate para renderizar items con iconos"""
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        
        # Obtener datos
        icon = index.data(Qt.DecorationRole)
        text = index.data(Qt.DisplayRole)
        
        # Background según estado (sin usar palette, más simple)
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, Qt.lightGray)
        elif option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, Qt.gray)
        # No pintamos background si no hay estado especial (CSS lo maneja)
        
        # Dibujar icono
        icon_size = 24
        icon_rect = option.rect.adjusted(10, 
                                         (option.rect.height() - icon_size) // 2, 
                                         -option.rect.width() + 10 + icon_size, 
                                         -(option.rect.height() - icon_size) // 2)
        if icon:
            icon.paint(painter, icon_rect)
        
        # Dibujar texto
        text_x = icon_rect.right() + 10
        painter.setPen(Qt.black)
        
        font = QFont()
        font.setPointSize(10)
        font.setWeight(QFont.Medium)
        painter.setFont(font)
        
        text_rect = option.rect.adjusted(text_x, 0, -10, 0)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        
        painter.restore()
    
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(option.rect.width(), 40)


class IconComboBox(QComboBox):
    """ComboBox con iconos personalizados"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName("SideBar-ComboBoxes")
        
        # Configurar modelo
        self.model = QStandardItemModel()
        self.setModel(self.model)
        
        # Aplicar delegate
        delegate = IconComboBoxDelegate()
        self.setItemDelegate(delegate)
        
        # Configurar tamaño
        self.setMinimumHeight(40)
        self.view().setMinimumWidth(280)
    
    def add_item(self, text: str, icon_path: str = ""):
        """Añade un item con icono opcional"""
        item = QStandardItem(text)
        
        if icon_path:
            item.setIcon(QIcon(icon_path))
        
        self.model.appendRow(item)
    
    def clear_items(self):
        """Limpia todos los items"""
        self.model.clear()


# Ejemplo de uso:
"""
from ui.components.icon_combobox import IconComboBox
from config import settings

# Crear combobox
self.model_combo = IconComboBox(self)

# Añadir items con iconos
self.model_combo.add_item("GPT-4 Turbo", settings.GPT4_ICON_DIR)
self.model_combo.add_item("GPT-4", settings.GPT4_ICON_DIR)
self.model_combo.add_item("GPT-3.5 Turbo", settings.GPT35_ICON_DIR)

# Añadir al layout
layout.addWidget(self.model_combo)
"""