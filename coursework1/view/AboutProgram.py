from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(639, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/IconPNG/Image/IcoPNG.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 281))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(310, 30, 321, 221))
        self.label_2.setAcceptDrops(False)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(320, 10, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(430, 270, 91, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AboutProgram"))
        self.label.setText(_translate("Form", "<html><head/><body><p><img src=\":/IconPNG/Image/IcoPNG.png\"/></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"justify\">    NetMare - это мощная утилита для анализа и диагностики сетевых соединений. Программа предоставляет пользователю широкий набор инструментов для проверки связи с удалёнными хостами, разрешения DNS-запросов, определения геолокации IP-адресов и визуализации маршрутов пакетов на карте. NetAnalyzer создан для того, чтобы помочь системным администраторам, сетевым инженерам и любому, кто сталкивается с проблемами в сети, легко и быстро получать необходимую информацию для диагностики и устранения неполадок.</p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"center\">NetMare</p></body></html>"))
        self.label_4.setText(_translate("Form", "Версия 1.03"))
import Resources.resource_rc
