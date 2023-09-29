import sys
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QColor
from modules.api import conf


class CustomComboBox(QComboBox):
    def __init__(self):
        super().__init__()

        model = QStandardItemModel()
        self.setModel(model)

        # Add items with names and colors
        self.addItem("Выбрать цветовую метку")

        self.addItem(f"{conf['LABELS']['1']} (красный)")
        self.setItemColor(1, QColor(124, 18, 18))

        # Add items with names and colors
        self.addItem(f"{conf['LABELS']['2']} (желтый)")
        self.setItemColor(2, QColor(255, 192, 0))

        self.addItem(f"{conf['LABELS']['3']} (зеленый)")
        self.setItemColor(3, QColor(46, 143, 46))

        self.addItem(f"{conf['LABELS']['4']} (синий)")
        self.setItemColor(4, QColor(43, 43, 173))
        
        self.addItem(f"{conf['LABELS']['5']} (пурпурный)")
        self.setItemColor(5, QColor(194, 83, 194))
        
        self.addItem(f"{conf['LABELS']['6']} (циановый)")
        self.setItemColor(6, QColor(101, 177, 177))
        
        self.addItem(f"{conf['LABELS']['7']} (коричневый)")
        self.setItemColor(7, QColor(77, 57, 21))

        self.addItem(f"{conf['LABELS']['8']} (серый)")
        self.setItemColor(8, QColor(62, 63, 67))

    def setItemColor(self, index, color):
        item = self.model().item(index)
        if item:
            item.setData(color, Qt.BackgroundRole)
            if item.text() in [f"{conf['LABELS']['8']} (серый)", f'{conf["LABELS"]["4"]} (синий)', f'{conf["LABELS"]["1"]} (красный)', f'{conf["LABELS"]["7"]} (коричневый)']:
                item.setForeground(QColor(255, 255, 255))
            else:
                item.setForeground(QColor(0, 0, 0))
