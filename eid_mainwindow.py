# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_EID.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_7 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget_2 = QtGui.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.btn_load_target = QtGui.QPushButton(self.layoutWidget_2)
        self.btn_load_target.setMinimumSize(QtCore.QSize(1, 0))
        self.btn_load_target.setObjectName(_fromUtf8("btn_load_target"))
        self.gridLayout_3.addWidget(self.btn_load_target, 1, 3, 1, 1)
        self.btn_reorder_pics = QtGui.QPushButton(self.layoutWidget_2)
        self.btn_reorder_pics.setMinimumSize(QtCore.QSize(10, 0))
        self.btn_reorder_pics.setObjectName(_fromUtf8("btn_reorder_pics"))
        self.gridLayout_3.addWidget(self.btn_reorder_pics, 0, 3, 1, 1)
        self.scrl_features_2 = QtGui.QScrollArea(self.layoutWidget_2)
        self.scrl_features_2.setWidgetResizable(True)
        self.scrl_features_2.setObjectName(_fromUtf8("scrl_features_2"))
        self.scrlw_features_2 = QtGui.QWidget()
        self.scrlw_features_2.setGeometry(QtCore.QRect(0, 0, 697, 440))
        self.scrlw_features_2.setObjectName(_fromUtf8("scrlw_features_2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.scrlw_features_2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.treeView = QtGui.QTreeView(self.scrlw_features_2)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout_5.addWidget(self.treeView, 1, 0, 1, 1)
        self.scrl_features_2.setWidget(self.scrlw_features_2)
        self.gridLayout_3.addWidget(self.scrl_features_2, 4, 1, 1, 6)
        self.btn_clear_filter = QtGui.QPushButton(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clear_filter.sizePolicy().hasHeightForWidth())
        self.btn_clear_filter.setSizePolicy(sizePolicy)
        self.btn_clear_filter.setObjectName(_fromUtf8("btn_clear_filter"))
        self.gridLayout_3.addWidget(self.btn_clear_filter, 0, 4, 1, 1)
        self.btn_apply_filter = QtGui.QPushButton(self.layoutWidget_2)
        self.btn_apply_filter.setObjectName(_fromUtf8("btn_apply_filter"))
        self.gridLayout_3.addWidget(self.btn_apply_filter, 0, 5, 1, 1)
        self.btn_unhide_all = QtGui.QPushButton(self.layoutWidget_2)
        self.btn_unhide_all.setObjectName(_fromUtf8("btn_unhide_all"))
        self.gridLayout_3.addWidget(self.btn_unhide_all, 1, 5, 1, 1)
        self.btn_hide_all = QtGui.QPushButton(self.layoutWidget_2)
        self.btn_hide_all.setObjectName(_fromUtf8("btn_hide_all"))
        self.gridLayout_3.addWidget(self.btn_hide_all, 1, 4, 1, 1)
        self.label_target = QtGui.QLabel(self.layoutWidget_2)
        self.label_target.setText(_fromUtf8(""))
        self.label_target.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_target.setObjectName(_fromUtf8("label_target"))
        self.gridLayout_3.addWidget(self.label_target, 2, 2, 1, 4)
        self.scrollArea_2 = QtGui.QScrollArea(self.splitter)
        self.scrollArea_2.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setAutoFillBackground(True)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrlw = QtGui.QWidget()
        self.scrlw.setGeometry(QtCore.QRect(0, 0, 73, 535))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrlw.sizePolicy().hasHeightForWidth())
        self.scrlw.setSizePolicy(sizePolicy)
        self.scrlw.setObjectName(_fromUtf8("scrlw"))
        self.gridLayout_6 = QtGui.QGridLayout(self.scrlw)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.scrollArea_2.setWidget(self.scrlw)
        self.gridLayout_7.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_load_target.setText(_translate("MainWindow", "Load Target", None))
        self.btn_reorder_pics.setText(_translate("MainWindow", "Reorder Images", None))
        self.btn_clear_filter.setText(_translate("MainWindow", "Clear Filter", None))
        self.btn_apply_filter.setText(_translate("MainWindow", "Apply FIlter", None))
        self.btn_unhide_all.setText(_translate("MainWindow", "Unhide All", None))
        self.btn_hide_all.setText(_translate("MainWindow", "Hide Matches", None))

