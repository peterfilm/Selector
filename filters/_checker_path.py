from modules.api import conf, load_key_to_api
import os


class Checker:
    ENABLER = 0
    '''
    Проверяем путь
    '''

    def disabler(self, value):
        '''
        Если нет пути к папке - блокирует все кнопки
        '''
        # self.comboBox_rating.setEnabled(value)
        self.comboBox_color.setEnabled(value)
        self.checkBox_rename.setEnabled(value)
        self.checkBox_dir.setEnabled(value)
        self.pushButton_find.setEnabled(value)
        self.lineEdit_files.setText(conf['PATH'])
        self.rating.setEnabled(value)

    def check_path(self, path):
        '''
        проверяем есть ли такой путь какой был указан
        '''
        if os.path.exists(path):
            return True
        else:
            return False

    def check_in_conf(self):
        '''
        Проверяем есть ли путь в конфе
        '''
        if conf['PATH']:
            Checker.ENABLER = 1
            Checker.disabler(self, Checker.ENABLER)
        else:
            Checker.ENABLER = 0
            Checker.disabler(self, Checker.ENABLER)
