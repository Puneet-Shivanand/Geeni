import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os.path import abspath
import backend

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Geeni"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        mylabel = QLabel("Please input your 23andMe text file for processing.", self)
        mylabel.setFont(QFont("sansSerif", 18, weight=73))
        mylabel.setStyleSheet("color: rgb(32, 194, 14)") #Hacker green color
        mylabel.resize(1000, 60)
        mylabel.move(500, 100)

        self.create_menu_bar()
        self.showMaximized()

    def create_menu_bar(self):
        file_dialog = QAction("Input File", self)
        file_dialog.setShortcut("Ctrl+F")
        file_dialog.setStatusTip("Input file to be analyzed")
        file_dialog.triggered.connect(lambda: self.openningFiles())

        exit = QAction("Exit", self)
        exit.setShortcut("Ctrl+W")
        exit.setStatusTip("Exit the program")
        exit.triggered.connect(QCoreApplication.instance().quit)

        programinfo = QAction("Information", self)
        programinfo.setShortcut("Ctrl+I")
        programinfo.setStatusTip("Learn how to use this program")
        programinfo.triggered.connect(lambda: self.showInfo()) #Make this open a file with instructions


        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(file_dialog)
        file_menu.addAction(exit)

        about_menu = menu_bar.addMenu("&About")
        about_menu.addAction(programinfo)

    def showInfo(self):
        with open("readme.txt") as myfile:
            text = myfile.read()
            label = QLabel(text, self)
            label.resize(1000, 1000)
            label.move(550, 50)
            label.setFont(QFont("sansSerif", 12))
            label.setStyleSheet("color: rgb(255, 255, 255)")
            label.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options() if QFileDialog.Options() else QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            global filePath
            filePath = abspath(fileName)
            return filePath

    def create_results_window(self):
        self.newWindow = ResultsWindow(self)
        self.newWindow.closed.connect(self.show)
        self.newWindow.showMaximized()
        self.hide()

    def openningFiles(self):
        filePath = self.openFileNameDialog()
        if filePath:
            # user_input is a tuple of form ("[input]", True)
            global user_input
            user_input = QInputDialog.getText(self, "Condition", "Enter the genetic condition EXACTLY as it would appear on SNPedia:")
            self.create_results_window()

class ResultsWindow(QMainWindow): #Maybe make it a QMainWindow?

    closed = pyqtSignal()

    def __init__(self, parent=None):
        super(ResultsWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Geeni Results")

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.resultsDisplay()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def resultsDisplay(self):
        geneInfo = backend.genePageScraper(user_input[0], filePath)
        # mydict = {i+1:geneInfo[i] for i in range(len(geneInfo))}

        # Putting the information into a QLabel format
        bigstring = ""
        headers = ["RSID", "Chromosome", "Genotype", "Magnitude", "Summary"]
        bigstring += "Results are in the form: " + str(headers) + "\n"*2
        for sublist in geneInfo:
            bigstring += str(sublist) + "\n"

        resultsLabel = QLabel(bigstring, self)
        resultsLabel.setFont(QFont("sansSerif", 18))
        resultsLabel.setStyleSheet("color: rgb(255, 255, 255)")
        resultsLabel.resize(2000, 1000)
        resultsLabel.move(100, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
