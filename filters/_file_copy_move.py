from PyQt5.QtCore import Qt, QThread, pyqtSignal
import shutil
from modules.api import conf
import os

class FileCopyMove(QThread):
    mysignal = pyqtSignal(object)

    def __init__(self, files, new_path, operation, rawjpg, parent=None):
        QThread.__init__(self, parent)
        self.files = files
        self.new_path = new_path
        self.operation = operation
        self.rawjpg = rawjpg
        self.running = False 

    def run(self):  # обязательный для потоков метод
        self.running = True
        for file_name in self.files:
            if self.running:
                source_file_path = os.path.normpath(os.path.join(conf['PATH'], file_name))
                target_file_path = os.path.normpath(os.path.join(self.new_path, file_name))
                xmp = '.'.join(file_name.split('.')[:-1]) + '.xmp'
                target_file_path_xmp = os.path.normpath(os.path.join(self.new_path, xmp))
                if self.operation == "copy":
                    try:
                        shutil.copy(source_file_path, target_file_path)
                        if os.path.exists(os.path.normpath(os.path.join(conf['PATH'], xmp))):
                            shutil.copy(os.path.normpath(os.path.join(conf['PATH'], xmp)), target_file_path_xmp)
                        if self.rawjpg:
                            for i in conf['JPEGS']:
                                file = os.path.normpath(os.path.join(conf['PATH'], '.'.join(file_name.split('.')[:-1]) + '.' + i))
                                copy_path = os.path.normpath(os.path.join(self.new_path, '.'.join(file_name.split('.')[:-1]) + '.' + i))
                                if os.path.exists(file):
                                    shutil.copy(file, copy_path)
                    except Exception as e:
                        print(e)
                elif self.operation == "move":
                    try:
                        shutil.move(source_file_path, target_file_path)
                        if os.path.exists(os.path.normpath(os.path.join(conf['PATH'], xmp))):
                            shutil.move(os.path.normpath(os.path.join(conf['PATH'], xmp)), target_file_path_xmp)
                            
                        if self.rawjpg:
                            for i in conf['JPEGS']:
                                file = os.path.normpath(os.path.join(conf['PATH'], '.'.join(file_name.split('.')[:-1]) + '.' + i))
                                move_path = os.path.normpath(os.path.join(self.new_path, '.'.join(file_name.split('.')[:-1]) + '.' + i))
                                if os.path.exists(file):
                                    shutil.move(file, move_path)
                    except Exception as e:
                        print(e)
            self.mysignal.emit(file_name)
            
            