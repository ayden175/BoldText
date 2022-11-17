import sys
import math
import os

from PyQt5 import QtWidgets, QtGui, uic
from pdfme import build_pdf
import tkinter
from tkinter import filedialog

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.setWindowIcon(QtGui.QIcon(self.resource_path('logo.png')))
        uic.loadUi(self.resource_path('bold_text.ui'), self)
        self.show()

        self.text_align.addItems(['Left', 'Center', 'Right', 'Justify'])
        self.save_file.clicked.connect(self.savePdf)

        self.document = {
            'style': {
                'margin_bottom': 50,
                'text_align': self.text_align.currentText()[0].lower(),
                's': self.font_size.value(),
                'page_numbering_style': 'arabic'
            },
            'formats': {
                "title": {"b": 1, "s": int(self.font_size.value() * 1.2)}
            },
            'running_sections': {
                "footer": {
                "x": "left", "y": 800, "height": "bottom", "style": {"text_align": "c", "s": min(self.font_size.value(), 10)},
                "content": [{".": [{"var": "$page"}]}]
                }
            }
        }

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # ---------------------- SAVE PDF ----------------------
    def savePdf(self):
        filename = self.selectFilename()
        if filename is None:
            return

        title = self.title.text()
        text = self.text_input.toPlainText()
        paragraphs = [self.boldPar(par) for par in text.split('\n') if par != '']       

        section = {'content': []}
        if self.page_numbers.isChecked():
            section['running_sections'] = ['footer']

        if title != '':
            section['content'].append({'.': title, 'style': 'title'})
        for par in paragraphs:
            section['content'].append(par)
        self.document['sections'] = [section]

        with open(filename, 'wb') as file:
            try:
                build_pdf(self.document, file)
                self.popup('Success', 'PDF saved successfully')
            except Exception as e:
                self.popup('Error', str(e), QtWidgets.QMessageBox.Critical)
                return

    def boldPar(self, par):
        result = []
        for word in par.split(' '):
            if len(word) < 2:
                result.append(word)
            elif len(word) == 3:
                result.append({'.b': word[0]})
                result.append(word[1:])
            else:
                bold_len = math.ceil(len(word) / 2)
                result.append({'.b': word[:bold_len]})
                result.append(word[bold_len:])
            result.append(' ')
        return result

    def selectFilename(self):
        path = filedialog.asksaveasfile(defaultextension=".pdf", filetypes=(("PDF Files", "*.pdf"),("All Files", "*.*") ))
        if path is None:
            return
        if path.name.endswith('.pdf'):
            return path.name
        else:
            return path.name + '.pdf'

    def popup(self, title, message, icon=QtWidgets.QMessageBox.Information):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

if __name__ == '__main__':
    tkinter.Tk().withdraw()
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
