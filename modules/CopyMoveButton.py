from modules.api import conf, load_key_to_api
import os
import shutil
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMessageBox
from functools import partial
from filters._blocker import blocker
from filters._file_copy_move import FileCopyMove

class CopyMoveButton:
    '''
    Кнопка копирования в папку
    '''

    def __init__(self, main_window):
        self.mw = main_window
        
        self.mw.pushButton_copy.clicked.connect(partial(self.copy_or_move, 'copy')) # копировать файлы
        self.mw.pushButton_changeDir.clicked.connect(partial(self.copy_or_move, 'move')) # переместить файлы
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_label_text)
        
        self.timer2 = QTimer()
        
    def copy_or_move(self, operation):
        file_names = [i for i in self.mw.textEdit.toPlainText().split() if i.lower() not in ['+', 'jpg']]
        rawjpg = self.mw.checkBox_rawjpg.checkState()
        
        if self.mw.lineEdit_path.text() == conf['PATH']:
            QMessageBox.warning(self.mw, 'Ошибка', 'Выбран тот же самый путь')
        else:
            if file_names:                
                    self.mythread = FileCopyMove(file_names, self.mw.lineEdit_path.text(), operation, rawjpg)
                    self.mythread.started.connect(partial(self.on_started, operation))
                    self.mythread.finished.connect(partial(self.on_finished, operation))
                    if not self.mythread.isRunning():
                        self.mythread.start()
            else:
                old_status = self.mw.label_status.text()
                self.timer2.stop()
                if operation == 'copy':
                    self.mw.label_status.setText('Нажмите кнопку "Найти", чтобы определить файлы для копирования')
                elif operation == 'move':
                    self.mw.label_status.setText('Нажмите кнопку "Найти", чтобы определить файлы для перемещения')
                self.timer2.timeout.connect(partial(self.clear_label_text_lower, old_status))
                self.timer2.start(5000)
            
    def clear_label_text(self):
        # очищаем upperStatus
        self.mw.label_upperStatus.setText("")
        
    def clear_label_text_lower(self, value):
        # заменяем lower_status
        self.mw.label_status.setText(value)
        
    def on_stop(self, value):
        self.mythread.running = False  # изменяем флаг выполнения
        self.timer.stop()
        if value == 'copy':
            self.mw.label_upperStatus.setText('Копирование отменено')
        if value == 'move':
            self.mw.label_upperStatus.setText('Перемещение файлов отменено')
        self.timer.start(5000)
        
        
    def closeEvent(self, event):  # вызывается при закрытии окна
        self.hide()  # скрываем окно
        self.mythread.running = False  # Изменяем флаг выполнения
        self.mythread.wait(5000)  # даем время чтобы закончить
        # возвращает значение True, если поток успешно завершил работу
        event.accept()
        
    def on_started(self, value):
        if value == 'copy':
            self.mw.label_upperStatus.setText('копирую фотографии...')
            self.timer.stop()
            blocker(self.mw, 0)
            self.mw.pushButton_cancel.clicked.connect(partial(self.on_stop, 'copy'))
        elif value == 'move':
            self.mw.label_upperStatus.setText('перемещаю фотографии...')
            self.timer.stop()
            blocker(self.mw, 0)
            self.mw.pushButton_cancel.clicked.connect(partial(self.on_stop, 'move'))

    def on_finished(self, value):
        # вызывается при завершении потока
        self.timer.stop()
        if value == 'copy': 
            if self.mw.label_upperStatus.text() != 'Копирование отменено':
                self.mw.label_upperStatus.setText(f'Файлы скопированы')
        elif value == 'move':
            if self.mw.label_upperStatus.text() != 'Перемещение файлов отменено':
                self.mw.label_upperStatus.setText(f'Файлы перемещены')
                load_key_to_api('PATH', self.mw.lineEdit_path.text())
                conf['PATH'] = self.mw.lineEdit_path.text()
                self.mw.lineEdit_files.setText(conf['PATH'])
                self.mw.lineEdit_path.clear()
        blocker(self.mw, 1)
        self.timer.start(5000)
                