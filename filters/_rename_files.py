from PyQt5.QtCore import QThread, pyqtSignal
from modules.api import conf, name_of_file
from PyQt5.QtWidgets import QMessageBox
import os
import xml.etree.ElementTree as ET
import re
from filters._jpeg_finder import jpeg_finder2
from filters._errors import WrongName, WrongSeparator


class ChangeNames(QThread):
    mysignal_rename = pyqtSignal(object)

    def __init__(self, files, checkbox, name, sep, nulls, digit, rawjpg, parent=None):
        QThread.__init__(self, parent)
        self.files = files
        self.checkbox = checkbox
        self.name = name
        self.sep = sep
        self.nulls = nulls
        self.digit = digit
        self.rawjpg = rawjpg
        self.new_files = []
        self.counter = 0
        self.running = True

    def run(self):  # обязательный для потоков метод 
        for file in self.files:
            if self.running:                     
                try: 
                    if re.fullmatch(name_of_file, self.name) == None:
                        raise WrongName('неверное имя файла')
                    
                    # проверяем есть ли разделитель
                    if self.sep:
                        a = re.fullmatch(name_of_file, self.sep)
                        sep = a[0] if a else None
                    else:
                        sep = ''
                    
                    # проверяем есть ли цифра
                    if self.digit:
                        digit = int(self.digit)
                    else:
                        digit = 1
                        
                    if sep != None:
                        n = self.nulls

                        new_name, self.counter = self.rename_files(file, len(str(len(self.files))), self.name, self.counter, sep, digit, n)
                        if new_name:
                            self.new_files.append(new_name)
                    else:
                        raise WrongSeparator('неверное имя сепаратора')
                    self.mysignal_rename.emit(file)  
                except Exception as e:
                    print(e)
                    # QMessageBox.warning(self.mw, 'Ошибка', 'Неизвестная ошибка')
                    break   
            self.mysignal_rename.emit(self.new_files) 
        
    
    def rename_files(self, i, lenfiles, name, counter, sep, digit, n):
        nulls = str(counter + digit) if n else str(counter + digit).zfill(lenfiles + 1 if lenfiles <= 1 else lenfiles)
        try:
            new_file_name = os.path.normpath(os.path.join(conf['PATH'], name + sep + nulls)) # просто название
            old_filename = '.'.join(i.split(os.extsep)[:-1]) # отдельно имя и расширение
            new_filename = new_file_name + '.' + i.split('.')[-1] # новое название файла с расширением
            os.rename(i, new_filename)
            if os.path.exists(os.path.normpath(old_filename + '.xmp')):
                os.rename(old_filename + '.xmp', new_file_name + '.xmp')
            # обрабатываем доп. джипег
            if self.rawjpg:
                jpeg = jpeg_finder2(os.path.basename(i))
                if jpeg:
                    ext = '.' + jpeg.split('.')[-1]
                    os.rename(jpeg, new_file_name + ext)
            counter += 1
            
            return [os.path.basename(new_filename), counter]
            
        except Exception as e:
            print(e)