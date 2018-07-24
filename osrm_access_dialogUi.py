# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'osrm_access_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OsrmAccessDialog(object):
    def setupUi(self, OsrmAccessDialog):
        OsrmAccessDialog.setObjectName("OsrmAccessDialog")
        OsrmAccessDialog.resize(448, 451)
        font = QtGui.QFont()
        font.setPointSize(8)
        OsrmAccessDialog.setFont(font)
        self.label_subtitle = QtWidgets.QLabel(OsrmAccessDialog)
        self.label_subtitle.setGeometry(QtCore.QRect(40, 10, 361, 20))
        self.label_subtitle.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_subtitle.setFont(font)
        self.label_subtitle.setObjectName("label_subtitle")
        self.pushButton_about = QtWidgets.QPushButton(OsrmAccessDialog)
        self.pushButton_about.setGeometry(QtCore.QRect(10, 420, 85, 27))
        self.pushButton_about.setObjectName("pushButton_about")
        self.close_button_box = QtWidgets.QDialogButtonBox(OsrmAccessDialog)
        self.close_button_box.setGeometry(QtCore.QRect(260, 420, 176, 27))
        self.close_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.close_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.close_button_box.setObjectName("close_button_box")
        self.layoutWidget = QtWidgets.QWidget(OsrmAccessDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 411, 171))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.textBrowser_nb_centers = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_nb_centers.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_nb_centers.sizePolicy().hasHeightForWidth())
        self.textBrowser_nb_centers.setSizePolicy(sizePolicy)
        self.textBrowser_nb_centers.setMaximumSize(QtCore.QSize(16777215, 24))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBrowser_nb_centers.setPalette(palette)
        font = QtGui.QFont()
        font.setItalic(False)
        self.textBrowser_nb_centers.setFont(font)
        self.textBrowser_nb_centers.setOverwriteMode(True)
        self.textBrowser_nb_centers.setObjectName("textBrowser_nb_centers")
        self.gridLayout_2.addWidget(self.textBrowser_nb_centers, 6, 1, 1, 1)
        self.pushButtonOrigin = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButtonOrigin.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButtonOrigin.setFont(font)
        self.pushButtonOrigin.setObjectName("pushButtonOrigin")
        self.gridLayout_2.addWidget(self.pushButtonOrigin, 5, 0, 1, 1)
        self.lineEdit_xyO = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_xyO.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        self.lineEdit_xyO.setFont(font)
        self.lineEdit_xyO.setObjectName("lineEdit_xyO")
        self.gridLayout_2.addWidget(self.lineEdit_xyO, 5, 1, 1, 1)
        self.toolButton_poly = QtWidgets.QToolButton(self.layoutWidget)
        self.toolButton_poly.setEnabled(False)
        self.toolButton_poly.setObjectName("toolButton_poly")
        self.gridLayout_2.addWidget(self.toolButton_poly, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 4, 1, 1, 1)
        self.comboBox_pointlayer = gui.QgsMapLayerComboBox(self.layoutWidget)
        self.comboBox_pointlayer.setEnabled(False)
        self.comboBox_pointlayer.setObjectName("comboBox_pointlayer")
        self.gridLayout_2.addWidget(self.comboBox_pointlayer, 2, 1, 1, 1)
        self.checkBox_selectedFt = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_selectedFt.setEnabled(False)
        self.checkBox_selectedFt.setObjectName("checkBox_selectedFt")
        self.gridLayout_2.addWidget(self.checkBox_selectedFt, 3, 1, 1, 1)
        self.comboBox_method = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.comboBox_method.setFont(font)
        self.comboBox_method.setObjectName("comboBox_method")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_method, 0, 0, 1, 3)
        self.layoutWidget1 = QtWidgets.QWidget(OsrmAccessDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 220, 411, 192))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonClear = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButtonClear.setFont(font)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.gridLayout_3.addWidget(self.pushButtonClear, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.pushButton_fetch = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_fetch.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_fetch.setFont(font)
        self.pushButton_fetch.setObjectName("pushButton_fetch")
        self.gridLayout_3.addWidget(self.pushButton_fetch, 3, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.spinBox_max = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_max.setMinimum(20)
        self.spinBox_max.setMaximum(80)
        self.spinBox_max.setSingleStep(2)
        self.spinBox_max.setProperty("value", 60)
        self.spinBox_max.setObjectName("spinBox_max")
        self.gridLayout.addWidget(self.spinBox_max, 2, 1, 1, 1)
        self.spinBox_intervall = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_intervall.setMinimum(2)
        self.spinBox_intervall.setMaximum(20)
        self.spinBox_intervall.setSingleStep(2)
        self.spinBox_intervall.setProperty("value", 10)
        self.spinBox_intervall.setObjectName("spinBox_intervall")
        self.gridLayout.addWidget(self.spinBox_intervall, 3, 1, 1, 1)
        self.labem_host = QtWidgets.QLabel(self.layoutWidget1)
        self.labem_host.setObjectName("labem_host")
        self.gridLayout.addWidget(self.labem_host, 0, 0, 1, 1)
        self.lineEdit_host = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_host.setFont(font)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.gridLayout.addWidget(self.lineEdit_host, 0, 1, 1, 1)
        self.lineEdit_profileName = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_profileName.setFont(font)
        self.lineEdit_profileName.setObjectName("lineEdit_profileName")
        self.gridLayout.addWidget(self.lineEdit_profileName, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.pushButton_about.raise_()
        self.close_button_box.raise_()
        self.label_subtitle.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(OsrmAccessDialog)
        self.close_button_box.accepted.connect(OsrmAccessDialog.accept)
        self.close_button_box.rejected.connect(OsrmAccessDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OsrmAccessDialog)
        OsrmAccessDialog.setTabOrder(self.comboBox_method, self.comboBox_pointlayer)
        OsrmAccessDialog.setTabOrder(self.comboBox_pointlayer, self.checkBox_selectedFt)
        OsrmAccessDialog.setTabOrder(self.checkBox_selectedFt, self.pushButtonOrigin)
        OsrmAccessDialog.setTabOrder(self.pushButtonOrigin, self.lineEdit_xyO)
        OsrmAccessDialog.setTabOrder(self.lineEdit_xyO, self.toolButton_poly)
        OsrmAccessDialog.setTabOrder(self.toolButton_poly, self.textBrowser_nb_centers)
        OsrmAccessDialog.setTabOrder(self.textBrowser_nb_centers, self.lineEdit_host)
        OsrmAccessDialog.setTabOrder(self.lineEdit_host, self.spinBox_max)
        OsrmAccessDialog.setTabOrder(self.spinBox_max, self.spinBox_intervall)
        OsrmAccessDialog.setTabOrder(self.spinBox_intervall, self.pushButtonClear)
        OsrmAccessDialog.setTabOrder(self.pushButtonClear, self.pushButton_fetch)
        OsrmAccessDialog.setTabOrder(self.pushButton_fetch, self.close_button_box)
        OsrmAccessDialog.setTabOrder(self.close_button_box, self.pushButton_about)

    def retranslateUi(self, OsrmAccessDialog):
        _translate = QtCore.QCoreApplication.translate
        OsrmAccessDialog.setWindowTitle(_translate("OsrmAccessDialog", "OSRM"))
        self.label_subtitle.setToolTip(_translate("OsrmAccessDialog", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_subtitle.setText(_translate("OsrmAccessDialog", "<html><head/><body><p align=\"center\">Accessibility isochrones / catchment areas</p></body></html>"))
        self.pushButton_about.setText(_translate("OsrmAccessDialog", "About.."))
        self.label_3.setText(_translate("OsrmAccessDialog", "Source point layer"))
        self.textBrowser_nb_centers.setHtml(_translate("OsrmAccessDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-style:italic;\">0 center(s) selected</span></p></body></html>"))
        self.pushButtonOrigin.setText(_translate("OsrmAccessDialog", "Origin point"))
        self.toolButton_poly.setText(_translate("OsrmAccessDialog", "+"))
        self.checkBox_selectedFt.setText(_translate("OsrmAccessDialog", "Use only selected features"))
        self.comboBox_method.setItemText(0, _translate("OsrmAccessDialog", "Select a method ..."))
        self.comboBox_method.setItemText(1, _translate("OsrmAccessDialog", "By clicking on the map"))
        self.comboBox_method.setItemText(2, _translate("OsrmAccessDialog", "By selecting a point layer"))
        self.pushButtonClear.setText(_translate("OsrmAccessDialog", "Clear previous isochrones"))
        self.pushButton_fetch.setText(_translate("OsrmAccessDialog", "Display the result"))
        self.label_2.setText(_translate("OsrmAccessDialog", "Intervall (minutes)"))
        self.label.setText(_translate("OsrmAccessDialog", "Max. polygon isochrones (minutes)"))
        self.labem_host.setText(_translate("OsrmAccessDialog", "<html><head/><body><p>OSRM instance url</p></body></html>"))
        self.lineEdit_host.setText(_translate("OsrmAccessDialog", "http://127.0.0.1:5000/"))
        self.lineEdit_profileName.setText(_translate("OsrmAccessDialog", "v1/driving"))
        self.label_4.setText(_translate("OsrmAccessDialog", "Profile"))

from qgis import gui