# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_asset_browser.ui'
#
# Created: Mon Jun 25 18:59:35 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AssetBrowser(object):
    def setupUi(self, AssetBrowser):
        AssetBrowser.setObjectName(_fromUtf8("AssetBrowser"))
        AssetBrowser.resize(590, 726)
        AssetBrowser.setWindowTitle(QtGui.QApplication.translate("AssetBrowser", "Assets", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(AssetBrowser)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_checkout = QtGui.QPushButton(self.centralwidget)
        self.btn_checkout.setEnabled(True)
        self.btn_checkout.setGeometry(QtCore.QRect(240, 510, 95, 31))
        self.btn_checkout.setAutoFillBackground(False)
        self.btn_checkout.setText(QtGui.QApplication.translate("AssetBrowser", "Check Out", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_checkout.setCheckable(False)
        self.btn_checkout.setAutoDefault(True)
        self.btn_checkout.setDefault(False)
        self.btn_checkout.setFlat(False)
        self.btn_checkout.setObjectName(_fromUtf8("btn_checkout"))
        self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 50, 241, 144))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_proj = QtGui.QLabel(self.formLayoutWidget)
        self.label_proj.setText(QtGui.QApplication.translate("AssetBrowser", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.label_proj.setObjectName(_fromUtf8("label_proj"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_proj)
        self.label_seq = QtGui.QLabel(self.formLayoutWidget)
        self.label_seq.setText(QtGui.QApplication.translate("AssetBrowser", "Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.label_seq.setObjectName(_fromUtf8("label_seq"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_seq)
        self.label_sh = QtGui.QLabel(self.formLayoutWidget)
        self.label_sh.setText(QtGui.QApplication.translate("AssetBrowser", "Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sh.setObjectName(_fromUtf8("label_sh"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_sh)
        self.combo_proj = QtGui.QComboBox(self.formLayoutWidget)
        self.combo_proj.setObjectName(_fromUtf8("combo_proj"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.combo_proj)
        self.combo_seq = QtGui.QComboBox(self.formLayoutWidget)
        self.combo_seq.setObjectName(_fromUtf8("combo_seq"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.combo_seq)
        self.combo_sh = QtGui.QComboBox(self.formLayoutWidget)
        self.combo_sh.setObjectName(_fromUtf8("combo_sh"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.combo_sh)
        self.combo_asset_type = QtGui.QComboBox(self.formLayoutWidget)
        self.combo_asset_type.setObjectName(_fromUtf8("combo_asset_type"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.combo_asset_type)
        self.label_asset_type = QtGui.QLabel(self.formLayoutWidget)
        self.label_asset_type.setText(QtGui.QApplication.translate("AssetBrowser", "Asset type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_asset_type.setObjectName(_fromUtf8("label_asset_type"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_asset_type)
        self.btn_checkin = QtGui.QPushButton(self.centralwidget)
        self.btn_checkin.setEnabled(True)
        self.btn_checkin.setGeometry(QtCore.QRect(40, 510, 95, 31))
        self.btn_checkin.setAutoFillBackground(False)
        self.btn_checkin.setText(QtGui.QApplication.translate("AssetBrowser", "Check In", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_checkin.setCheckable(False)
        self.btn_checkin.setAutoDefault(True)
        self.btn_checkin.setDefault(False)
        self.btn_checkin.setFlat(False)
        self.btn_checkin.setObjectName(_fromUtf8("btn_checkin"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(330, 90, 256, 192))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.btn_cancel = QtGui.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(460, 520, 95, 31))
        self.btn_cancel.setText(QtGui.QApplication.translate("AssetBrowser", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(30, 230, 256, 192))
        self.treeView.setObjectName(_fromUtf8("treeView"))
        AssetBrowser.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AssetBrowser)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 590, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AssetBrowser.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AssetBrowser)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AssetBrowser.setStatusBar(self.statusbar)

        self.retranslateUi(AssetBrowser)
        QtCore.QMetaObject.connectSlotsByName(AssetBrowser)

    def retranslateUi(self, AssetBrowser):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AssetBrowser = QtGui.QMainWindow()
    ui = Ui_AssetBrowser()
    ui.setupUi(AssetBrowser)
    AssetBrowser.show()
    sys.exit(app.exec_())

