from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PySide6.QtCore import Qt, QModelIndex, QSize, QRect
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPainter, QFont, QColor

class IconComboBoxDelegate(QStyledItemDelegate):
    """Delegate para renderizar items con iconos y estilos personalizados"""

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()

        # Obtener datos
        icon = index.data(Qt.DecorationRole)
        text = index.data(Qt.DisplayRole)
        item = index.model().item(index.row())
        enabled = item.isEnabled()

        rect = option.rect

        # =============================
        # 1. FONDO SEGÚN ESTADO
        # =============================

        if not enabled:
            # Fondo tenue del item deshabilitado
            painter.fillRect(rect, Qt.white)
        else:
            # Hover
            if option.state & QStyle.State_MouseOver:
                painter.fillRect(rect, QColor("#F1F5F9"))  # gris suave
            # Seleccionado
            elif option.state & QStyle.State_Selected:
                painter.fillRect(rect, QColor("#E8EEF5"))  # azul muy claro
            else:
                painter.fillRect(rect, QColor("#FFFFFF"))  # fondo normal

        # =============================
        # 2. ICONO
        # =============================
        icon_size = 24
        icon_rect = QRect(
            rect.left() + 10,
            rect.top() + (rect.height() - icon_size) // 2,
            icon_size,
            icon_size,
        )

        if icon:
            mode = QIcon.Normal if enabled else QIcon.Disabled
            icon.paint(painter, icon_rect, Qt.AlignCenter, mode)

        # =============================
        # 3. TEXTO
        # =============================

        font = QFont()
        font.setPointSize(10)
        font.setWeight(QFont.Medium)
        painter.setFont(font)

        text_color = QColor("#0F172A") if enabled else QColor("#9CA3AF")  # gris apagado
        painter.setPen(text_color)

        text_rect = QRect(
            icon_rect.right() + 10,
            rect.top(),
            rect.width() - icon_rect.width() - 20,
            rect.height()
        )

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

    def get_value(self) -> str:
        return self.currentText()
