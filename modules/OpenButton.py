from modules.api import conf
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMessageBox
import os

class OpenButton:
    '''
    Кнопка для открытия папки с фотографиями
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.pushButton_openFolder.clicked.connect(self.open_folder)
        
    def open_folder(self):
        if conf['PATH']:
            QDesktopServices.openUrl(QUrl.fromLocalFile(conf['PATH']))
        else:
            QMessageBox.warning(self.mw, 'Ошибка', 'Путь не найден')