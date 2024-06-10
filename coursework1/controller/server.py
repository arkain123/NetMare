from PyQt5 import QtWidgets
import sys
import server_files.server as server

app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
window = server.ServerWindow()  # Создаём объект класса ExampleApp
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение