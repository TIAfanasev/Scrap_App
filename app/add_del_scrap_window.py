from PyQt5 import Qt, QtWidgets, QtGui
from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from openpyxl.workbook import Workbook

from app.db_requests import check_weight, get_id_by_name, get_nds_price_by_name


class AddDelScrap(Qt.QDialog):

    def __init__(self, name_list, flag, parent=None):
        super().__init__(parent)
        self.flag = flag
        self.result_dict = None
        self.row_count = None
        self.name_list = name_list
        self.name_list.sort()
        self.name_list.insert(0, "Выберите наименование")
        self.setGeometry(560, 240, 800, 600)
        if flag:
            self.setWindowTitle('Прибытие')
        else:
            self.setWindowTitle('Убытие')
        self.setWindowIcon(QtGui.QIcon("Icon.png"))

        self.group_list = []
        if flag:
            self.label = Qt.QLabel('Выберите прибывшие наименование(-я)')
        else:
            self.label = Qt.QLabel('Выберите убывшие наименование(-я)')
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.table = Qt.QTableWidget()
        # self.table.setFont(Var.font)

        self.start = Qt.QPushButton('Сохранить и выйти')
        # self.start.setFont(Var.font)

        self.v_layout = Qt.QVBoxLayout(self)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.start)

        self.name_table()

        self.start.clicked.connect(self.go_out_btn)

    def name_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Наименование", "Количество", "Удалить"])

        self.row_count = self.table.rowCount()
        self.table.insertRow(self.row_count)

        self.row_items()
        # for x in self.roles_copy:
        #     if x[0].isdigit() or x[1].isdigit():
        #         row_count = self.table.rowCount()
        #         self.table.insertRow(row_count)
        #
        #         item = QtWidgets.QTableWidgetItem(x)
        #         item.setTextAlignment(Qtt.AlignCenter)
        #         self.table.setItem(row_count, 0, item)
        #
        #         item = Qt.QPushButton('+')
        #         item.clicked.connect(self.add_btn)
        #         self.table.setCellWidget(row_count, 1, item)

        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setDefaultAlignment(Qtt.AlignCenter)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    # def add_btn(self):
    #     gr = self.table.item(self.table.currentRow(), 0).text()
    #     self.group_list.append(gr)
    #     self.roles_copy.remove(gr)
    #     t_groups = self.groups.text()
    #     self.groups.setText(t_groups + gr + "; ")
    #     self.gr_table()
    #

    def row_items(self):
        item = Qt.QComboBox()
        item.addItems(self.name_list)
        item.currentTextChanged.connect(self.add_new_row)
        self.table.setCellWidget(self.row_count, 0, item)

        item = Qt.QLineEdit()
        item.setDisabled(True)
        item.setAlignment(Qtt.AlignCenter)
        self.table.setCellWidget(self.row_count, 1, item)

        item = Qt.QPushButton('Del')
        item.clicked.connect(self.del_btn)
        item.setDisabled(True)
        self.table.setCellWidget(self.row_count, 2, item)

    def add_new_row(self):
        self.table.cellWidget(self.row_count, 0).setDisabled(True)
        self.table.cellWidget(self.row_count, 1).setDisabled(False)
        self.table.cellWidget(self.row_count, 2).setDisabled(False)
        name = self.table.cellWidget(self.row_count, 0).currentText()
        self.name_list.remove(name)
        self.row_count = self.table.rowCount()
        self.table.insertRow(self.row_count)
        self.row_items()

    def go_out_btn(self):
        self.result_dict = {}
        try:
            for x in range(self.row_count):
                key = self.table.cellWidget(x, 0).currentText()
                value = float(self.table.cellWidget(x, 1).text())
                if not value:
                    raise ValueError
                elif not self.flag and not check_weight(key, value):
                    raise Warning
                else:
                    self.result_dict[key] = value
        except ValueError as e:
            print(e)
            Qt.QMessageBox.critical(self, 'Ошибка!', 'В поле количество введите массу в тоннах!\nДробная часть '
                                                     'вводится через точку.')
        except Warning as e:
            print(e)
            Qt.QMessageBox.critical(self, 'Ошибка!', f'Вес наименования {key} превышает доступный в наличии!')
        else:
            if self.result_dict:
                button = QMessageBox.question(self, "Создание отчета", "Сохранить отчет об изменениях?")
                if button == QMessageBox.Yes:
                    name = ''
                    while not name:
                        name, ok = QInputDialog.getText(self, 'Новый отчет',
                                                        'Введите название файла\nили оставьте поле пустым\n')
                        if ok:
                            if name:
                                self.edit_report(name)
                            else:
                                Qt.QMessageBox.critical(self, 'Ошибка!', 'Название файла не может быть пустым!')

                self.accept()
            else:
                self.reject()

    def del_btn(self):
        name = self.table.cellWidget(self.table.currentRow(), 0).currentText()
        self.name_list.append(name)
        self.table.update()
        self.table.removeRow(self.table.currentRow())
        self.row_count = self.table.rowCount() - 1

        self.upd_list()

    def upd_list(self):
        self.name_list.remove("Выберите наименование")
        self.name_list.sort()
        self.name_list.insert(0, "Выберите наименование")

        item = Qt.QComboBox()
        item.addItems(self.name_list)
        item.currentTextChanged.connect(self.add_new_row)
        self.table.setCellWidget(self.row_count, 0, item)

    def edit_report(self, name):
        wb = Workbook()

        ws = wb.active
        if self.flag:
            ws.title = "Прибытие"
        else:
            ws.title = "Убытие"

        titles = ["ID", "Наименование", "Количество", "Цена", "Сумма", "% НДС", "НДС", "Всего"]

        for x in range(1, 9):
            ws.cell(row=1, column=x, value=titles[x - 1])

        y = 2
        for one in self.result_dict.keys():
            ws.cell(row=y, column=1, value=get_id_by_name(one))
            ws.cell(row=y, column=2, value=one)
            ws.cell(row=y, column=3, value=self.result_dict[one])
            nds_n_price = get_nds_price_by_name(one)
            ws.cell(row=y, column=4, value=nds_n_price.price)
            cost = float(format(nds_n_price.price * self.result_dict[one], '.2f'))
            ws.cell(row=y, column=5, value=cost)
            ws.cell(row=y, column=6, value=nds_n_price.percent_nds)
            nds = float(format(nds_n_price.percent_nds * cost * 0.01, '.2f'))
            ws.cell(row=y, column=7, value=nds)
            ws.cell(row=y, column=8, value=cost - nds)
            y += 1

        wb.save(f'{name}.xlsx')
