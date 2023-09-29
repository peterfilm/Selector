from PyQt5.QtWidgets import QApplication, QWidget
import sys
from PyQt5.QtGui import QIcon
from data.design import Ui_Selector
from modules import *
import os

class Selector(QWidget, Ui_Selector):
    '''
    Программа для выборки фотографий на ретушь от клиентов
    '''

    def __init__(self):
        super().__init__()
        # грузим qss в файл
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            qss_file_path = os.path.join(script_dir, "style.qss")
            with open(qss_file_path, "r") as qss_file:
                qss_content = qss_file.read()

            # Apply the QSS to your application
            self.setStyleSheet(qss_content)
        except Exception as e:
            print(e)
        self.setupUi(self)
        
        icon = QIcon(os.path.join("img", "icon.ico"))
        self.setWindowIcon(icon)

        self.show()
        
        self.pushButton_cancel.hide()
        self.combocolor = ComboColor(self)
        self.select_folder = SelectFolder(self)
        self.comborating = ComboRating(self)
        self.findButton = FindButton(self)
        self.enterButton = EnterButton(self)
        self.rename = RenameButton(self)
        self.sep = Separator(self)
        self.digit = FromDigit(self)
        self.tEdit = TextEdit(self)
        self.renameExample = RenameExample(self)
        self.openBtn = OpenButton(self)
        self.change_dir = ChangeDir(self)
        self.copy_move_button = CopyMoveButton(self)

        # кнопки
        self.pushButton_about.clicked.connect(self.open_modal_author)

    def open_modal_author(self):
        modal_dialog = PeterWindow(self)
        modal_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Selector()

    window.show()
    sys.exit(app.exec_())
