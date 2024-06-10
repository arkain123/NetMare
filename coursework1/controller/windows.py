from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets
from view import MainFormDowngrade, AboutAuthor, AboutProgram, Start
from model.Ping import ping
from model.TCPPing import TCPPing
from model.DNSLookup import DNSLookup
from model.MapGenerator import MapGenerator
from model.GeoIPLookup import IPGeolocation
import subprocess
import socket
import time
import threading

class WelcomeWindow(QtWidgets.QMainWindow, Start.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.window = MainWindow()
        self.pushButton.clicked.connect(self.mainWindowStart)
        self.pushButton_2.clicked.connect(self.close)

    def mainWindowStart(self):
        self.window.show()
        self.close()


class MainWindow(QtWidgets.QMainWindow, MainFormDowngrade.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.rowCount = 0
        self.setupUi(self)
        self.client_socket = None
        self.authorwindow = AuthorWindow()
        self.programwindow = ProgramWindow()
        self.text = ""
        self.AboutAuthorAction.triggered.connect(self.authorWindowStart)
        self.AboutProgramAction.triggered.connect(self.programWindowStart)
        self.ClearButton.clicked.connect(self.clear_table)
        self.SaveTxtAction.triggered.connect(self.saveFileTxt)
        self.DoButton.clicked.connect(self.start)
        self.SaveButton.clicked.connect(self.saveFileTxt)
        self.ClearAction.triggered.connect(self.clear_table)
        self.StartServerAction.triggered.connect(self.start_server)
        self.StartButton.clicked.connect(self.start_sending)
        self.StopButton.clicked.connect(self.stop_sending)
        self.PingRButton.clicked.connect(self.checked_changed)
        self.PortCheckerRButton.clicked.connect(self.checked_changed)
        self.DNSLookUpRButton.clicked.connect(self.checked_changed)
        self.GeoIPLookUpRButton.clicked.connect(self.checked_changed)
        self.NetworkLoadRButton.clicked.connect(self.checked_changed)
        self.current_thread = None
        self.communicator = Communicate()
        self.communicator.log_signal.connect(self.log_message)
        self.checked_changed()

    def authorWindowStart(self):
        self.authorwindow.show()

    def programWindowStart(self):
        self.programwindow.show()

    def saveFileTxt(self):
        name, ok = QFileDialog.getSaveFileName(self, "Save File", "log", "Text Files (*.txt)")
        if len(name) == 0:
            return
        file = open(name, "w")
        self.rowCount = self.tableWidget.rowCount()
        if self.rowCount == 0:
            file.write("")
        else:
            for row in range(self.rowCount):
                file.write("Host: " + self.tableWidget.item(row, 0).text() + "\n")
                file.write("Requests: " + self.tableWidget.item(row, 1).text() + "\n")
                file.write("Timeout: " + self.tableWidget.item(row, 2).text() + "\n")
                file.write("Avg. Time: " + self.tableWidget.item(row, 3).text() + "\n")
                file.write("Successful pings: " + self.tableWidget.item(row, 4).text() + "\n")
                file.write("Failed pings: " + self.tableWidget.item(row, 5).text() + "\n")
                file.write("Loss percentage: " + self.tableWidget.item(row, 6).text() + "\n")
                file.write("\n")
        file.write("\n")
        file.write(self.text)
        file.close()

    def start_server(self):
        subprocess.Popen(['python', '', "controller/server.py"], shell=True)

    def start(self):
        if self.PingRButton.isChecked():
            self.ping()
        elif self.PortCheckerRButton.isChecked():
            self.check_port()
        elif self.DNSLookUpRButton.isChecked():
            self.dnslook()
        elif self.GeoIPLookUpRButton.isChecked():
            self.geolookup()
        elif self.NetworkLoadRButton.isChecked():
            self.networkload()

    def open_html_file(self):
        try:
            subprocess.Popen(['start', '', "map.html"], shell=True)
        except Exception as e:
            print(f"An error occurred: {e}")

    def checked_changed(self):
        if self.PingRButton.isChecked():
            self.IpLine.setEnabled(True)
            self.URILine.setEnabled(False)
            self.PortLine.setEnabled(False)
            self.CountLine.setEnabled(True)
            self.TimeoutLine.setEnabled(True)
            self.ServerSettingsGBox.setEnabled(False)
            self.DoButton.setEnabled(True)
        elif self.PortCheckerRButton.isChecked():
            self.IpLine.setEnabled(True)
            self.URILine.setEnabled(False)
            self.PortLine.setEnabled(True)
            self.CountLine.setEnabled(False)
            self.TimeoutLine.setEnabled(True)
            self.ServerSettingsGBox.setEnabled(False)
            self.DoButton.setEnabled(True)
        elif self.DNSLookUpRButton.isChecked():
            self.IpLine.setEnabled(False)
            self.URILine.setEnabled(True)
            self.PortLine.setEnabled(False)
            self.CountLine.setEnabled(False)
            self.TimeoutLine.setEnabled(False)
            self.ServerSettingsGBox.setEnabled(False)
            self.DoButton.setEnabled(True)
        elif self.NetworkLoadRButton.isChecked():
            self.IpLine.setEnabled(False)
            self.URILine.setEnabled(False)
            self.PortLine.setEnabled(False)
            self.CountLine.setEnabled(True)
            self.TimeoutLine.setEnabled(True)
            self.ServerSettingsGBox.setEnabled(True)
            self.DoButton.setEnabled(False)
        elif self.GeoIPLookUpRButton.isChecked():
            self.IpLine.setEnabled(True)
            self.URILine.setEnabled(False)
            self.PortLine.setEnabled(False)
            self.CountLine.setEnabled(False)
            self.TimeoutLine.setEnabled(False)
            self.ServerSettingsGBox.setEnabled(False)
            self.DoButton.setEnabled(True)

    def ping(self):
        try:
            self.text = ""
            self.InfoTextBox.setText(self.text)
            result = ping(self.IpLine.text(), self.CountLine.text(), float(self.TimeoutLine.text()))

            self.rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.rowCount)

            self.tableWidget.setItem(self.rowCount, 0, QtWidgets.QTableWidgetItem(result['host']))
            self.tableWidget.setItem(self.rowCount, 1, QtWidgets.QTableWidgetItem(result['count']))
            self.tableWidget.setItem(self.rowCount, 2, QtWidgets.QTableWidgetItem(str(result['delay'])))
            self.tableWidget.setItem(self.rowCount, 3, QtWidgets.QTableWidgetItem(str(round(result['avg'], 3))))
            self.tableWidget.setItem(self.rowCount, 4, QtWidgets.QTableWidgetItem(str(result['successes'])))
            self.tableWidget.setItem(self.rowCount, 5, QtWidgets.QTableWidgetItem(str(result['failures'])))
            self.tableWidget.setItem(self.rowCount, 6, QtWidgets.QTableWidgetItem(str(result['loss']) + '%'))

            self.text += "Хост: " + result['host']
            self.text += "\nКол-во пакетов: " + result['count']
            self.text += "\nВремя между пакетами: " + str(result['delay'])
            self.text += "\nСр.время отправки: " + str(round(result['avg'], 3))
            self.text += "\nУспешно: " + str(result['successes'])
            self.text += "\nНеуспешно: " + str(result['failures'])
            self.text += "\nПроцент потерь: " + str(result['loss']) + '%'
            self.InfoTextBox.setText(self.text)

        except:
            self.InfoTextBox.setText("Ошибка. Проверьте ввод")

    def clear_table(self):
        self.rowCount = self.tableWidget.rowCount()
        while self.rowCount >= 0:
            self.tableWidget.removeRow(self.rowCount)
            self.rowCount -= 1
        self.rowCount = self.tableWidget.rowCount()
        self.text = ""
        self.InfoTextBox.setText("")

    def check_port(self):
        try:
            ping_obj = TCPPing(str(self.IpLine.text()), port=self.PortLine.text(), timeout=self.TimeoutLine.text())
            result = ping_obj.run()
            self.text = ""
            self.text = "Host: " + result['host'] + "\nPort: " + str(result['port'])
            self.text += "\nStatus: " + result['status'] + "\nResponse Time: " + str(result['response_time'])
            self.InfoTextBox.setText(self.text)
        except:
            self.InfoTextBox.setText("Ошибка. Проверьте ввод")

    def dnslook(self):
        try:
            dnslook_obj = DNSLookup(self.URILine.text())
            result = dnslook_obj.run()
            self.text = ""
            self.text = "Host: " + result['host'] + "\nIp: " + result['ip']
            self.InfoTextBox.setText(self.text)
        except:
            self.InfoTextBox.setText("Ошибка. Проверьте ввод")

    def geolookup(self):
        try:
            geolook_obj = IPGeolocation()
            result = geolook_obj.get_location(str(self.IpLine.text()))
            mapgen = MapGenerator()
            mapgen.add_marker(result, f"IP: {str(self.IpLine.text())}")
            mapgen.show()
            self.open_html_file()
            data = geolook_obj.get_result()
            self.text = ""
            self.text += f"Ip: {data['ip']}\n"
            try:
                self.text += f"Hostname: {data['hostname']}\n"
            except:
                pass
            self.text += f"City: {data['city']}\n"
            self.text += f"Region: {data['region']}\n"
            self.text += f"Country: {data['country']}\n"
            self.text += f"Location: {data['loc']}\n"
            self.text += f"Organisation: {data['org']}\n"
            self.text += f"Postal: {data['postal']}\n"
            self.text += f"timezone: {data['timezone']}\n"
            self.InfoTextBox.setText(self.text)
        except:
            self.InfoTextBox.setText("Ошибка. Проверьте ввод")

    def start_sending(self):
        try:
            if not self.current_thread or not self.current_thread.is_alive():
                self.progressBar.setValue(1)
                self.Port2Line.setEnabled(False)
                self.Ip2Line.setEnabled(False)
                self.MainSettingsGBox.setEnabled(False)
                self.WorkGBox.setEnabled(False)
                self.StartButton.setEnabled(False)
                self.StopButton.setEnabled(True)

                ip = self.Ip2Line.text()
                port = int(self.Port2Line.text())
                num_packets = int(self.CountLine.text())
                interval = float(self.TimeoutLine.text())
                self.current_thread = PacketSenderThread(ip, port, num_packets, interval, self.communicator)
                self.current_thread.start()
                self.text = "Отправка запущена\n"
                self.InfoTextBox.setText(self.text)
        except:
            self.InfoTextBox.setText("Ошибка. Проверьте ввод")
            self.stop_sending()

    def stop_sending(self):
        self.progressBar.setValue(0)
        self.Port2Line.setEnabled(True)
        self.Ip2Line.setEnabled(True)
        self.WorkGBox.setEnabled(True)
        self.MainSettingsGBox.setEnabled(True)
        self.StartButton.setEnabled(True)
        self.StopButton.setEnabled(False)
        try:
            self.current_thread.stop()
            self.current_thread.join()
            self.text += "\nОтправка остановлена"
            self.InfoTextBox.setText(self.text)
        except:
            self.text += "\nОшибка. Проверьте ввод"
            self.InfoTextBox.setText(self.text)

    def log_message(self, message):
        self.text += message + "\n"
        self.InfoTextBox.setText(self.text)


class AuthorWindow(QtWidgets.QMainWindow, AboutAuthor.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ProgramWindow(QtWidgets.QMainWindow, AboutProgram.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Communicate(QObject):
    log_signal = pyqtSignal(str)


class PacketSenderThread(threading.Thread):
    def __init__(self, ip, port, num_packets, interval, communicator):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.num_packets = num_packets
        self.interval = interval
        self.stop_event = threading.Event()
        self.communicator = communicator

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            self.communicator.log_signal.emit("Подключаемся к {}:{}".format(self.ip, self.port))
            # Создаем сокет
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, self.port))

            self.communicator.log_signal.emit("Подключено. Отправляем пакеты...")
            # Отправляем пакеты
            start_time = time.time()
            for i in range(self.num_packets):
                if self.stop_event.is_set():
                    break
                packet = b"Hello, server!"
                sock.sendall(packet)
                self.communicator.log_signal.emit("Пакет {} отправлен".format(i + 1))
                elapsed_time = time.time() - start_time
                self.communicator.log_signal.emit(
                    "Время затраченное на передачу пакета {}: {:.4f} с".format(i + 1, elapsed_time))
                start_time = time.time()
                time.sleep(self.interval)

            sock.close()
            self.communicator.log_signal.emit("\nОтправка завершена")
        except Exception as e:
            self.communicator.log_signal.emit("Ошибка: {}".format(e))
        finally:
            while True:
                if self.stop_event.is_set():
                    break