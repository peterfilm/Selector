class ComboColor:
    '''
    Выбор цветовой метки
    '''

    def __init__(self, main_window):
        self.mw = main_window

        self.colors = {
            "Выбрать цветовую метку": "",
            "Red (красный)": "#7c1212",
            "Yellow (желтый)": "#ffc000",
            "Green (зеленый)": "#2e8f2e",
            "Blue (синий)": "#2b2bad",
            "Purple (пурпурный)": "#c253c2",
            "Cyan (циановый)": "#65b1b1",
            "Brown (коричневый)": "#4d3915",
            "Trash (серый)": "#3e3f43",
        }

        self.mw.comboBox_color.currentTextChanged.connect(self.text_changed)

    def text_changed(self):
        new_color = '{ background: ' + \
            str(self.colors[self.mw.comboBox_color.currentText()]) + '; '
        if self.mw.comboBox_color.currentText() in ['Trash (серый)', 'Blue (синий)', 'Red (красный)', 'Brown (коричневый)']:
            text_color = '#ffffff'
        elif self.mw.comboBox_color.currentText() == "Выбрать цветовую метку":
            text_color = ''
        else:
            text_color = '#000000'
        new_color += f'color: {text_color}' + ' }'
        self.mw.comboBox_color.setStyleSheet(f'QComboBox {new_color}')
