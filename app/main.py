from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QInputDialog
from PyQt5 import Qt, QtWidgets
from PyQt5.QtGui import QIcon
import sys

import styles
from app.admin_window import Admin
from app.db_requests import create_tables, create_test, all_table, update_weight, out_metal, get_name_by_id
from add_del_scrap_window import AddDelScrap
from app.change_info_window import ChangeScrap
from app.login import Login
from app.report_window import Report


class MainWindow(Qt.QMainWindow):

    def __init__(self, current_u_id, role):
        super().__init__()

        self.current_u_id = current_u_id
        self.setGeometry(0, 0, 1500, 600)
        self.setWindowTitle('Главное окно')
        self.setWindowIcon(QIcon("icons/Icon.png"))

        central_widget = Qt.QWidget()
        self.setCentralWidget(central_widget)

        self.table = Qt.QTableWidget()
        self.main_label = Qt.QLabel('Список склада')
        self.main_label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.main_label.setAlignment(Qtt.AlignCenter)

        self.add_scrap_btn = Qt.QPushButton('Прием металла')
        self.add_scrap_btn.setFont(styles.font)
        self.out_scrap_button = Qt.QPushButton('Убытие металла')
        self.out_scrap_button.setFont(styles.font)
        self.edit_namelist_btn = Qt.QPushButton('Изменить список')
        self.edit_namelist_btn.setFont(styles.font)
        self.report_btn = Qt.QPushButton('Выгрузить отчет')
        self.report_btn.setFont(styles.font)
        self.admin_menu_btn = Qt.QPushButton('Администрирование')
        self.admin_menu_btn.setFont(styles.font)

        self.check_layout = Qt.QHBoxLayout()
        self.check_layout.setAlignment(Qtt.AlignRight)
        self.v_layout = Qt.QVBoxLayout()
        self.table_layout = Qt.QHBoxLayout()
        self.table_layout.addWidget(self.table)
        self.button_layout = Qt.QHBoxLayout()
        self.button_layout.addWidget(self.add_scrap_btn)
        self.button_layout.addWidget(self.out_scrap_button)
        self.button_layout.addWidget(self.edit_namelist_btn)
        self.button_layout.addWidget(self.report_btn)
        if role == 2:
            self.button_layout.addWidget(self.admin_menu_btn)
        self.v_layout.addWidget(self.main_label)
        self.v_layout.addLayout(self.check_layout)
        self.v_layout.addLayout(self.table_layout)
        self.v_layout.addLayout(self.button_layout)
        central_widget.setLayout(self.v_layout)

        self.add_scrap_btn.clicked.connect(self.add_scrap)
        self.out_scrap_button.clicked.connect(self.out_scrap)
        self.edit_namelist_btn.clicked.connect(self.edit_scrap)
        self.report_btn.clicked.connect(self.create_new_report)
        self.admin_menu_btn.clicked.connect(self.admin_window)

        self.table_filling()

    def table_filling(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Наименование", "Количество",
             "Цена", "Сумма", "% НДС", "НДС",
             "Всего", "Последнее\nизменения",
             "Последний\nредактор"])
        records = all_table()

        for row in records:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            item = QTableWidgetItem(str(row.ScrapList.id))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 0, item)

            name = str(row.NameList.name)
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 1, item)

            item = QTableWidgetItem(str(row.ScrapList.weight))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 2, item)

            item = QTableWidgetItem(str(row.ScrapList.price))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 3, item)

            cost = float(format(row.ScrapList.price * row.ScrapList.weight, '.2f'))

            item = QTableWidgetItem(str(cost))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 4, item)

            item = QTableWidgetItem(str(row.ScrapList.percent_nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 5, item)

            nds = float(format(row.ScrapList.percent_nds * cost * 0.01, '.2f'))

            item = QTableWidgetItem(str(nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 6, item)

            item = QTableWidgetItem(str(cost - nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 7, item)

            item = QTableWidgetItem(row.ScrapList.edit_date.strftime('%B %d %Y - %H:%M:%S'))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 8, item)

            editor_name = get_name_by_id(row.ScrapList.editor)
            item = QTableWidgetItem(str(editor_name))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 9, item)

        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    def add_scrap(self):
        st = AddDelScrap(True)
        if st.exec_() == QtWidgets.QDialog.Accepted:
            update_weight(self.current_u_id, st.result_dict)
            self.table_filling()

    def out_scrap(self):
        dw = AddDelScrap(False)
        if dw.exec_() == QtWidgets.QDialog.Accepted:
            print(dw.result_dict)
            if dw.result_dict:
                out_metal(self.current_u_id, dw.result_dict)
        self.table_filling()

    def edit_scrap(self):
        et = ChangeScrap(self.current_u_id)
        et.exec_()
        self.table_filling()

    def create_new_report(self):
        text, ok = QInputDialog.getText(self, 'Новый отчет', 'Введите название файла')
        if ok:
            if text:
                rp = Report(text)
                rp.exec_()
            else:
                Qt.QMessageBox.critical(self, 'Ошибка!', 'Название файла не может быть пустым!')

    def admin_window(self):
        adm = Admin()
        adm.exec_()


if __name__ == '__main__':
    create_tables()
    create_test()
    app = Qt.QApplication(sys.argv)
    lg = Login()
    if lg.exec_() == QtWidgets.QDialog.Accepted:
        w = MainWindow(1, 2)
        w.showMaximized()
    else:
        sys.exit()
    sys.exit(app.exec_())
