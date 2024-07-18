from PyQt5 import Qt, QtWidgets, QtGui
from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem, QHeaderView
from openpyxl.workbook import Workbook

from app.db_requests import check_weight, get_id_by_name, get_nds_price_by_name, get_user_info, delete_user
from app.edit_user import UserEditor


class Admin(Qt.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Администрирование')
        self.setWindowIcon(QtGui.QIcon("Icon.png"))
        self.label = Qt.QLabel('Список пользователей')
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.table = Qt.QTableWidget()

        self.add_user_btn = Qt.QPushButton('Добавить пользователя')
        self.exit_btn = Qt.QPushButton('Сохранить и выйти')

        self.button_layout = Qt.QHBoxLayout()
        self.button_layout.addWidget(self.add_user_btn)
        self.button_layout.addWidget(self.exit_btn)

        self.v_layout = Qt.QVBoxLayout(self)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.table)
        self.v_layout.addLayout(self.button_layout)

        self.add_user_btn.clicked.connect(self.add_user)
        self.exit_btn.clicked.connect(self.save_n_exit)

        self.table_filling()

    def table_filling(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Логин", "Роль", "Изменить", "Удалить"])

        records = get_user_info()

        # print(records)
        for users, role in records:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            item = QTableWidgetItem(str(users.id))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 0, item)

            item = QTableWidgetItem(str(users.name))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 1, item)

            item = QTableWidgetItem(str(users.login))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 2, item)

            item = QTableWidgetItem(str(role.role))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 3, item)

            item = Qt.QPushButton('Edit')
            item.clicked.connect(self.editor)
            self.table.setCellWidget(row_count, 4, item)

            item = Qt.QPushButton('Del')
            item.clicked.connect(self.deleter)
            self.table.setCellWidget(row_count, 5, item)

            self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            # self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
            self.table.resizeRowsToContents()

    def editor(self):
        u_id = int(self.table.item(self.table.currentRow(), 0).text())
        ue = UserEditor(u_id)
        if ue.exec_() == QtWidgets.QDialog.Accepted:
            self.table_filling()

    def add_user(self):
        ue = UserEditor()
        if ue.exec_() == QtWidgets.QDialog.Accepted:
            self.table_filling()

    def deleter(self):
        u_id = int(self.table.item(self.table.currentRow(), 0).text())
        button = QMessageBox.warning(self, "Удаление", "Удалить пользователя?\nЭто действие нельзя отменить",
                                     buttons=QMessageBox.Yes | QMessageBox.No,
                                     defaultButton=QMessageBox.No)
        if button == QMessageBox.Yes:
            delete_user(u_id)
            self.table_filling()

    def save_n_exit(self):
        self.accept()
