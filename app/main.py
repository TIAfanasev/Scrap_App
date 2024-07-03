from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5 import Qt, QtWidgets
from PyQt5.QtGui import QIcon
import sys

import styles
from app.database import Base, sync_engine
from app.db_requests import create_tables, create_test, all_table, scrap_names, add_new_metal, out_metal
from add_scrap_window import AddDelScrap

#import Var


class MainWindow(Qt.QMainWindow):

    def __init__(self):
        super().__init__()

        # Прорисовка окна приложения
        self.name_list = set()
        self.setGeometry(0, 0, 1500, 600)
        self.setWindowTitle('Главное окно')
        self.setWindowIcon(QIcon("Icon.png"))

        central_widget = Qt.QWidget()
        self.setCentralWidget(central_widget)

        self.table = Qt.QTableWidget()
        self.main_label = Qt.QLabel('Список склада')
        self.main_label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.main_label.setAlignment(Qtt.AlignCenter)

        # self.checkbox_process = Qt.QCheckBox('Необработанные заявки')
        # self.checkbox_process.setFont(Styles.font)
        self.refresh_btn = Qt.QPushButton('Обновить')
        self.refresh_btn.setFont(styles.font)
        self.add_scrap_btn = Qt.QPushButton('Прием металла')
        self.add_scrap_btn.setFont(styles.font)
        self.out_scrap_button = Qt.QPushButton('Убытие металла')
        self.out_scrap_button.setFont(styles.font)
        self.edit_namelist_btn = Qt.QPushButton('Изменить список')
        self.edit_namelist_btn.setFont(styles.font)
        self.report_btn = Qt.QPushButton('Выгрузить отчет')
        self.report_btn.setFont(styles.font)

        self.notif = Qt.QLabel('*перейти в редактирование можно двойным нажатием '
                               'ЛКМ по нужной ячейке или специальными кнопками ниже')
        self.notif.setStyleSheet("color:grey; font: 9pt 'Arial';")

        self.check_layout = Qt.QHBoxLayout()
        # self.check_layout.addWidget(self.checkbox_process)
        self.check_layout.addWidget(self.refresh_btn)
        self.check_layout.setAlignment(Qtt.AlignRight)
        self.v_layout = Qt.QVBoxLayout()
        self.table_layout = Qt.QHBoxLayout()
        self.table_layout.addWidget(self.table)
        self.button_layout = Qt.QHBoxLayout()
        self.button_layout.addWidget(self.add_scrap_btn)
        self.button_layout.addWidget(self.out_scrap_button)
        self.button_layout.addWidget(self.edit_namelist_btn)
        self.button_layout.addWidget(self.report_btn)
        self.v_layout.addWidget(self.main_label)
        self.v_layout.addLayout(self.check_layout)
        self.v_layout.addLayout(self.table_layout)
        self.v_layout.addWidget(self.notif)
        self.v_layout.addLayout(self.button_layout)
        central_widget.setLayout(self.v_layout)

        self.add_scrap_btn.clicked.connect(self.add_scrap)
        self.out_scrap_button.clicked.connect(self.out_scrap)

        self.state_cb()
    #     # Первое заполнение таблицы
    #     self.state_cb()
    #
    #     # Проверка изменения состояния чекбокса
    #     self.checkbox_process.stateChanged.connect(self.state_cb)
    #
    #     # Сигнал двойного нажатия по элементу таблицы
    #     self.table.doubleClicked.connect(self.item_doubleclick)
    #
    #     # Нажатие кнопки обновления таблицы
    #     self.refresh_btn.clicked.connect(self.state_cb)
    #
    #     self.edit_bld_btn.clicked.connect(self.editor)
    #
    #     self.edit_clnt_btn.clicked.connect(self.editor)
    #
    #     self.add_req_btn.clicked.connect(self.add)
    #
    # def add(self):
    #     ad = Add_request.NewReq()
    #     if ad.exec_():
    #         self.state_cb()
    #
    # def editor(self):
    #     sender = self.sender()
    #     if sender.text() == 'Список зданий':
    #         self.edit = List_editor.ListEditor(1)
    #     else:
    #         self.edit = List_editor.ListEditor(0)
    #
    #     if self.edit.exec_():
    #         self.state_cb()
    #

    # Обработка изменения чекбокса
    def state_cb(self):
        self.table_filling()
        self.table.resizeRowsToContents()

    # def item_doubleclick(self):
    #     cur_id = self.table.item(self.table.currentRow(), 0).text()
    #     if self.table.currentColumn() in [1, 5, 6, 7, 8, 9]:
    #         cl_id = Var.one_query('client', 'apps', cur_id)
    #         ec = Client_Editor.EditClient(cl_id)
    #         ec.exec_()
    #         self.state_cb()
    #
    #     elif self.table.currentColumn() == 2:
    #         hs_id = Var.one_query('building', 'apps', cur_id)
    #         eh = Build_Editor.EditBuild(hs_id)
    #         eh.exec_()
    #         self.state_cb()
    #
    # def checkbox_edit(self):
    #     ch = self.sender()
    #     ix = self.table.indexAt(ch.pos())
    #     cur_id = self.table.item(ix.row(), 0).text()
    #     work_query = f'UPDATE apps SET ready = \'{ch.isChecked()}\' WHERE id = {cur_id}'
    #     Var.cursor.execute(work_query)
    #     Var.connection.commit()
    #
    # # Заполнение таблицы значениями из БД
    def table_filling(self):

        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Наименование", "Количество", "Цена", "Сумма", "% НДС", "НДС", "Всего"])

        records = all_table()

        for row in records:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            item = QTableWidgetItem(str(row.id))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 0, item)

            name = scrap_names(row.name)
            item = QTableWidgetItem(name)
            self.name_list.add(name)
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 1, item)

            item = QTableWidgetItem(str(row.weight))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 2, item)

            item = QTableWidgetItem(str(row.price))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 3, item)

            cost = float(format(row.price * row.weight, '.2f'))

            item = QTableWidgetItem(str(cost))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 4, item)

            item = QTableWidgetItem(str(row.percent_nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 5, item)

            nds = float(format(row.percent_nds * cost * 0.01, '.2f'))

            item = QTableWidgetItem(str(nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 6, item)

            item = QTableWidgetItem(str(cost - nds))
            item.setTextAlignment(Qtt.AlignCenter)
            self.table.setItem(row_count, 7, item)

        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.resizeRowsToContents()

    def add_scrap(self):
        st = AddDelScrap(list(self.name_list), True)
        if st.exec_() == QtWidgets.QDialog.Accepted:
            print(st.result_dict)
            if st.result_dict:
                add_new_metal(st.result_dict)
        self.state_cb()

    def out_scrap(self):
        dw = AddDelScrap(list(self.name_list), False)
        if dw.exec_() == QtWidgets.QDialog.Accepted:
            print(dw.result_dict)
            if dw.result_dict:
                out_metal(dw.result_dict)
        self.state_cb()




if __name__ == '__main__':

    create_tables()
    create_test()
    app = Qt.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
