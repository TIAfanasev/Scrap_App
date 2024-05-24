from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import Qt, QtWidgets
from PyQt5.Qt import QTimer
from PyQt5.QtGui import QIcon
import sys
import os

import Styles
#import Var


class MainWindow(Qt.QMainWindow):

    def __init__(self):
        super().__init__()

        # Прорисовка окна приложения
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
        self.refresh_btn.setFont(Styles.font)
        self.add_scrap_btn = Qt.QPushButton('Прием металла')
        self.add_scrap_btn.setFont(Styles.font)
        self.out_scrap_button = Qt.QPushButton('Убытие металла')
        self.out_scrap_button.setFont(Styles.font)
        self.edit_namelist_btn = Qt.QPushButton('Изменить список')
        self.edit_namelist_btn.setFont(Styles.font)
        self.report_btn = Qt.QPushButton('Выгрузить отчет')
        self.report_btn.setFont(Styles.font)

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
    # # Обработка изменения чекбокса
    # def state_cb(self):
    #     self.table_filling()
    #     self.table.resizeRowsToContents()
    #
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
    # def table_filling(self):
    #
    #     state = self.checkbox_process.checkState()
    #     self.table.clear()
    #     self.table.setRowCount(0)
    #     self.table.setColumnCount(10)
    #     self.table.setHorizontalHeaderLabels(
    #         ["ID", "ФИО", "Город", "Дата заявки", "Выполнение", "Телефон", "Telegram", "WhatsApp", "Viber",
    #          "Email"])
    #
    #     if state:
    #         display_query = 'SELECT * FROM apps WHERE ready = False ORDER BY id'
    #     else:
    #         display_query = 'SELECT * FROM apps ORDER BY ready, id'
    #
    #     Var.cursor.execute(display_query)
    #
    #     Var.connection.commit()
    #     records = Var.cursor.fetchall()
    #
    #     for row in records:
    #         client_name = Var.one_query('fio', 'clients', row[1])
    #
    #         building_address = Var.one_query('address', 'buildings', row[2])
    #
    #         phone = Var.one_query('phone', 'clients', row[1])
    #
    #         mail = Var.one_query('email', 'clients', row[1])
    #
    #         telegram = Var.one_query('telegram', 'clients', row[1])
    #
    #         row_count = self.table.rowCount()
    #         self.table.insertRow(row_count)
    #
    #         item = QTableWidgetItem(str(row[0]))
    #         item.setTextAlignment(Qtt.AlignCenter)
    #         self.table.setItem(row_count, 0, item)
    #
    #         item = QTableWidgetItem(client_name)
    #         item.setTextAlignment(Qtt.AlignCenter)
    #         self.table.setItem(row_count, 1, item)
    #
    #         item = QTableWidgetItem(building_address)
    #         item.setTextAlignment(Qtt.AlignCenter)
    #         self.table.setItem(row_count, 2, item)
    #
    #         item = QTableWidgetItem(str(row[3]))
    #         item.setTextAlignment(Qtt.AlignCenter)
    #         self.table.setItem(row_count, 3, item)
    #
    #         chk_bx = Qt.QCheckBox()
    #         chk_bx.setStyleSheet("text-align: center; margin-left:50%; margin-right:50%;")
    #         chk_bx.setCheckState(Qtt.Checked) if row[4] is True else chk_bx.setCheckState(Qtt.Unchecked)
    #         chk_bx.clicked.connect(self.checkbox_edit)
    #         self.table.setCellWidget(row_count, 4, chk_bx)
    #
    #         item = QTableWidgetItem('+7' + str(phone))
    #         item.setTextAlignment(Qtt.AlignCenter)
    #         self.table.setItem(row_count, 5, item)
    #
    #         if telegram:
    #             item = Qt.QLabel(f"<a href='https://t.me/{telegram}'>Перейти</a>", openExternalLinks=True)
    #         else:
    #             item = Qt.QLabel("Не указан")
    #         item.setAlignment(Qtt.AlignCenter)
    #         item.setMinimumHeight(15)
    #         self.table.setCellWidget(row_count, 6, item)
    #
    #         item = Qt.QLabel(f"<a href='https://wa.me/7{phone}'>Перейти</a>", openExternalLinks=True)
    #         item.setAlignment(Qtt.AlignCenter)
    #         self.table.setCellWidget(row_count, 7, item)
    #
    #         item = Qt.QLabel(f"<a href='viber://chat?number=%2B7{phone}'>Перейти</a>", openExternalLinks=True)
    #         item.setAlignment(Qtt.AlignCenter)
    #         self.table.setCellWidget(row_count, 8, item)
    #
    #         item = QTableWidgetItem(str(mail))
    #         item.setTextAlignment(Qtt.AlignCenter)
    #         self.table.setItem(row_count, 9, item)
    #
    #     self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    #
    #     self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
    #     self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
    #     self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
    #     self.table.resizeRowsToContents()


if __name__ == '__main__':

    app = Qt.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
