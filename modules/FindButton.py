import re
import os
from modules.api import conf, load_key_to_api
from filters._ending_name import ending_name
from filters._natural_sort import natural_sort_key
from filters._raw_finder import raw_finder
from filters._jpeg_finder import jpeg_finder
from filters._check_formats import check_formats
from PyQt5.QtGui import QTextCursor
from modules.rename_example import RenameExample

splitter = re.compile(r'([,; \n\-]+(\s))|([,; \n\-]+)|(\s)')
chooser = re.compile(r'[a-zA-ZА-Яа-яёЁ\S]*[0]*[0-9]+(\.\w+)?')
choose_name = re.compile(r'(?P<name>[0]*[\d]+)(?P<ext>\.\w+\d)?')


class FindButton:
    '''
    Кнопка найти - сопоставляет набранные человеком цифры с фотографиями из указанной папки
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.pushButton_find.clicked.connect(self.find_photos)
        
    def find_photos(self):
        ch = self.mw.checkBox_rawjpg.checkState()
        ldir = self.all_folder([os.path.basename(i) for i in os.listdir(conf['PATH'])])
        td = self.get_textEdit()
        if len(td) == 0:
            self.mw.label_status.setText(f'Найдено: {len(ldir)} файлов в папке')
            self.mw.pushButton_enter.setEnabled(False)
            self.create_path_files(ldir)
        else:
            self.create_path_files(td)
            
    def create_path_files(self, td):
        ch = self.mw.checkBox_rawjpg.checkState()
        try:
            ldir = sorted([[re.findall(choose_name, i)[-1][0], jpeg_finder(i) if ch else i ] for i in os.listdir(conf['PATH']) 
                           if os.path.isfile(os.path.join(conf['PATH'],i)) 
                           and re.findall(choose_name, i)[-1][0] in td
                           and check_formats(i.split('.')[-1].lower()) 
                           and (not raw_finder(i) if ch else i)],  
                          key=lambda para: (natural_sort_key(para[0]), para[1]))
            self.mw.textEdit.clear()
            for i in sorted(ldir, key = lambda para: (para[1], para[0])):
                self.mw.textEdit.append(i[1])
            new_lst = self.get_textEdit()
            not_found = sorted([i for i in td if i not in new_lst], key=natural_sort_key)
            if len(ldir) != 0:
                self.mw.pushButton_enter.setEnabled(True)
            else:
                self.mw.pushButton_enter.setEnabled(False)
            if not_found:
                self.mw.textEdit.append('\n\n_____Не найдено:_____')
                for i in not_found:
                    self.mw.textEdit.append(i)
            self.mw.label_status.setText(f'Найдено: {ending_name(len(ldir))}')
            self.mw.renameExample.create_example()
        except Exception as e:
            print(e)
            
        

    def get_textEdit(self):
        try:
            td = self.mw.textEdit.toPlainText()
            td_split = re.split(splitter, td)
            split_text = [item for item in td_split if item != None and [p for p in item if p not in ',; \n']]
            choose_text = [re.findall('\d+', i.rsplit('.', 1)[0])[-1] for i in split_text if re.fullmatch(chooser, i)]
            return choose_text
        except Exception as e:
            print(e)
            
    
    def all_folder(self, td_split):
        try:
            split_text = [item for item in td_split if item != None and [p for p in item if p not in ',; \n']]
            choose_text = [re.findall('\d+', i.rsplit('.', 1)[0])[-1] for i in split_text 
                        if os.path.isfile(os.path.join(conf['PATH'],i)) 
                        and check_formats(i.split('.')[-1].lower())
                        and re.fullmatch(chooser, i) ]
            return choose_text
        except Exception as e:
            print(e)