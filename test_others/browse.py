import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QFileDialog,QPushButton
from PyQt5 import uic,QtGui,QtCore,QtSql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QSizeF

import sqlite3
import os
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog
from jinja2 import Template    

class Browse(QDialog):
    def __init__(self,p='',parent=None):
        super().__init__()
        uic.loadUi('./ui/browse.ui', self)
        self.setWindowIcon(QtGui.QIcon("./images/carti.png"))
        self.setWindowTitle("Easy Pos Software By Best Solution Online")
        self.browse.clicked.connect(self.browsingIm)
        self.image=''
        self.saveimg.clicked.connect(self.save)
        self.print.clicked.connect(self.print_file)
        self.printPreview.clicked.connect(self.print_preview_dialog)
        #self.textEdit.hide()
        self.textEdit.setStyleSheet("background:black")
        self.rows = [["1", "Maik", "Mustermann"],
        ["2", "Tom", "Jerry"],
        ["3", "Jonny", "Brown"]]

        #with open("html/purchaseinvoice.html") as file:
            #self.textEdit.setText(Template(file.read()).render( rows=self.rows))


    def browsingIm(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Image File', r"","Image files (*.jpg *.gif *.png *.svg *.jpeg *.ico)")
        self.label.setPixmap(QPixmap(fname[0]))
        self.image=fname[0]

    def save(self):
        file_name = os.path.basename(self.image)
        #extension = os.path.splitext(file_name)[1]
        img = Image.open(self.image)
        img.save("./uploads/{}".format(file_name))

    #print dialog method
    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    #these methods are for print preview dialog
    def print_preview_dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QSizeF(210, 297), QPrinter.Millimeter)
        printer.setResolution(600)
        printer.setPageMargins(0,0,0,0,6)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()
    def print_preview(self, printer):
        self.textEdit.print_(printer)


   
if __name__=="__main__":
    app = QApplication(sys.argv)
    data = Browse()
    data.show()
    sys.exit(app.exec_())  