from PyQt5 import QtWidgets
import sys
import controller.windows


#O(1)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = controller.windows.WelcomeWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение