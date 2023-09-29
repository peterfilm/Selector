from PyQt5.QtWidgets import QDialog
from data.peter import PeterUI


class PeterWindow(QDialog):
    '''
    Окошко об авторе
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.modal = PeterUI()
        self.modal.setupUi(self)
        self.setWindowModality(2)  # чтоб блокировало другие окна
