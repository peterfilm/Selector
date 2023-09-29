from modules.api import conf, only_digits
import re
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIntValidator

class FromDigit:
    '''
    Начинать с нужной цифры
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.lineEdit_digit.returnPressed.connect(self.pressed)
        
        int_validator = QIntValidator()
        int_validator.setBottom(1)  # Optional: Set a minimum value (0 in this case)
        self.mw.lineEdit_digit.setValidator(int_validator)
            
    def pressed(self):
        name = re.fullmatch(only_digits, self.mw.lineEdit_digit.text())
        if not name:
            QMessageBox.warning(self.mw, 'Ошибка', 'Недопустимое значение для номера')
            self.mw.lineEdit_digit.clear()