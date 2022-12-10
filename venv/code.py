import sqlite3 # Библиотеки
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableView, QApplication, QTableWidgetItem


class App(QWidget): # Основной виджет
    def __init__(self):
        super().__init__()
        # Заполнение виджета таблицы данными из бд
        uic.loadUi('interface.ui', self)
        self.connection = sqlite3.connect("images.db")
        res = self.connection.cursor().execute("SELECT * FROM main").fetchall()

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)

        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'description', 'k'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        # Событие нажатия на кнопку
        self.pushButton.clicked.connect(self.show_data)

    def show_data(self): # Функция при нажатии на кнопку
        select_data = self.lineEdit.text()
        length = len(
            self.connection.cursor().execute("SELECT * FROM main").fetchall())
        #Код преобразования коэффициента k в символьную картинку
        if str(select_data).isdigit() and 0 < int(select_data) < length + 1:
            array = [[chr(9617) + chr(9617) for i in range(106)] for j in
                     range(17)]
            image_x = 106
            image_y = 17
            k = int(self.connection.cursor().execute(
                f"""SELECT * FROM main WHERE id == {select_data}""").fetchall()
                    [0][2]) # Выделение k из строки по выбранному id
            # Формула Таппера
            for y in range(17):
                for x in range(106):
                    ky = y + k
                    res = ((ky // 17) // (2 ** -(-17 * x - (ky % 17)))) % 2
                    if res > 0.5:
                        array[y][105 - x] = chr(9619) + chr(9619)
            self.textEdit.setPlainText('\n'.join(
                [''.join([str(row) for row in col][:image_x]) for col in
                 array][
                :image_y]))

    def closeEvent(self, event): # Отключить БД после закрытия программы
        self.connection.close()


if __name__ == '__main__': # Запуск окна
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
