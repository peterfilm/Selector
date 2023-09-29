from PyQt5.QtCore import QThread, pyqtSignal
from modules.api import conf
import os
import pyexiv2
import xml.etree.ElementTree as ET
import re
from filters._jpeg_finder import jpeg_finder2


class ChangeMetaData(QThread):
    mysignal = pyqtSignal(object)

    def __init__(self, files, rating=None, label=None, parent=None):
        QThread.__init__(self, parent)
        self.files = files
        self.rating = rating
        self.label = label
        self.running = True

    def run(self):  # обязательный для потоков метод
        for i in self.files:
            # CТАВИМ РЕЙТИНГ
            
            # простые форматы с вшитым xmp
            if self.running:
                if i.split('.')[-1].lower() in conf['SIMPLE_FORMATS']:
                    self.simple_files(i)
                else:
                    # рав-форматы
                    if os.path.exists(os.path.splitext(i)[0] + ".xmp"):
                        self.raw_with_xmp(i)
                    else:
                        self.raw_without_xmp(i)
                    jpeg = jpeg_finder2(os.path.basename(i))
                    if jpeg:
                        self.simple_files(jpeg)
                self.mysignal.emit(i)
                    
    
    def raw_with_xmp(self, i):
        # рейтинг и лейбел, если у рава есть xmp
        xmp_file_name = os.path.splitext(i)[0] + ".xmp"
        self.change_xmp_file(xmp_file_name, self.rating, self.label)
        
    def raw_without_xmp(self, i):
        # рейтинг и лейбел, если у рава нет xmp
        self.create_xmp_file(i)
    
    def simple_files(self, i):
        # рейтинг и лейбел, если простой формат с вшитым xmp
        try:
            old_path = os.getcwd()
            os.chdir(os.path.dirname(os.path.realpath(i)))
            img=pyexiv2.Image(os.path.basename(i), encoding='utf-8')
            img.modify_xmp({'Xmp.xmp.Rating': self.rating})
            if self.label:
                img.modify_xmp({'Xmp.xmp.Label': conf['LABELS'][str(self.label)]})
            else:
                img.modify_xmp({'Xmp.xmp.Label': ''})
            img.close()
            os.chdir(old_path)
        except Exception as e:
            os.chdir(old_path)
            print(e)
        
    def create_xmp_file(self, file_path):
        # создать xmp файл для рава
        try:
            xmp_file_name = os.path.splitext(file_path)[0] + ".xmp"
            
            xmp_root = ET.Element("{adobe:ns:meta/}xmpmeta")
            xmp_root.set("xmlns:x", "adobe:ns:meta/")
            xmp_root.set("x:xmptk", "XMP Core 5.6.0")
            
            rdf_rdf = ET.SubElement(xmp_root, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")
            rdf_description = ET.SubElement(rdf_rdf, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
            rdf_description.set("xmlns:photoshop", "http://ns.adobe.com/photoshop/1.0/")
            rdf_description.set("xmlns:xmp", "http://ns.adobe.com/xap/1.0/")
            rdf_description.set("xmp:Rating", str(self.rating))
            if self.label:
                rdf_description.set("xmp:Label", str(conf['LABELS'][str(self.label)]))
            else:
                rdf_description.set("xmp:Label", '')
            tree = ET.ElementTree(xmp_root)
            tree.write(xmp_file_name, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            print(e)           
        
    def change_xmp_file(self, xmp_file_path, rating=None, label=None):
        # изменить xmp file, если он уже существует
        with open(xmp_file_path, "r") as xmp_file:
            xmp_text = xmp_file.read()
            
        new_rating = f'xmp:Rating'
        if re.search(new_rating, xmp_text):
            new_rating = f'xmp:Rating="{self.rating}"'
            xmp_text = re.sub(r'xmp:Rating="\d+"', new_rating, xmp_text)
        else:
            create_date = re.search(r'xmp:CreateDate="\S+"', xmp_text)[0]
            new_rating = create_date + f'\n   xmp:Rating="{self.rating}"'
            xmp_text = re.sub(r'xmp:CreateDate="\S+"', new_rating, xmp_text)
            
        changed_label = conf['LABELS'][str(self.label)] if self.label else ''
        
        new_label = f'xmp:Label'
        if re.search(new_label, xmp_text):
            new_label = f'xmp:Label="{changed_label}"'
            xmp_text = re.sub(r'xmp:Label="\w*"', new_label, xmp_text)
        else:
            create_date = re.search(r'xmp:CreateDate="\S+"', xmp_text)[0]
            new_label = create_date + f'\n   xmp:Label="{changed_label}"'
            xmp_text = re.sub(r'xmp:CreateDate="\S+"', new_label, xmp_text)
        try:
            with open(xmp_file_path, "w") as xmp_file:
                xmp_file.write(xmp_text)
        except Exception as e:
            print(e)