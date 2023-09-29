from modules.api import conf, name_of_file
import re
from PyQt5.QtWidgets import QMessageBox

class Separator:
    '''
    Поле для ввода сепаратора
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.lineEdit_sep.returnPressed.connect(self.pressed)
            
    def pressed(self):
        name = re.fullmatch(name_of_file, self.mw.lineEdit_sep.text())
        if not name:
            QMessageBox.warning(self.mw, 'Ошибка', 'Недопустимое имя сепаратора')
            self.mw.lineEdit_sep.clear()