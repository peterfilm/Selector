from modules.api import conf, name_of_file
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

class ChangeDir:
    '''
    Изменение директории файлов
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.checkBox_dir.stateChanged.connect(self.dir_settings)
        self.mw.pushButton_path.clicked.connect(self.choose_path)
        self.mw.lineEdit_path.textChanged.connect(self.path_check)
        self.mw.lineEdit_path.returnPressed.connect(self.path_check_exist)
        
    def dir_settings(self):
        ch = 1 if self.mw.checkBox_dir.checkState() else 0
        self.mw.lineEdit_path.setEnabled(ch)
        self.mw.pushButton_path.setEnabled(ch)
        self.mw.lineEdit_path.setStyleSheet("color: #ffffff") if ch else self.mw.lineEdit_path.setStyleSheet("")
        
        if not self.mw.checkBox_dir.checkState() and self.mw.lineEdit_path.text():
            self.mw.pushButton_copy.setEnabled(False)
            self.mw.pushButton_changeDir.setEnabled(False)
            
        if self.mw.checkBox_dir.checkState() and self.mw.lineEdit_path.text():
            self.mw.pushButton_copy.setEnabled(True)
            self.mw.pushButton_changeDir.setEnabled(True)
        
        
    def choose_path(self):
        try:
            directory = QFileDialog.getExistingDirectory(self.mw)
            if directory:
                self.mw.lineEdit_path.setText(directory)
        except Exception as e:
            print(e)
        
    def path_check(self):
        if self.mw.lineEdit_path.text():
            self.mw.pushButton_copy.setEnabled(True)
            self.mw.pushButton_changeDir.setEnabled(True)
        else:
            self.mw.pushButton_copy.setEnabled(False)
            self.mw.pushButton_changeDir.setEnabled(False)
            
    def path_check_exist(self):
        if not os.path.exists(self.mw.lineEdit_path.text()):
            self.mw.lineEdit_path.setText('')
            QMessageBox.warning(self.mw, 'Ошибка', 'Путь не найден')