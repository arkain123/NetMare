from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets
import view.Server as Server
import socket


class ServerWindow(QtWidgets.QMainWindow, Server.Ui_Server):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.text = ""
        self.isWorking = False
        self.server_thread = None
        self.StartButton.clicked.connect(self.checkstate)
        self.SaveButton.clicked.connect(self.saveFileTxt)

    def checkstate(self):
        if self.isWorking:
            self.stop_server()
        else:
            self.start_server()

    def saveFileTxt(self):
        name, ok = QFileDialog.getSaveFileName(self, "Save File", "log", "Text Files (*.txt)")
        if len(name) == 0:
            return
        file = open(name, "w")
        file.write(self.text)
        file.close()

    def start_server(self):
        self.Port2Line.setEnabled(False)
        self.progressBar.setValue(1)
        self.StartButton.setText("Остановить сервер")

        self.isWorking = True
        if self.server_thread is None or not self.server_thread.isRunning():
            self.server_thread = ServerThread(port=int(self.Port2Line.text()))
            self.server_thread.new_message.connect(self.log_message)
            self.server_thread.start()

    def stop_server(self):
        self.Port2Line.setEnabled(True)
        self.progressBar.setValue(0)
        self.StartButton.setText("Запустить сервер")

        self.isWorking = False
        if self.server_thread and self.server_thread.isRunning():
            self.server_thread.stop_signal.emit()

    def log_message(self, message):
        self.text += message + "\n"
        self.InfoTextBox.append(message)


class ServerThread(QThread):
    new_message = pyqtSignal(str)
    stop_signal = pyqtSignal()

    def __init__(self, host='127.0.0.1', port=11208):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True
        self.stop_signal.connect(self.stop)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            self.new_message.emit(f'Сервер начал работу на {self.host}:{self.port}')
            while self.running:
                s.settimeout(1)
                try:
                    conn, addr = s.accept()
                except socket.timeout:
                    continue
                with conn:
                    self.new_message.emit(f'Подключение от {addr[0]}')
                    while self.running:
                        try:
                            data = conn.recv(1024)
                            if not data:
                                break
                            self.new_message.emit(f'Получено: {data.decode()}')
                            conn.sendall(data)
                        except:
                            self.new_message.emit(f'Клиент отключен')
                            break

    def stop(self):
        self.running = False
        self.new_message.emit('Сервер остановлен')