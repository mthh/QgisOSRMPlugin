# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'osrm_batch_route_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OsrmBatchRouteDialog(object):
    def setupUi(self, OsrmBatchRouteDialog):
        OsrmBatchRouteDialog.setObjectName("OsrmBatchRouteDialog")
        OsrmBatchRouteDialog.resize(450, 410)
        self.label_subtitle = QtWidgets.QLabel(OsrmBatchRouteDialog)
        self.label_subtitle.setGeometry(QtCore.QRect(80, 10, 281, 20))
        self.label_subtitle.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_subtitle.setFont(font)
        self.label_subtitle.setObjectName("label_subtitle")
        self.layoutWidget = QtWidgets.QWidget(OsrmBatchRouteDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 260, 391, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonRun = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonRun.setFont(font)
        self.pushButtonRun.setObjectName("pushButtonRun")
        self.gridLayout.addWidget(self.pushButtonRun, 2, 0, 1, 1)
        self.pushButtonReverse = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButtonReverse.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setKerning(True)
        self.pushButtonReverse.setFont(font)
        self.pushButtonReverse.setDefault(False)
        self.pushButtonReverse.setFlat(False)
        self.pushButtonReverse.setObjectName("pushButtonReverse")
        self.gridLayout.addWidget(self.pushButtonReverse, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.check_add_layer = QtWidgets.QCheckBox(self.layoutWidget)
        self.check_add_layer.setMaximumSize(QtCore.QSize(210, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.check_add_layer.setFont(font)
        self.check_add_layer.setAutoFillBackground(False)
        self.check_add_layer.setChecked(True)
        self.check_add_layer.setObjectName("check_add_layer")
        self.gridLayout.addWidget(self.check_add_layer, 0, 0, 1, 1)
        self.pushButton_about = QtWidgets.QPushButton(OsrmBatchRouteDialog)
        self.pushButton_about.setGeometry(QtCore.QRect(10, 370, 85, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton_about.setFont(font)
        self.pushButton_about.setObjectName("pushButton_about")
        self.close_button_box = QtWidgets.QDialogButtonBox(OsrmBatchRouteDialog)
        self.close_button_box.setGeometry(QtCore.QRect(335, 370, 101, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.close_button_box.setFont(font)
        self.close_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.close_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.close_button_box.setObjectName("close_button_box")
        self.line = QtWidgets.QFrame(OsrmBatchRouteDialog)
        self.line.setEnabled(True)
        self.line.setGeometry(QtCore.QRect(10, 110, 431, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget1 = QtWidgets.QWidget(OsrmBatchRouteDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 130, 391, 131))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 3, 0, 1, 1)
        self.pushButtonBrowse = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonBrowse.setFont(font)
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.gridLayout_3.addWidget(self.pushButtonBrowse, 3, 2, 1, 1)
        self.lineEdit_output = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_output.setText("")
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.gridLayout_3.addWidget(self.lineEdit_output, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)
        self.lineEdit_profileName = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_profileName.setFont(font)
        self.lineEdit_profileName.setObjectName("lineEdit_profileName")
        self.gridLayout_3.addWidget(self.lineEdit_profileName, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 2, 1, 1, 1)
        self.lineEdit_host = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.gridLayout_3.addWidget(self.lineEdit_host, 0, 1, 1, 2)
        self.frame_pts_layer = QtWidgets.QFrame(OsrmBatchRouteDialog)
        self.frame_pts_layer.setEnabled(True)
        self.frame_pts_layer.setGeometry(QtCore.QRect(30, 50, 391, 49))
        self.frame_pts_layer.setObjectName("frame_pts_layer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_pts_layer)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame_pts_layer)
        self.label_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.ComboBoxDestination = gui.QgsMapLayerComboBox(self.frame_pts_layer)
        self.ComboBoxDestination.setEnabled(True)
        self.ComboBoxDestination.setMinimumSize(QtCore.QSize(0, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.ComboBoxDestination.setFont(font)
        self.ComboBoxDestination.setObjectName("ComboBoxDestination")
        self.gridLayout_2.addWidget(self.ComboBoxDestination, 1, 1, 1, 1)
        self.ComboBoxOrigin = gui.QgsMapLayerComboBox(self.frame_pts_layer)
        self.ComboBoxOrigin.setEnabled(True)
        self.ComboBoxOrigin.setMinimumSize(QtCore.QSize(0, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.ComboBoxOrigin.setFont(font)
        self.ComboBoxOrigin.setObjectName("ComboBoxOrigin")
        self.gridLayout_2.addWidget(self.ComboBoxOrigin, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_pts_layer)
        self.label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.pushButton_about.raise_()
        self.close_button_box.raise_()
        self.label_subtitle.raise_()
        self.frame_pts_layer.raise_()
        self.line.raise_()

        self.retranslateUi(OsrmBatchRouteDialog)
        self.close_button_box.accepted.connect(OsrmBatchRouteDialog.accept)
        self.close_button_box.rejected.connect(OsrmBatchRouteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OsrmBatchRouteDialog)

    def retranslateUi(self, OsrmBatchRouteDialog):
        _translate = QtCore.QCoreApplication.translate
        OsrmBatchRouteDialog.setWindowTitle(_translate("OsrmBatchRouteDialog", "OSRM"))
        self.label_subtitle.setToolTip(_translate("OsrmBatchRouteDialog", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_subtitle.setText(_translate("OsrmBatchRouteDialog", "<html><head/><body><p align=\"center\">Batch OSRM viaroute</p></body></html>"))
        self.pushButtonRun.setText(_translate("OsrmBatchRouteDialog", "Compute and save the result"))
        self.pushButtonReverse.setText(_translate("OsrmBatchRouteDialog", "Reverse O/D"))
        self.check_add_layer.setText(_translate("OsrmBatchRouteDialog", "Add the result to the canvas"))
        self.pushButton_about.setText(_translate("OsrmBatchRouteDialog", "About.."))
        self.label_11.setText(_translate("OsrmBatchRouteDialog", "Output file"))
        self.pushButtonBrowse.setText(_translate("OsrmBatchRouteDialog", "Browse"))
        self.label_10.setText(_translate("OsrmBatchRouteDialog", "Host"))
        self.lineEdit_profileName.setText(_translate("OsrmBatchRouteDialog", "v1/driving"))
        self.label_3.setText(_translate("OsrmBatchRouteDialog", "Profile"))
        self.lineEdit_host.setText(_translate("OsrmBatchRouteDialog", "http://127.0.0.1:5000/"))
        self.label_2.setText(_translate("OsrmBatchRouteDialog", "<html><head/><body><p align=\"center\">Destination layer</p></body></html>"))
        self.label.setText(_translate("OsrmBatchRouteDialog", "<html><head/><body><p align=\"center\">Origin layer</p></body></html>"))

from qgis import gui
