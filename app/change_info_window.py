from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5 import Qt, QtWidgets
from PyQt5.QtGui import QIcon
import sys

from app.db_requests import get_nds_price_by_name


class ChangeScrap(Qt.QDialog):

    def __init__(self, name_list, parent=None):
        super().__init__(parent)

        self.previous_value = None
        self.row_count = None
        self.name_list = name_list
        self.name_list.sort()
        self.table = Qt.QTableWidget()

        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Редактирование')
        self.setWindowIcon(QIcon("Icon.png"))

        self.label = Qt.QLabel('Редактирование списка наименований')
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.v_layout = Qt.QVBoxLayout(self)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.table)

        self.table.itemDoubleClicked.connect(self.item_click)

        self.scrap_table()
        self.table_filling()

    def scrap_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Наименование", "Цена", "% НДС", "Удалить"])

        # self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def table_filling(self):
        for name in self.name_list:
            full_info = get_nds_price_by_name(name)

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            item = QTableWidgetItem(name)
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 0, item)

            item = QTableWidgetItem(str(full_info.price))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 1, item)

            item = QTableWidgetItem(str(full_info.percent_nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 2, item)

            item = Qt.QPushButton('Del')
            # item.clicked.connect(self.del_btn)
            self.table.setCellWidget(row_count, 3, item)

    def item_click(self):
        self.previous_value = self.table.currentItem().text()
        print(self.previous_value)

    def item_changed(self):
        current_value = self.table.currentItem().text()
        if self.table.currentColumn() in [1, 2]:
            try:
                current_value = float(current_value)
            except Exception as e:
                print(e)
                Qt.QMessageBox.critical(self, 'Ошибка!', '% НДС или цена заполнены неверно!\nДробная часть '
                                                         'вводится через точку.')
            else:
                item = QTableWidgetItem(str(current_value))
                item.setTextAlignment(Qtt.AlignCenter)
                self.table.setItem(self.table.currentRow(), self.table.currentColumn(), item)
