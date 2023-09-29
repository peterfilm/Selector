from modules.api import conf, name_of_file
import re
from PyQt5.QtWidgets import QMessageBox

class RenameButton:
    '''
    Кнопка переименования
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.checkBox_rename.stateChanged.connect(self.rename)
        self.mw.lineEdit_rename.returnPressed.connect(self.pressed)
        
        self.reveal(0)
    
    def reveal(self, value):
        if value == 1:
            self.mw.lineEdit_rename.setEnabled(True)
            self.mw.lineEdit_rename.setStyleSheet("color: #ffffff")
            self.mw.lineEdit_sep.setEnabled(True)
            self.mw.lineEdit_sep.setStyleSheet("color: #ffffff")
            self.mw.comboBox_nulls.setEnabled(True)
            self.mw.lineEdit_digit.setEnabled(True)
            self.mw.lineEdit_digit.setStyleSheet("color: #ffffff")
            
            self.mw.lineEdit_rename.show()
            self.mw.lineEdit_sep.show()
            self.mw.comboBox_nulls.show()
            self.mw.lineEdit_digit.show()
            self.mw.label_newName.show()
        elif value == 0:
            self.mw.lineEdit_rename.setEnabled(False)
            self.mw.lineEdit_sep.setEnabled(False)
            self.mw.comboBox_nulls.setEnabled(False)
            self.mw.lineEdit_rename.setStyleSheet("")
            self.mw.lineEdit_digit.setEnabled(False)
            self.mw.lineEdit_digit.setStyleSheet("")
            
            self.mw.lineEdit_rename.hide()
            self.mw.lineEdit_sep.hide()
            self.mw.comboBox_nulls.hide()
            self.mw.lineEdit_digit.hide()
            self.mw.label_newName.hide()
        
    def rename(self):
        self.reveal(self.mw.checkBox_rename.isChecked())
        self.mw.checkBox_rename.isChecked()
            
    def pressed(self):
        name = re.fullmatch(name_of_file, self.mw.lineEdit_rename.text())
        if not name:
            QMessageBox.warning(self.mw, 'Ошибка', 'Недопустимое имя файла')
            self.mw.lineEdit_rename.clear()