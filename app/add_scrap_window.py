from PyQt5 import Qt, QtWidgets, QtGui
from PyQt5.QtCore import Qt as Qtt


class AddScrap(Qt.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.row_count = None
        self.test_data = None
        self.setGeometry(560, 240, 800, 600)
        self.setWindowTitle('Прибытие')
        self.setWindowIcon(QtGui.QIcon("Icon.png"))

        self.group_list = []
        # self.roles_copy = list(Var.roles)

        self.label = Qt.QLabel('Выберите группу(-ы)')
        self.label.setStyleSheet("color:#0095DA; font: bold 20pt 'MS Shell Dlg 2';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.groups = Qt.QLabel()
        # self.groups.setFont(Var.font)

        self.table = Qt.QTableWidget()
        # self.table.setFont(Var.font)

        self.start = Qt.QPushButton('Старт!')
        # self.start.setFont(Var.font)

        self.v_layout = Qt.QVBoxLayout(self)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.groups)
        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.start)

        self.name_table()

        self.start.clicked.connect(self.start_btn)

    def name_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Наименование", "Количество", "Удалить"])

        self.row_count = self.table.rowCount()
        self.table.insertRow(self.row_count)

        self.test_data = ["Выберите наименование", "Медь", "Сталь"]

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
        item.addItems(self.test_data)

        # item.setTextAlignment(Qtt.AlignCenter)
        item.currentTextChanged.connect(self.add_new_row)
        self.table.setCellWidget(self.row_count, 0, item)

        item = Qt.QLineEdit()
        item.setDisabled(True)
        item.setAlignment(Qtt.AlignCenter)
        self.table.setCellWidget(self.row_count, 1, item)

        item = Qt.QPushButton('Del')
        # item.clicked.connect(self.add_btn)
        self.table.setCellWidget(self.row_count, 2, item)

    def add_new_row(self):
        self.table.cellWidget(self.row_count, 0).setDisabled(True)
        self.table.cellWidget(self.row_count, 1).setDisabled(False)
        name = self.table.cellWidget(self.row_count, 0).currentText()
        self.test_data.remove(name)
        self.row_count = self.table.rowCount()
        self.table.insertRow(self.row_count)
        self.row_items()

    def start_btn(self):
        result_dict = {}
        try:
            for x in range(self.row_count):
                key = self.table.cellWidget(x, 0).currentText()
                value = float(self.table.cellWidget(x, 1).text())
                result_dict[key] = value
        except Exception as e:
            print(e)
            Qt.QMessageBox.critical(self, 'Ошибка!', 'В поле количество введите массу в тоннах!\nДробная часть '
                                                             'вводится через точку.')
        else:
            print(result_dict)
            self.accept()
