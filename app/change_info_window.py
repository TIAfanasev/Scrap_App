from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5 import Qt, QtWidgets
from PyQt5.QtGui import QIcon
import sys

from app.db_requests import get_nds_price_by_name, update_price_or_nds, check_scrapname_unique, update_scrapname


class ChangeScrap(Qt.QDialog):

    def __init__(self, u_id, name_list, parent=None):
        super().__init__(parent)

        self.u_id = u_id
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

        self.scrap_table()
        # self.table_filling()

        self.table.currentItemChanged.connect(self.item_click)
        self.table.cellChanged.connect(self.item_changed)

    def scrap_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Наименование", "Цена", "% НДС", "Удалить"])

        # self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.table_filling()

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
        if self.table.currentColumn() in [0, 1, 2]:
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
                self.table.currentItem().setText(self.previous_value)
            else:
                if self.table.currentColumn() == 1:
                    update_price_or_nds(self.u_id, self.table.item(self.table.currentRow(), 0).text(), current_value, True)
                elif self.table.currentColumn() == 2:
                    update_price_or_nds(self.u_id, self.table.item(self.table.currentRow(), 0).text(), current_value, False)
                self.table.currentItem().setText(format(current_value, '.2f'))

        elif self.table.currentColumn() == 0:
            if check_scrapname_unique(current_value):
                update_scrapname(self.u_id, self.previous_value, current_value)
            else:
                Qt.QMessageBox.critical(self, 'Ошибка!', 'Такое название уже существует!')
                self.table.currentItem().setText(self.previous_value)
