from PyQt5.QtGui import QPixmap, QPainter, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QStyledItemDelegate


class ComboRating:
    '''
    Выбор звездочки
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.rating.ratingChanged.connect(self.selection_change)
        
    def selection_change(self, i):
        pass