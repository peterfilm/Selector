import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QStyledItemDelegate, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPalette
from PyQt5.QtCore import Qt

class RatingComboBoxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.isValid():
            text = index.data()
            stars = index.data(Qt.UserRole)  # Number of stars

            # Draw text
            super().paint(painter, option, index)

            # Draw stars
            star_icon = QPixmap("img/star.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            for i in range(stars):
                painter.drawPixmap(option.rect.x() + option.rect.width() - 30 - i * 25, option.rect.y(), star_icon)

class RatingComboBox(QComboBox):
    def __init__(self, layout_widget):
        super().__init__()
        self.layout_widget = layout_widget

        ratings = [
            {"text": "Выберать рейтинг", "stars": 0},
            {"text": "1 звезда", "stars": 1},
            {"text": "2 звезды", "stars": 2},
            {"text": "3 звезды", "stars": 3},
            {"text": "4 звезды", "stars": 4},
            {"text": "5 звезд", "stars": 5},
        ]

        delegate = RatingComboBoxDelegate(self)
        self.setItemDelegate(delegate)

        for rating_data in ratings:
            self.addItem(rating_data["text"], rating_data["stars"])
            
            
            
# Получить значение из комобокса
# selected_index = combo_box.currentIndex()
# selected_data = combo_box.itemData(selected_index, Qt.UserRole)  # Assuming you stored the value in UserRole
# if selected_data is not None:
#     rating_value = selected_data  # Use the value as needed
# else:
#     rating_value = None  # Handle the placeholder item