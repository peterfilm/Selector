from modules.api import conf
import re

class RenameExample:
    '''
    Пример того как будет выглядеть переименованный текст
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.lineEdit_rename.textChanged.connect(self.change)
        self.mw.lineEdit_sep.textChanged.connect(self.change)
        self.mw.lineEdit_digit.textChanged.connect(self.change)
        self.mw.comboBox_nulls.currentIndexChanged.connect(self.change)
        self.example = None
        
    def change(self):
        name = self.mw.lineEdit_rename.text()
        separator = self.mw.lineEdit_sep.text()
        txt_count = len(str(len(self.mw.textEdit.toPlainText().split('\n\n_____Не найдено:_____')[0].split())))
        nulls = 1 if self.mw.comboBox_nulls.currentIndex() else txt_count + 1 if txt_count <= 1 else txt_count
        digit = self.mw.lineEdit_digit.text() if self.mw.lineEdit_digit.text() else '1'
        if self.example:
            self.mw.label_newName.setText(self.example + '   ->   '+ name + separator + digit.zfill(nulls) + '.' + self.example.split('.')[-1])
        else:
            self.mw.label_newName.setText(name + separator + digit.zfill(nulls))
            
    def create_example(self):
        self.example = self.mw.textEdit.toPlainText().split()[0]
        