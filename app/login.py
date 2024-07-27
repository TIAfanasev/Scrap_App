from PyQt5 import Qt, QtWidgets
from PyQt5.QtCore import Qt as Qtt

from hashlib import md5

from PyQt5.QtGui import QIcon

from db_requests import check_logpass, get_user_id_by_login


class Login(Qt.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.u_id = None
        self.role = None
        self.setGeometry(800, 400, 400, 200)
        self.setWindowIcon(QIcon("icons/Icon.png"))
        self.setWindowTitle('Вход')
        self.label = Qt.QLabel('Авторизация')
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.login_label = Qt.QLabel('Логин:')
        self.login_line = Qt.QLineEdit(self)

        self.password_label = Qt.QLabel('Пароль:')
        self.password_line = Qt.QLineEdit(self)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)

        self.lineedit_layout = Qt.QVBoxLayout()
        self.lineedit_layout.addWidget(self.login_label)
        self.lineedit_layout.addWidget(self.login_line)
        self.lineedit_layout.addWidget(self.password_label)
        self.lineedit_layout.addWidget(self.password_line)

        self.log_in = Qt.QPushButton('Войти')

        self.v_layout = Qt.QVBoxLayout(self)
        self.v_layout.addWidget(self.label)
        self.v_layout.addLayout(self.lineedit_layout)
        self.v_layout.addWidget(self.log_in)

        self.log_in.clicked.connect(self.lets_login)

    def lets_login(self):
        password = self.password_line.text()
        for x in range(10):
            password = md5(password.encode()).hexdigest()
        self.role = check_logpass(self.login_line.text(), password)
        if self.role:
            self.u_id = get_user_id_by_login(self.login_line.text())
            self.accept()
        else:
            Qt.QMessageBox.critical(self, 'Ошибка!', f'Доступ запрещен!\nЛогин или пароль введены неверно')
            self.login_line.clear()
            self.password_line.clear()
