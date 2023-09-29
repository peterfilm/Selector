from modules.api import conf, load_key_to_api
from PyQt5.QtWidgets import QFileDialog
from filters._checker_path import Checker
import os


class SelectFolder:
    '''
    Кнопка выбора папки
    '''

    def __init__(self, main_window):
        self.mw = main_window
        Checker.check_in_conf(self.mw)
        self.mw.pushButton_files.clicked.connect(self.folder_clicked)
        self.mw.lineEdit_files.returnPressed.connect(self.userlink)
        if conf['PATH']:
            self.mw.label_status.setText('Выбрана директория с фотографиями. Добавьте список номеров фотографий и нажмите "Найти"')
            self.mw.pushButton_openFolder.setEnabled(True)
        else:
            self.mw.label_status.setText('Выберите директорию с фотографиями')
            self.mw.pushButton_openFolder.setEnabled(False)
            
    def folder_clicked(self):
        if not conf['PATH']:
            try:
                directory = QFileDialog.getExistingDirectory(self.mw)
            except Exception as e:
                print(e)
        else:
            try:
                directory = QFileDialog.getExistingDirectory(
                    self.mw, directory=conf['PATH'])
            except:
                pass
        if Checker.check_path(self.mw, directory):
            load_key_to_api('PATH', directory)
            conf['PATH'] = directory
        Checker.check_in_conf(self.mw)
        self.mw.pushButton_openFolder.setEnabled(True)
        self.mw.label_status.setText('Выбрана директория с фотографиями. Добавьте список номеров фотографий и нажмите "Найти"')
        
    def userlink(self):
        if os.path.exists(self.mw.lineEdit_files.text()):
            if Checker.check_path(self.mw, self.mw.lineEdit_files.text()):
                load_key_to_api('PATH', self.mw.lineEdit_files.text())
                conf['PATH'] = self.mw.lineEdit_files.text()
            Checker.check_in_conf(self.mw)
            self.mw.pushButton_openFolder.setEnabled(True)
            self.mw.label_status.setText('Выбрана директория с фотографиями. Добавьте список номеров фотографий и нажмите "Найти"')
        else:
            self.mw.lineEdit_files.setText(conf['PATH'])
            self.mw.pushButton_openFolder.setEnabled(False)
            self.mw.label_status.setText('Несуществующая директория. Введите корректный путь к файлам')
