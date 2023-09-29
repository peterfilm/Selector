from modules.api import conf
from filters._ending_name import ending_name

class TextEdit:
    '''
    Поле для ввода номеров файлов
    '''

    def __init__(self, main_window):
        self.mw = main_window
        self.mw.textEdit.textChanged.connect(self.is_empty)
        self.mw.textEdit.textChanged.connect(self.changed_text)
        
    def is_empty(self):
        if not self.mw.textEdit.toPlainText():
            self.mw.pushButton_enter.setEnabled(False)
        if self.mw.textEdit.toPlainText():
            self.mw.renameExample.create_example()
            
    def changed_text(self):
        text = self.mw.textEdit.toPlainText().split('\n\n_____Не найдено:_____')[0].split()
        if not text:
            self.mw.label_status.setText(f'Нажмите найти')
        else:
            self.mw.label_status.setText(f'Выбрано: {ending_name(len(text))}')