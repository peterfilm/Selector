from modules.api import conf, name_of_file
import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMessageBox
import xml.etree.ElementTree as ET
import re
import shutil
from filters._errors import WrongName, WrongSeparator
from filters._raw_finder import raw_finder
from filters._jpeg_finder import jpeg_finder2
from filters._change_metaData import ChangeMetaData
from filters._rename_files import ChangeNames
from filters._blocker import blocker
from functools import partial


class EnterButton:
    '''
    Кнопка "Выполнить"
    '''
    def __init__(self, main_window):
        self.mw = main_window
        self.mw.pushButton_enter.clicked.connect(self.enter)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_label_text)
        self.new_files = []
        self.was_canceled = False
        
    def enter(self):
        files = [os.path.join(os.path.normpath(conf['PATH']), i) for i in self.mw.textEdit.toPlainText().split('\n\n_____Не найдено:_____')[0].split() if os.path.exists(os.path.join(os.path.normpath(conf['PATH']), i))]
        # counter = 0
        rating = self.mw.rating.get_rating()
        label = self.mw.comboBox_color.currentIndex()
        new_files = []
        
        self.mythread = ChangeMetaData(files, rating, label)
        self.renamer = ChangeNames(files,
                                   self.mw.checkBox_rename.isChecked(),
                                    self.mw.lineEdit_rename.text(),
                                    self.mw.lineEdit_sep.text(),
                                    self.mw.comboBox_nulls.currentIndex(),
                                    self.mw.lineEdit_digit.text(),
                                    self.mw.checkBox_rawjpg.checkState())
        
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(partial(self.on_finished, files))
        self.mythread.mysignal.connect(
            self.on_change, Qt.QueuedConnection)  # обработчик этого сигнала
        
        self.renamer.started.connect(self.on_started_rename)
        self.renamer.finished.connect(self.on_finished_rename)
        self.renamer.mysignal_rename.connect(self.on_change_rename, Qt.QueuedConnection)
        
            
        if not self.mythread.isRunning():
            self.mythread.start()
                
    def clear_label_text(self):
        # очищаем upperStatus
        self.mw.label_upperStatus.setText("")
    
    def on_stop(self, value):
        if value == 'rating':
            self.was_canceled = True
            self.mythread.running = False
        if value == 'rename':
            self.was_canceled = True
            self.renamer.running = False
        
    def on_started(self):
        self.mw.label_upperStatus.setText("Начинаю выставлять рейтинг и цветовые метки")
        self.mw.pushButton_cancel.clicked.connect(partial(self.on_stop, 'rating'))
        blocker(self.mw, 0)

    def on_finished(self, files):
        print('Закончили выставление рейтинга')
        self.timer.stop()
        self.mythread.wait(5000)
        if not self.was_canceled:
            self.mw.label_upperStatus.setText(f'Файлам установлен рейтинг и цветовая метка')
        else:
            self.mw.label_upperStatus.setText(f'Выставление рейтинга отменено')
        self.timer.start(5000)
        if self.mw.checkBox_rename.isChecked():
            if not self.renamer.isRunning():
                self.renamer.start()
        else:
            blocker(self.mw, 1)
        self.was_canceled = False
        
    def on_change(self, s):
        self.mw.label_upperStatus.setText(f'Ставим рейтинг и цветовую метку {os.path.basename(s)}')
        
    def on_started_rename(self):
        self.mw.pushButton_cancel.clicked.connect(partial(self.on_stop, 'rename'))
        print('начинаю переименовывать')
        
    def on_finished_rename(self):
        print('закончили переименовывание')
        # если были переименования
        if self.new_files and self.mw.checkBox_rename.isChecked():
            self.mw.textEdit.clear()
            for j in self.new_files:
                if self.mw.checkBox_rawjpg.checkState():
                    jpeg = jpeg_finder2(j)
                    if jpeg:
                        self.mw.textEdit.append(j + ' + ' + jpeg.split('.')[-1].upper())
                    else:
                        self.mw.textEdit.append(j)
                else:
                    self.mw.textEdit.append(j)
                        
            self.new_files = []
            self.timer.stop()
            if not self.was_canceled:
                self.mw.label_upperStatus.setText(f'Файлы переименованы')
            else: 
                self.mw.label_upperStatus.setText(f'Переименование было отменено')
            self.timer.start(5000)
        elif not self.new_files and self.mw.checkBox_rename.isChecked():
            self.mw.label_upperStatus.setText('Ошибка при переименовании')
        blocker(self.mw, 1)
        self.was_canceled = False
        
        
    def on_change_rename(self, s):
        if type(s) == str:
            self.mw.label_upperStatus.setText(f'Переименовываю {os.path.basename(s)}')
        else:
            self.new_files = s
            self.mw.label_upperStatus.setText(f'')
            
    def closeEvent(self, event):  # вызывается при закрытии окна
        self.hide()  # скрываем окно
        self.mythread.running = False  # Изменяем флаг выполнения
        self.renamer.running = False
        self.mythread.wait(5000)  # даем время чтобы закончить
        # возвращает значение True, если поток успешно завершил работу
        event.accept()
        
        