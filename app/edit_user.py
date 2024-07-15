from PyQt5 import Qt, QtWidgets, QtGui
from PyQt5.QtCore import Qt as Qtt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem, QHeaderView
from openpyxl.workbook import Workbook
from hashlib import md5

from app import styles
from app.db_requests import check_weight, get_id_by_name, get_nds_price_by_name, get_user_info, check_unique_login, \
    update_user


class UserEditor(Qt.QDialog):

    def __init__(self, u_id, parent=None):
        super().__init__(parent)
        self.u_id = u_id

        self.setGeometry(800, 350, 300, 300)
        self.setWindowTitle('Редактирование')
        self.setWindowIcon(QtGui.QIcon("Icon.png"))
        self.label = Qt.QLabel('Редактирование пользователя')
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.user, self.role = get_user_info(self.u_id)

        self.id_label = Qt.QLabel(f'ID: {self.user.id}')
        self.id_label.setFont(styles.font)

        self.name_label = Qt.QLabel('ФИО:')
        self.name_label.setFont(styles.font)
        self.name = Qt.QLineEdit()
        self.name.setFont(styles.font)
        self.name.setPlaceholderText('Пример: Иванов Иван Иванович')
        self.name.setText(self.user.name)

        self.login_label = Qt.QLabel('Логин:')
        self.login_label.setFont(styles.font)
        self.login = Qt.QLineEdit()
        self.login.setFont(styles.font)
        self.login.setPlaceholderText('Пример: user1')
        self.login.setText(self.user.login)

        self.role_label = Qt.QLabel(f'Роль: {self.role.role}')
        self.role_label.setFont(styles.font)

        self.password_label = Qt.QLabel('Изменить пароль:')
        self.password_label.setFont(styles.font)
        self.password = Qt.QLineEdit()
        self.password.setFont(styles.font)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.save_btn = Qt.QPushButton('Сохранить и выйти')

        v_layout = Qt.QVBoxLayout(self)
        v_layout.addWidget(self.id_label)
        v_layout.addWidget(self.name_label)
        v_layout.addWidget(self.name)
        v_layout.addWidget(self.login_label)
        v_layout.addWidget(self.login)
        v_layout.addWidget(self.role_label)
        v_layout.addWidget(self.password_label)
        v_layout.addWidget(self.password)
        v_layout.addWidget(self.save_btn)

        self.save_btn.clicked.connect(self.save_and_exit)

    def save_and_exit(self):
        if check_unique_login(str(self.login.text())) or self.user.login == str(self.login.text()):
            if self.password.text():
                password = self.password.text()
                for x in range(10):
                    password = md5(password.encode()).hexdigest()
                update_user(self.u_id, (self.name.text()), str(self.login.text()), str(password))
            else:
                update_user(self.u_id, str(self.name.text()), str(self.login.text()))
            self.accept()
        else:
            Qt.QMessageBox.critical(self, 'Ошибка!', 'Указанный логин уже существует!')
