import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from ui_asset_browser import Ui_AssetBrowser
# huy 2
class AssetBrowserMain(QMainWindow, Ui_AssetBrowser):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #self.button2.clicked.connect(self.fill)

    def fill(self):
        button=self.sender()
        print button.text()
        self = self.label.setText("text")
    
if __name__ == "__main__":
    import sys
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtGui import *

    app = QtGui.QApplication(sys.argv)
    window = AssetBrowserMain()
    window.show()
    sys.exit(app.exec_())